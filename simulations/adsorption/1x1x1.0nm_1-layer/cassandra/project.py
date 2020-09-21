import flow
from flow import FlowProject, directives
import templates.ndcrc
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Project(FlowProject):
    pass


@Project.label
def simulation_complete(job):
    "Verify that the simulation has completed"

    import numpy as np

    try:
        thermo_data = np.genfromtxt(job.fn("equil.out.prp"), skip_header=3)
        completed = int(thermo_data[-1][0]) == job.sp.nsteps
    except:
        completed = False
        pass

    return completed


@Project.operation
@Project.post(simulation_complete)
@directives(omp_num_threads=4)
def run_adsorption(job):
    """Run adsorption simulation for the given statepoint"""

    import mbuild
    import foyer
    import unyt as u
    import mosdef_cassandra as mc

    from mosdef_slitpore.utils.utils import get_ff
    from mosdef_slitpore.utils.cassandra import spce_water

    temperature = job.sp.T * u.K
    mu = job.sp.mu * u.kJ / u.mol
    nsteps = job.sp.nsteps

    # Create graphene system
    pore = mbuild.recipes.GraphenePore(
        pore_width=1.0,
        pore_length=1.0,
        pore_depth=1.1,
        n_sheets=1,
        slit_pore_dim=2,
    )

    # Translate to centered at 0,0,0 and make box larger in z
    pore.translate(-pore.center)
    pore.periodicity[2] = 2.0

    # Run simulation from inside job dir
    with job:
        # Apply ff
        ff = foyer.Forcefield(get_ff("pore-spce.xml"))
        typed_pore = ff.apply(pore)

        # Create a water molecule with the spce geometry
        water = spce_water()
        typed_water = ff.apply(water)

        # Create box and species list
        box_list = [pore]
        species_list = [typed_pore, typed_water]

        # Specify mols at start of the simulation
        mols_in_boxes = [[1, 0]]

        # Create MC system
        system = mc.System(box_list, species_list, mols_in_boxes=mols_in_boxes)
        moves = mc.MoveSet("gcmc", species_list)

        # Set move probabilities
        moves.prob_translate = 0.25
        moves.prob_rotate = 0.25
        moves.prob_insert = 0.25
        moves.prob_regrow = 0.0

        # Set thermodynamic properties
        thermo_props = [
            "energy_total",
            "volume",
            "nmols",
            "mass_density",
        ]

        custom_args = {
            "cutoff_style": "cut",
            "charge_style": "ewald",
            "rcut_min": 0.5 * u.angstrom,
            "vdw_cutoff": 4.9 * u.angstrom,
            "charge_cutoff": 4.9 * u.angstrom,
            "properties": thermo_props,
            "angle_style": ["harmonic", "fixed"],
            "run_name": "equil",
            "coord_freq": 50000,
        }

        # Specify the restricted insertion
        restricted_type = [[None, "slitpore"]]
        restricted_value = [[None, 0.5 * u.nm ]]
        moves.add_restricted_insertions(
            species_list, restricted_type, restricted_value
        )

        mc.run(
            system=system,
            moveset=moves,
            run_type="equilibration",
            run_length=nsteps,
            temperature=temperature,
            chemical_potentials=["none", mu],
            **custom_args,
        )

if __name__ == "__main__":
    Project().main()
