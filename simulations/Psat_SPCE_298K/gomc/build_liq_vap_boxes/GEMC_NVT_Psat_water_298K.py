import mbuild as mb
from foyer import Forcefield
import sys
sys.path.append('../../../../')
from mosdef_slitpore.utils import charmm_writer as mf_charmm

Water_res_name = 'H2O'
FF_file_water = '../../../../mosdef_slitpore/ffxml/pore-spce.xml'

water = mb.load('O', smiles=True)
water.name = Water_res_name
water.energy_minimize(forcefield = FF_file_water , steps=10**9)


FF_Dict = {water.name: FF_file_water }

residues_List = [water.name]

Fix_bonds_angles_residues = [ water.name ]



print('Running: filling liquid box')
water_box_liq = mb.fill_box(compound=[water],
                            density= 950 ,
                            compound_ratio = [1] ,
                            box=[3.0, 3.0, 3.0] )
print('Completed: filling liquid box')

print('Running: filling vapor box')
water_box_vap = mb.fill_box(compound=[water,],
                            n_compounds = [50],
                            box=[60, 60, 60])
print('Completed: filling vapor box')



print('Running: GOMC FF file, and the psf and pdb files')
mf_charmm.charmm_psf_psb_FF(water_box_liq,
                            'Box_0_liq_water_30A_L_cubed_box',
                            structure_1 = water_box_vap ,
                            filename_1 = 'Box_1_vap_water_600A_L_cubed_box',
                            FF_filename ="GOMC_water_FF" ,
                            forcefield_files = FF_Dict,
                            residues= residues_List ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = Fix_bonds_angles_residues,
                            reorder_res_in_pdb_psf = False
                            )
print('Completed: GOMC FF file, and the psf and pdb files')