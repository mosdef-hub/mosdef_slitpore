import flow
from flow import FlowProject, directives
import templates.ndcrc
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Project(FlowProject):
    pass


@Project.label
def nvt_complete(job):
    "Verify that the simulation has completed"

    import numpy as np

    try:
        thermo_data = np.genfromtxt(job.fn("equil.nvt.out.prp"), skip_header=3)
        completed = int(thermo_data[-1][0]) == job.sp.nsteps_eq
    except:
        completed = False
        pass

    return completed


@Project.label
def gcmc_complete(job):
    "Verify that the simulation has completed"

    import numpy as np

    try:
        thermo_data = np.genfromtxt(
            job.fn("equil.gcmc.out.prp"), skip_header=3
        )
        completed = int(thermo_data[-1][0]) == job.sp.nsteps_prod
    except:
        completed = False
        pass

    return completed


@Project.operation
@Project.post(gcmc_complete)
@directives(omp_num_threads=4)
def run_desorption(job):
    """Run desorption simulation for the given statepoint"""

    import mbuild
    import unyt as u

    from mosdef_slitpore.utils.cassandra import run_desorption
    from mosdef_slitpore.utils.cassandra import spce_water

    temperature = job.sp.T * u.K
    mu = job.sp.mu * u.kJ / u.mol
    nwater = job.sp.nwater
    nsteps_eq = job.sp.nsteps_eq
    nsteps_prod = job.sp.nsteps_prod

    # Create pore system
    empty_pore = mbuild.recipes.GraphenePore(
        pore_width=1.0,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=3,
        slit_pore_dim=2,
    )

    # Translate to centered at 0,0,0 and make box larger in z
    empty_pore.translate(-empty_pore.center)
    empty_pore.periodicity[2] = 6.0

    # Create a water molecule with the spce geometry
    water = spce_water()
    # Create box of water to place in pore
    water_box = mbuild.Box([3.0, 3.0, 0.8])  # nm
    water = mbuild.fill_box(water, n_compounds=nwater, box=water_box)
    water.translate(-water.center)
    filled_pore = mbuild.Compound()
    filled_pore.add(empty_pore, inherit_periodicity=True)
    filled_pore.add(water, inherit_periodicity=False)

    # Run simulation from inside job dir
    with job:
        run_desorption(
            empty_pore,
            filled_pore,
            nwater,
            temperature,
            mu,
            nsteps_eq,
            nsteps_prod,
            pore_width=1.0 * u.nm,
        )


if __name__ == "__main__":
    Project().main()
