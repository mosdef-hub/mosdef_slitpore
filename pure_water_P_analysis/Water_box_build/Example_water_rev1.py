import mbuild as mb
from foyer import Forcefield
import parmed as pmd
import os
#import files.generate_sim_boxes as generate_sim_boxes

# This file allows generation of 2 types of water molecules with different
# residue names.  These waters must have a FF specified to the residue,
# which allows for multiple FFs and stops conflicting FF from erroring out.

#Note residues= Molecule_ResName_List and forcefield_files=forcefield_file_to_use, must
# have the residue matched with the FFs in sequence.

#fix_residue = list: fix all atoms from residues in current location
#fix_residue_in_box  = list: fix all atoms from residues to move within the box but cannot be transferred between boxes
# fix_res_bonds_angles = list: fix all bonds and angles of a residue in the FF file (.inp) file

# forcefield_file_to_use = dictionary or string , which applies FF to individual residues or
#                           The string applies to all residues

Water_mol2_file = 'files/tip3p.mol2'

Water_res_name = 'WAT'
Fake_Water_res_name = 'wat'

FF_file = 'files/pore-spce.xml'
FF_fake_water_file = 'files/FF_Fake_SPCE.xml'

water = mb.load(Water_mol2_file)
water.name = Water_res_name
water.energy_minimization(forcefield = FF_file , steps=10**9)

fake_water = mb.load(Water_mol2_file)
fake_water.name = Fake_Water_res_name
fake_water.energy_minimization(forcefield = FF_fake_water_file  , steps=10**9)

Molecule_ResName_List = [water.name] #[water.name]  or [water.name, fake_water.name]

forcefield_file_to_use = FF_file # FF_file or  {water.name : FF_file, fake_water.name : FF_fake_water_file}


filename_box_info = 'Water_boxes_for_test' # no extention
min_atom_spacing =0.25

Density_reservoir_box_kg_m_cubed = 900
Dim_reservoir_box_nm = [5,5,5]


mol_fraction_water = 1    #0.5
#mol_fraction_fake_water = #0.5 if fake water used

fix_residue = None  # can try [water.name]  ,Note: will crash example sim if not None
fix_residue_in_box = None # can try [water.name]  ,Note: will crash example sim if not None
fix_res_bonds_angles =[water.name] ## # can try [water.name]

Molecule_Type_List =[water] #[water, fake_water]
Molecule_mol_Fraction_List = [mol_fraction_water] #[mol_fraction_water, mol_fraction_fake_water ]


print('Running: reservoir packing')
box_reservior = mb.fill_box(compound=Molecule_Type_List,
                      density=Density_reservoir_box_kg_m_cubed,
                      box=Dim_reservoir_box_nm,
                      compound_ratio=Molecule_mol_Fraction_List)
print('Completed: reservoir packing')

print('Completed: reservoir pdb, psf, and parameter generator ')
box_reservior.gomc_save(str(filename_box_info) + '_box' + '.pdb',
                   residues=Molecule_ResName_List,
                   fix_residue=fix_residue,
                   fix_residue_in_box=fix_residue_in_box,
                   overwrite=True )

box_reservior.gomc_save(str(filename_box_info) + '_box' + '.psf',
                   residues=Molecule_ResName_List,
                   forcefield_files=forcefield_file_to_use,
                   overwrite=True )

box_reservior.gomc_save(str(filename_box_info) + '_box' + '.inp',
                   residues=Molecule_ResName_List,
                   forcefield_files=forcefield_file_to_use,
                   fix_res_bonds_angles=fix_res_bonds_angles,
                   overwrite=True )
print('Completed: reservoir pdb, psf, and parameter generator ')
