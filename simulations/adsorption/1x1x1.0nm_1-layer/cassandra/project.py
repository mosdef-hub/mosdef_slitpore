import flow
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
        pore_length=1.0,
        pore_depth=1.1,
        pore_width=pore_width.to_value("nm"),
        n_sheets=1,
        slit_pore_dim=2,
    )

    # Translate to centered at 0,0,0 and make box larger in z
    empty_pore.translate(-empty_pore.center)
    empty_pore.periodicity[2] = 2.0

    # Run simulation from inside job dir
    # Here we lower the vdw/charge cutoffs bc of small box
    with job:
        run_adsorption(
            empty_pore,
            pore_width,
            temperature,
            mu,
            nsteps_gcmc,
            seeds = [seed1, seed2],
            vdw_cutoff = 4.9 * u.angstrom,
            charge_cutoff = 4.9 * u.angstrom,
        )


if __name__ == "__main__":
    Project().main()
