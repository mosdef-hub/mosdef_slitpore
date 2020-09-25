import flow
import templates.ndcrc
import warnings


from flow import FlowProject, directives
from mosdef_slitpore.utils.cassandra_helpers import check_simulation


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Project(FlowProject):
    pass


@Project.label
def equil_complete(job):
    """Check if the equilibration simulation has completed"""
    return check_simulation(job.fn("equil.nvt.out.prp"), job.sp.nsteps.equil)


@Project.label
def prod_complete(job):
    """Check if the production simulation has completed"""
    return check_simulation(job.fn("prod.nvt.out.prp"), job.sp.nsteps.prod)


@Project.operation
@Project.post(prod_complete)
@directives(omp_num_threads=4)
def run_simulation(job):
    """Run NVT simulations for the given statepoint"""

    import mbuild
    import unyt as u

    from mosdef_slitpore.utils.cassandra_runners import run_nvt
    from mosdef_slitpore.utils.cassandra_helpers import spce_water

    pore_width = 1.0 * u.nm

    temperature = job.sp.T * u.K
    nwater = job.sp.nwater
    nsteps_eq = job.sp.nsteps.equil
    nsteps_prod = job.sp.nsteps.prod
    seed1 = job.sp.seed1
    seed2 = job.sp.seed2

    # Create pore system
    filled_pore = mbuild.recipes.GraphenePoreSolvent(
        pore_length=1.0,
        pore_depth=1.1,
        pore_width=pore_width.to_value("nm"),
        n_sheets=1,
        slit_pore_dim=2,
        x_bulk=0,
        solvent=spce_water,
        n_solvent=nwater,
    )

    # Translate to centered at 0,0,0 and make box larger in z
    box_center = filled_pore.periodicity/2.0
    filled_pore.translate(-box_center)
    filled_pore.periodicity[2] = 2.0

    # Run simulation from inside job dir
    with job:
        run_nvt(
            filled_pore,
            temperature,
            nsteps_eq,
            nsteps_prod,
            seeds = [seed1, seed2],
            vdw_cutoff=4.9 * u.angstrom,
            charge_cutoff=4.9 * u.angstrom
        )


if __name__ == "__main__":
    Project().main()
