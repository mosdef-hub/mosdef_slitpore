import flow
import signac
import warnings
import os
import foyer
import mbuild as mb
import environment
from flow import FlowProject, directives
from mosdef_slitpore.utils.utils import get_ff
from mosdef_slitpore.utils.gromacs import write_ndx, add_settles
from mbuild.formats.lammpsdata import write_lammpsdata
from mosdef_slitpore.utils.cassandra_helpers import create_spce_water

warnings.filterwarnings("ignore", category=DeprecationWarning)

def workspace_command(cmd):
    """Simple command to always go to the workspace directory"""
    return " && ".join(
        [
            "cd {job.ws}",
            cmd if not isinstance(cmd, list) else " && ".join(cmd),
            "cd ..",
        ]
    )

class Project(FlowProject):
    pass

@Project.label
def init_complete(job):
    """Verify that initialization has completed"""
    return job.isfile('init.gro')

@Project.label
def nvt_complete(job):
    """Verify that the nvt simulation has completed"""
    return job.isfile('data.sample')

@Project.operation
@Project.post(init_complete)
def initialize(job):
    water = create_spce_water()
    water.name = 'SOL'
    pore = mb.recipes.GraphenePoreSolvent(
        pore_width=2.0,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=3,
        slit_pore_dim=2,
        solvent=water,
        n_solvent=job.sp.nwater,
        x_bulk=0,
    )
    
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))
    
    water = mb.Compound()
    gph = mb.Compound()
    for child in pore.children:
        if child.name == 'SOL':
            water.add(mb.clone(child))
        else:
            gph.add(mb.clone(child)) 
    
    typed_water = ff.apply(water, residues='SOL', combining_rule='lorentz')
    typed_gph = ff.apply(gph, combining_rule='lorentz')
    
    typed_pore = typed_gph + typed_water
    typed_pore.box[1] = 60
   
    with job: 
        write_lammpsdata(typed_pore, 'data.spce')
        typed_pore.save('init.mol2', overwrite=True)
        typed_pore.save('init.gro', combine='all', overwrite=True)


@Project.operation
@Project.pre(init_complete)
@Project.post(nvt_complete)
@flow.cmd
def run_nvt(job):
    return _lammps_str(job)

def _lammps_str(job):
    root = job._project.root_directory()
    cmd = ('mpirun -n 16 lmp -i {0}/files/in.spce')

    return workspace_command(cmd.format(root))

if __name__ == "__main__":
    Project().main()
