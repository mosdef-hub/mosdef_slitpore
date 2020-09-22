#from mbuild.lib.recipes.porebuilder import GraphenePoreSolvent
#from mbuild.lib.recipes.porebuilder import GraphenePore
from mbuild.recipes.porebuilder import GraphenePoreSolvent
from mbuild.recipes.porebuilder import GraphenePore
import mbuild as mb
from foyer import Forcefield
#import mbuild.utils.specific_FF_to_residue as specific_FF_to_residue
import parmed.structure
import foyer
#from mbuild.recipes.porebuilder import porebuilder as recipes
import mbuild.formats.charmm_writer as mf_charmm
#**************************************************************
#**************************************************************
# variables to change  (start)
#**************************************************************
#**************************************************************
Water_res_name = 'H2O'
Fake_water_res_name = 'h2o'


FF_file = '../../../mosdef_slitpore/ffxml/pore-spce.xml'
FF_file_fake_water = '../../../mosdef_slitpore/ffxml/FF_Fake_SPCE.xml'



#**************************************************************
#**************************************************************
# variables to change  (end)
#**************************************************************
#**************************************************************


#**************************************************************
#**************************************************************
# auto-build empty graphene slit, filled water slit, and
# water box.  Generates the FF.inp, psf, and pdb files  (start)
#**************************************************************
#**************************************************************

#**************************************************************
# molecule and residue naming and lists (start)
#**************************************************************

water = mb.load('O', smiles=True)
water.name = Water_res_name
water.energy_minimization(forcefield = FF_file , steps=10**9)

Fake_water = mb.load('O', smiles=True)
Fake_water.name = Fake_water_res_name
Fake_water.energy_minimization(forcefield = FF_file_fake_water , steps=10**9)

FF_Graphene_pore_w_solvent_Dict = {'H2O' : FF_file, 'BOT' : FF_file, 'TOP' : FF_file}
residues_Graphene_pore_w_solvent_List = [ water.name,   'BOT', 'TOP']
Fix_bonds_angles_residues = [ water.name]

FF_Graphene_pore_w_solvent_fake_water_Dict = {'H2O' : FF_file, 'h2o' : FF_file_fake_water , 'BOT': FF_file, 'TOP': FF_file}
residues_Graphene_pore_w_solvent_fake_water_List = [Fake_water.name, water.name,  'BOT', 'TOP']
Fix_bonds_angles_fake_water_residues = [ water.name, Fake_water.name]

Fix_Graphene_residue = [ 'BOT', 'TOP']


#note since graphene is atom type 1 this is OK otherwise we would need to insert
# at least 1 water to get the proper FFs for the current MoSDeF writers.


#**************************************************************
# builds water reservoir (start)
#**************************************************************

box_reservior = mb.fill_box(compound=[water,water],density=600,
                            box=[6,6,6], compound_ratio=[0.8,0.2])

box_reservior_w_fake_water = mb.fill_box(compound=[water,Fake_water],density=600,
                            box=[6,6,6], compound_ratio=[0.8,0.2])

#**************************************************************
# builds water reservoir (end)
#**************************************************************

#**************************************************************
# builds empty graphene slit  for 10 Ang or 1nm (start)
#**************************************************************
# Create graphene system
pore_width_nm = 1.0
No_sheets = 3
sheet_spacing = 0.335
#for GOMC, currently we need to add the space at the end of the simulation
# this does not matter as we are using PBC's
graphene = GraphenePore(
        pore_width=sheet_spacing ,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=No_sheets,
        slit_pore_dim=2
)


# Translate to centered at-graphene.center[0],   -graphene.center[1],0 and make box larger in z
graphene.translate([ -graphene.center[0],   -graphene.center[1],0])
graphene.periodicity[2] = sheet_spacing*(2*No_sheets-1)+pore_width_nm



mf_charmm.charmm_psf_psb_FF(graphene,
                  'pore_3x3x1.0nm_3-layer',
                  structure_1 = box_reservior,
                  filename_1 = 'GOMC_reservior_box',
                            GOMC_FF_filename ="GOMC_pore_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_Dict ,
                  residues=residues_Graphene_pore_w_solvent_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_residues,
                            reorder_res_in_pdb_psf = False
                            )

