import flow
from flow import FlowProject, directives
import warnings
import shutil
import os
from mosdef_slitpore.utils.utils import get_ff
from mosdef_slitpore.utils.gromacs import write_ndx, add_settles
from mosdef_slitpore.utils.cassandra_helpers import create_spce_water

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Project(FlowProject):
    pass


@Project.label
def has_setter(job):
    return job.isfile("setter.py")


@Project.label
def has_structure(job):
    return job.isfile("init.mol2")


@Project.label
def has_md_files(job):
    "Verify that the files required for MD simulation are there"

    try:
        return job.isfile(job.doc.input_filename)
    except:
        return False


@Project.label
def md_completed(job):
    "Verify that the md simulation has completed"

    try:
        return job.isfile(job.doc.output_filename)
    except:
        return False


@Project.operation
@Project.post(has_setter)
def copy_setter(job):
    with job:
        print(os.listdir())
        shutil.copyfile(
            Project().root_directory() + "/setter.py", job.workspace() + "/setter.py"
        )


@Project.operation
@Project.post(has_md_files)
def md_files(job):
    import mbuild as mb
    import foyer

    water = create_spce_water()
    water.name = "SOL"
    pore = mb.recipes.GraphenePoreSolvent(
        pore_width=1.0,
        pore_length=1.0,
        pore_depth=1.1,
        n_sheets=1,
        slit_pore_dim=2,
        solvent=water,
        n_solvent=job.sp.nwater,
        x_bulk=0,
    )
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))
    pore.translate([0, 0.3325, 0])

    water = mb.Compound()
    gph = mb.Compound()
    for child in pore.children:
        if child.name == "SOL":
            water.add(mb.clone(child))
        else:
            gph.add(mb.clone(child))

    typed_water = ff.apply(water, residues="SOL", combining_rule="lorentz")
    typed_gph = ff.apply(gph, combining_rule="lorentz")

    typed_pore = typed_gph + typed_water
    typed_pore.box[1] = 20

    with job:
        import os
        import glob
        import numpy as np
        import unyt as u
        import mbuild as mb
        from cp2kmdpy.molecule_optimization import (
            Molecule_optimization,
        )  # for single molecule optimization
        from cp2kmdpy.md import MD  # for running MD
        from cp2kmdpy import runners
        import setter

        typed_pore.save("init.mol2", overwrite=True)
        temperature = job.sp.T * u.K
        # Defining the molecule we want to simulate

        graphene_water = mb.load("init.mol2")

        molecule = graphene_water
        box = mb.box.Box(lengths=[0.9824, 2, 1.0635])
        q = MD(
            molecules=[molecule],
            box=box,
            cutoff=650,
            functional="BLYP",
            basis_set={
                "C": "DZVP-MOLOPT-SR-GTH",
                "H": "DZVP-MOLOPT-SR-GTH",
                "O": "DZVP-MOLOPT-SR-GTH",
            },
            periodicity="XYZ",
            n_molecules=[1],
            traj_type="PDB",
            seed=1,
            project_name="carbon_water",
            initial_coordinate_filename="init.mol2",
            fixed_list="1..80",
        )
        q.temperature = temperature
        q.ensemble = "NVT"
        q.simulation_time = 1000 * u.ps
        # Initializing q
        q.md_initialization()

        # generating input files
        setter.md_files(q)
        job.doc.input_filename = q.input_filename
        job.doc.output_filename = q.output_filename
        job.doc.restart_filename = q.project_name + "-1.restart"


@Project.operation
@Project.pre(has_md_files)
@Project.post(md_completed)
@flow.directives(np=64)
def run_md(job):
    from cp2kmdpy import runners_mpi
    import os

    with job:

        a = runners_mpi.run_md(job.doc.input_filename, job.doc.output_filename, 64)
        print(a)


@Project.operation
@Project.pre(has_md_files)
@flow.directives(np=64)
def restart_md(job):
    from cp2kmdpy import runners_mpi
    import os

    with job:

        a = runners_mpi.run_md(job.doc.restart_filename, job.doc.output_filename, 64)
        print(a)


if __name__ == "__main__":
    Project().main()
