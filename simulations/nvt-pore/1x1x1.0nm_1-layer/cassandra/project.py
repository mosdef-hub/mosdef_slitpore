import flow
import templates.ndcrc
import warnings


from flow import FlowProject, directives
from mosdef_slitpore.utils.cassandra import check_simulation


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Project(FlowProject):
    pass


@Project.label
def equil_complete(job):
    return check_simulation(job.fn("equil.nvt.out.prp"), job.sp.nsteps.equil)


@Project.label
def prod_complete(job):
    return check_simulation(job.fn("prod.nvt.out.prp"), job.sp.nsteps.prod)


@Project.operation
@Project.post(prod_complete)
@directives(omp_num_threads=4)
def run_simulation(job):
    """Run nvt simulation for the given statepoint"""

    import mbuild
    import unyt as u

    from mosdef_slitpore.utils.cassandra import run_nvt
    from mosdef_slitpore.utils.cassandra import spce_water

    temperature = job.sp.T * u.K
    nwater = job.sp.nwater
    nsteps_eq = job.sp.nsteps.equil
    nsteps_prod = job.sp.nsteps.prod
    seed1 = job.sp.seed1
    seed2 = job.sp.seed2

    # Create pore system
    empty_pore = mbuild.recipes.GraphenePore(
        pore_width=1.0,
        pore_length=1.0,
        pore_depth=1.1,
        n_sheets=1,
        slit_pore_dim=2,
    )

    # Translate to centered at 0,0,0 and make box larger in z
    empty_pore.translate(-empty_pore.center)
    empty_pore.periodicity[2] = 2.0

    # Create a water molecule with the spce geometry
    water = spce_water()
    # Create box of water to place in pore
    water_box = mbuild.Box([1.0, 1.0, 0.8]) #nm
    water = mbuild.fill_box(water, n_compounds=nwater, box=water_box)
    water.translate(-water.center)
    filled_pore = mbuild.Compound()
    filled_pore.add(empty_pore, inherit_periodicity=True)
    filled_pore.add(water, inherit_periodicity=False)

    # Run simulation from inside job dir
    with job:
        run_nvt(
            empty_pore,
            filled_pore,
            nwater,
            temperature,
            nsteps_eq,
            nsteps_prod,
            seeds = [seed1, seed2],
            vdw_cutoff=4.9 * u.angstrom,
            charge_cutoff=4.9 * u.angstrom
        )


if __name__ == "__main__":
    Project().main()
