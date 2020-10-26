import flow
import warnings


from flow import FlowProject, directives
from mosdef_slitpore.utils.cassandra_helpers import check_simulation


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Project(FlowProject):
    pass


@Project.label
def equil_complete(job):
    """Check if the equilibration simulation has completed"""
    return check_simulation(job.fn("equil.out.prp"), job.sp.nsteps.equil)


@Project.label
def prod_complete(job):
    """Check if the production simulation has completed"""
    return check_simulation(job.fn("prod.out.prp"), job.sp.nsteps.prod)


@Project.operation
@Project.post(prod_complete)
@directives(omp_num_threads=4)
def run_simulation(job):
    """Run GCMC simulations for the given statepoint"""

    import mbuild
    import foyer
    import unyt as u
    import numpy as np
    import mosdef_cassandra as mc

    from mosdef_slitpore.utils.cassandra_helpers import spce_water
    from mosdef_slitpore.utils.utils import get_ff

    temperature = job.sp.T * u.K
    mu = job.sp.mu * u.kJ / u.mol
    nsteps_eq = job.sp.nsteps.equil
    nsteps_prod = job.sp.nsteps.prod
    seed1 = job.sp.seed1
    seed2 = job.sp.seed2

    # Want box size to depend on chemical potential
    # Prelim simulation shows mu' = -48 kJ/mol; p ~ 0.01 bar
    # Employ IG law to estimate remaining box sizes; target 40 waters
    mu_0 = -48 * u.kJ/u.mol
    p_0 = 0.01 * u.bar
    n_water_target = 40
    p_ig = p_0 * np.exp((mu-mu_0)/(u.kb * temperature))
    vol = n_water_target * u.kb * temperature / p_ig
    boxl = (vol**(1./3.)).to_value("nm")

    # Define custom_args that are the same
    # for all pure phase simulations
    custom_args = {
        "cutoff_style": "cut",
        "charge_style": "ewald",
        "rcut_min": 0.5 * u.angstrom,
        "vdw_cutoff": 9.0 * u.angstrom,
        "charge_cutoff": 0.25 * boxl * u.nm,
        "prop_freq": 1000,
        "angle_style": ["fixed"],
        "seeds" : [seed1, seed2],
    }

    # Create a water molecule with the spce geometry
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))
    water_typed = ff.apply(spce_water)

    species_list = [water_typed]
    box_list = [mbuild.Box([boxl, boxl, boxl])]
    system = mc.System(
        box_list, species_list,
    )
    moveset = mc.MoveSet("gcmc", species_list)
    moveset.prob_regrow = 0.0
    moveset.prob_translate = 0.3
    moveset.prob_rotate = 0.3
    moveset.prob_insert = 0.2

    with job:
        mc.run(
            system=system,
            moveset=moveset,
            run_type="equil",
            run_length=nsteps_eq,
            temperature=temperature,
            run_name="equil",
            chemical_potentials=[mu],
            **custom_args,
        )

        mc.restart(
            system=system,
            moveset=moveset,
            run_type="prod",
            run_length=nsteps_prod,
            temperature=temperature,
            run_name="prod",
            restart_name="equil",
            chemical_potentials=[mu],
            **custom_args,
        )


if __name__ == "__main__":
    Project().main()
