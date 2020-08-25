import flow
import signac
import warnings
import os
import foyer
import mbuild as mb
from flow import FlowProject, directives
from mosdef_slitpore.utils.utils import get_ff
from mosdef_slitpore.utils.gromacs import write_ndx, add_settles

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
def em_complete(job):
    """Verify that energy minimization has completed"""
    return job.isfile('em.gro')

@Project.label
def nvt_complete(job):
    """Verify that the nvt simulation has completed"""
    return job.isfile('nvt.gro')

@Project.operation
@Project.post(init_complete)
def initialize(job):
    water = mb.load('O', smiles=True)
    water.name = 'SOL'
    pore = mb.recipes.GraphenePoreSolvent(
        pore_width=1.0,
        pore_length=1.0,
        pore_depth=1.1,
        n_sheets=1,
        slit_pore_dim=2,
        solvent=water,
        n_solvent=n_solvent,
        x_bulk=0,
    )
   
    pore.periodicity[1] = 2.0
    
    ff = foyer.Forcefield(get_ff("pore-spce.xml"))
    
    water = mb.Compound()
    gph = mb.Compound()
    for child in pore.children:
        if child.name == 'SOL':
            water.add(mb.clone(child))
        else:
            gph.add(mb.clone(child)) 

    typed_water = ff.apply(water, residues='SOL')
    typed_gph = ff.apply(gph)

    typed_pore = typed_gph + typed_water

    with job:
        typed_pore.save('init.gro', combine='all', overwrite=True)
        typed_pore.save('init.top', combine='all', overwrite=True)
        typed_pore.save('init.mol2', overwrite=True)

        add_settles('init.top')
        write_ndx(path='.')


@Project.operation
@Project.pre(init_complete)
@Project.post(em_complete)
@flow.cmd
def run_em(job):
    return _gromacs_str("em.mdp", "em", "init")

@Project.operation
@Project.pre(em_complete)
@Project.post(nvt_complete)
@flow.cmd
def run_nvt(job):
    return _gromacs_str("nvt.mdp", "nvt", "em")

def _gromacs_str(mdp, op_name, gro_name):
    """Helper function, returns grompp command string for operation """
    mdp = signac.get_project().fn("files/{}.mdp".format(op_name))
    cmd = "gmx grompp -f {mdp} -c {gro_name}.gro -p init.top -o {op_name}.tpr --maxwarn 1 && gmx mdrun -deffnm {op_name}"
    return workspace_command(
        cmd.format(mdp=mdp, op_name=op_name, gro_name=gro_name)
    )


if __name__ == "__main__":
    Project().main()
