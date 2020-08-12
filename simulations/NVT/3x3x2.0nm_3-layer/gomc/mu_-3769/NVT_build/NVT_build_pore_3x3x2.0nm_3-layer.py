from mbuild.lib.recipes.porebuilder import GraphenePoreSolvent
from mbuild.lib.recipes.porebuilder import GraphenePore
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

Water_mol2_file = 'files/tip3p.mol2'
Fake_water_mol2_file = 'files/fake_tip3p.mol2'

Water_res_name = 'H2O'
Fake_water_res_name = 'h2o'

FF_file = 'files/FF_graphene_SPCE.xml'
FF_file_fake_water = 'files/FF_Fake_SPCE.xml'


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

water = mb.load(Water_mol2_file)
water.name = Water_res_name

water.energy_minimization(forcefield = FF_file , steps=10**9)

Fake_water = mb.load(Fake_water_mol2_file )
Fake_water.name = Fake_water_res_name
Fake_water.energy_minimization(forcefield = FF_file_fake_water , steps=10**9)


FF_Graphene_pore_w_solvent_fake_water_Dict = {'H2O' : FF_file, 'h2o' : FF_file_fake_water , 'BOT': FF_file, 'TOP': FF_file,'GraphenePore': FF_file }
residues_Graphene_pore_w_solvent_fake_water_List = [Fake_water.name, water.name,  'BOT', 'TOP','GraphenePore',  'F'] #[Fake_water.name, water.name,  'BOT', 'TOP','GraphenePore']
Fix_bonds_angles_fake_water_residues = [ water.name, Fake_water.name]

Fix_Graphene_residue = [ 'BOT', 'TOP']


#note since graphene is atom type 1 this is OK otherwise we would need to insert
# at least 1 water to get the proper FFs for the current MoSDeF writers.


#**************************************************************
# builds water reservoir (start)
#**************************************************************

box_reservior_w_fake_water = mb.fill_box(compound=[water,Fake_water],density=600,
                            box=[6,6,6], compound_ratio=[0.9,0.1])

#**************************************************************
# builds water reservoir (end)
#**************************************************************

#**************************************************************
# builds empty graphene slit  for 10 Ang or 1nm (start)
#**************************************************************
# Create graphene system
pore_width_nm = 2.0
No_sheets = 3
sheet_spacing = 0.335

water_spacing_from_walls = 0.2

Total_waters_fake_water = 540

#for GOMC, currently we need to add the space at the end of the simulation
# this does not matter as we are using PBC's
empty_graphene_pore = GraphenePore(
        pore_width=sheet_spacing ,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=No_sheets,
        slit_pore_dim=2
)

empty_graphene_pore_shifted = empty_graphene_pore


n_fake_waters = 5
n_waters = Total_waters_fake_water - n_fake_waters

#note the default spacing of 0.2 automatically accounted for in the water box packing (i.e. adding 0.2 nm for 1 wall is really 0.4 nm)
water_between_pores = mb.fill_box(compound=[water,Fake_water], n_compounds= [n_waters, n_fake_waters] , box=[3.0, 3.0, pore_width_nm - water_spacing_from_walls*1])
water_between_pores.translate([0,  0, sheet_spacing*(2*No_sheets-1) + water_spacing_from_walls])


filled_pore = empty_graphene_pore
filled_pore.add(water_between_pores, inherit_periodicity=False)
filled_pore.translate([ -filled_pore.center[0],   -filled_pore.center[1], 0])
filled_pore.periodicity[2] = sheet_spacing*(2*No_sheets-1)+pore_width_nm

#for child in filled_pore.children:
    #print("child = " + str(child))

mf_charmm.charmm_psf_psb_FF(filled_pore,
                  'filled_pore_fake_water_3x3x2.0nm_3-layer',
                  structure_1 =None ,
                  filename_1 = None,
                            GOMC_FF_filename ="GOMC_pore_fake_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_fake_water_Dict ,
                  residues= residues_Graphene_pore_w_solvent_fake_water_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_fake_water_residues,
                            reorder_res_in_pdb_psf = False
                            )



mf_charmm.charmm_psf_psb_FF(empty_graphene_pore,
                  'pore_3x3x2.0nm_3-layer',
                  structure_1 = box_reservior_w_fake_water ,
                  filename_1 = 'GOMC_reservior_fake_water_box',
                            GOMC_FF_filename ="GOMC_pore_fake_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_fake_water_Dict ,
                  residues= residues_Graphene_pore_w_solvent_fake_water_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_fake_water_residues,
                            reorder_res_in_pdb_psf = False
                            )

#**************************************************************
# builds empty graphene slit  for 10 Ang or 1nm (end)
#**************************************************************


