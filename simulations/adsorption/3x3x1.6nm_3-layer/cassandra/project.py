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
    import unyt as u

    from mosdef_slitpore.utils.cassandra import run_adsorption

    temperature = job.sp.T * u.K
    mu = job.sp.mu * u.kJ / u.mol
    nsteps = job.sp.nsteps

    # Create graphene system
    pore = mbuild.recipes.GraphenePore(
        pore_width=1.6,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=3,
        slit_pore_dim=2,
    )

    # Translate to centered at 0,0,0 and make box larger in z
    pore.translate(-pore.center)
    pore.periodicity[2] = 6.0

    # Run simulation from inside job dir
    with job:
        run_adsorption(pore, temperature, mu, nsteps)


if __name__ == "__main__":
    Project().main()
