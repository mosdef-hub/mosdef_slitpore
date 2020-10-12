import flow
import templates.ndcrc
import warnings


from flow import FlowProject, directives
from mosdef_slitpore.utils.cassandra_helpers import check_simulation


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Project(FlowProject):
    pass


@Project.label
def gcmc_complete(job):
    """Check if the GCMC simulation has completed"""
    return check_simulation(job.fn("gcmc.out.prp"), job.sp.nsteps_gcmc)


@Project.operation
@Project.post(gcmc_complete)
@directives(omp_num_threads=4)
def run_adsorption(job):
    """Run adsorption simulation for the given statepoint"""

    import mbuild
    import unyt as u

    from mosdef_slitpore.utils.cassandra_runners import run_adsorption

    pore_width = 1.0 * u.nm

    temperature = job.sp.T * u.K
    mu = job.sp.mu * u.kJ / u.mol
    nsteps_gcmc = job.sp.nsteps_gcmc
    seed1 = job.sp.seed1
    seed2 = job.sp.seed2

    # Create empty pore system
    empty_pore = mbuild.recipes.GraphenePore(
        pore_length=3.0,
        pore_depth=3.0,
        pore_width=pore_width.to_value("nm"),
        n_sheets=3,
        slit_pore_dim=2,
    )

    # Translate to centered at 0,0,0 and make box larger in z
    box_center = empty_pore.periodicity/2.0
    empty_pore.translate(-box_center)
    empty_pore.periodicity[2] = 6.0

    # Run simulation from inside job dir
    with job:
        run_adsorption(
            empty_pore,
            pore_width,
            temperature,
            mu,
            nsteps_gcmc,
            seeds = [seed1, seed2]
        )


if __name__ == "__main__":
    Project().main()