mf_charmm.charmm_psf_psb_FF(graphene,
                  'pore_3x3x1.0nm_3-layer',
                  structure_1 = box_reservior_w_fake_water,
                  filename_1 = 'GOMC_reservior_fake_water_box',
                            GOMC_FF_filename ="GOMC_pore_fake_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_fake_water_Dict ,
                  residues=residues_Graphene_pore_w_solvent_fake_water_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_fake_water_residues,
                            reorder_res_in_pdb_psf = False
                            )


#**************************************************************
# builds empty graphene slit  for 10 Ang or 1nm (end)
#**************************************************************


#**************************************************************
# builds empty graphene slit  for 16 Ang or 1nm (start)
#**************************************************************
# Create graphene system
pore_width_nm = 1.6
No_sheets = 3
sheet_spacing = 0.335
#for GOMC, currently we need to add the space at the end of the simulation
# this does not matter as we are using PBC's
graphene = GraphenePore(
        pore_width=sheet_spacing ,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=No_sheets,
        slit_pore_dim=2
)


# Translate to centered at-graphene.center[0],   -graphene.center[1],0 and make box larger in z
graphene.translate([ -graphene.center[0],   -graphene.center[1],0])
graphene.periodicity[2] = sheet_spacing*(2*No_sheets-1)+pore_width_nm



mf_charmm.charmm_psf_psb_FF(graphene,
                  'pore_3x3x1.6nm_3-layer',
                  structure_1 = box_reservior,
                  filename_1 = 'GOMC_reservior_box',
                            GOMC_FF_filename ="GOMC_pore_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_Dict ,
                  residues=residues_Graphene_pore_w_solvent_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_residues,
                            reorder_res_in_pdb_psf = False
                            )

mf_charmm.charmm_psf_psb_FF(graphene,
                  'pore_3x3x1.6nm_3-layer',
                  structure_1 = box_reservior_w_fake_water,
                  filename_1 = 'GOMC_reservior_fake_water_box',
                            GOMC_FF_filename ="GOMC_pore_fake_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_fake_water_Dict ,
                  residues=residues_Graphene_pore_w_solvent_fake_water_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_fake_water_residues,
                            reorder_res_in_pdb_psf = False
                            )


#**************************************************************
# builds empty graphene slit  for 16 Ang or 1nm (end)
#**************************************************************


#**************************************************************
# builds empty graphene slit  for 20 Ang or 1nm (start)
#**************************************************************
# Create graphene system
pore_width_nm = 2.0
No_sheets = 3
sheet_spacing = 0.335
#for GOMC, currently we need to add the space at the end of the simulation
# this does not matter as we are using PBC's
graphene = GraphenePore(
        pore_width=sheet_spacing ,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=No_sheets,
        slit_pore_dim=2
)


# Translate to centered at-graphene.center[0],   -graphene.center[1],0 and make box larger in z
graphene.translate([ -graphene.center[0],   -graphene.center[1],0])
graphene.periodicity[2] = sheet_spacing*(2*No_sheets-1)+pore_width_nm



mf_charmm.charmm_psf_psb_FF(graphene,
                  'pore_3x3x2.0nm_3-layer',
                  structure_1 = box_reservior,
                  filename_1 = 'GOMC_reservior_box',
                            GOMC_FF_filename ="GOMC_pore_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_Dict ,
                  residues=residues_Graphene_pore_w_solvent_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_residues,
                            reorder_res_in_pdb_psf = False
                            )

mf_charmm.charmm_psf_psb_FF(graphene,
                  'pore_3x3x2.0nm_3-layer',
                  structure_1 = box_reservior_w_fake_water,
                  filename_1 = 'GOMC_reservior_fake_water_box',
                            GOMC_FF_filename ="GOMC_pore_fake_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_fake_water_Dict ,
                  residues=residues_Graphene_pore_w_solvent_fake_water_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_fake_water_residues,
                            reorder_res_in_pdb_psf = False
                            )


#**************************************************************
# builds empty graphene slit  for 20 Ang or 1nm (end)
#**************************************************************
