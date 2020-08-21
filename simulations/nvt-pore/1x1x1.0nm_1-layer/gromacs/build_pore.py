import numpy as np
import mbuild as mb
import foyer
import os

from mosdef_slitpore.utils.utils import get_ff
from mosdef_slitpore.utils.gromacs import write_ndx, add_settles

def build_gromacs_pore(n_solvent):
    """Build graphene pore with water for gromacs simulation"""
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
   
    #pore.translate([0, 0, 1.0-pore.center[2]]) 
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

    if os.path.exists(f'{n_solvent}_mols'):
       pass
    else:
       os.mkdir(f'{n_solvent}_mols')

    typed_pore.save(f'{n_solvent}_mols/init.gro', combine='all', overwrite=True)
    typed_pore.save(f'{n_solvent}_mols/init.top', combine='all', overwrite=True)
    typed_pore.save(f'{n_solvent}_mols/init.mol2', overwrite=True)

    add_settles(f'{n_solvent}_mols/init.top')
    write_ndx(path=f'{n_solvent}_mols')

for i in [23, 24]:
    build_gromacs_pore(n_solvent=i) 
