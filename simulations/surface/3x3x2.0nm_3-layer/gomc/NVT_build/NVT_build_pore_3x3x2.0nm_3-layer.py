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

FF_file = '../../../../../../mosdef_slitpore/ffxml/pore-spce.xml'
FF_file_fake_water = '../../../../../../mosdef_slitpore/ffxml/FF_Fake_SPCE.xml'


water = mb.load('O', smiles=True)
water.name = Water_res_name
water.energy_minimization(forcefield = FF_file , steps=10**9)

FF_Graphene_pore_w_solvent_Dict = {'H2O' : FF_file, 'BOT' : FF_file, 'TOP' : FF_file}
residues_Graphene_pore_w_solvent_List = [ water.name,   'BOT', 'TOP']
Fix_bonds_angles_residues = [ water.name]

Fix_Graphene_residue = [ 'BOT', 'TOP']


#**************************************************************
# builds empty graphene slit  for 20 Ang or 1nm (start)
#**************************************************************

# Create graphene system
pore_width_nm = 2
No_sheets = 3
sheet_spacing = 1

water_spacing_from_walls = 0.2

Total_box_z_axis_nm = 6
graphene_sheet_space_nm = 0.335

n_waters = 485

empty_graphene_pore = GraphenePore( pore_width=pore_width_nm ,
                                    pore_length=3.0,
                                    pore_depth=3.0,
                                    n_sheets=No_sheets,
                                    slit_pore_dim=2 )


z_shift= Total_box_z_axis_nm / 2 - (graphene_sheet_space_nm * (No_sheets - 1) + pore_width_nm/2)

water_between_pores = mb.fill_box(compound=[water], n_compounds= [n_waters] , box=[2.90, 2.90, pore_width_nm - water_spacing_from_walls*1])
water_between_pores.translate([0,  0, water_spacing_from_walls + graphene_sheet_space_nm*(No_sheets-1)])
water_between_pores.translate([ -water_between_pores.center[0],   -water_between_pores.center[1], z_shift])

empty_graphene_pore.translate([ -empty_graphene_pore.center[0],   -empty_graphene_pore.center[1], z_shift])

filled_pore = empty_graphene_pore
filled_pore.add(water_between_pores, inherit_periodicity=False)
filled_pore.periodicity[2] = Total_box_z_axis_nm



mf_charmm.charmm_psf_psb_FF(filled_pore,
                  'filled_pore_water_3x3x2.0nm_3-layer',
                  structure_1 = None,
                  filename_1 = None,
                            GOMC_FF_filename ="GOMC_pore_water_FF" ,
                  forcefield_files= FF_Graphene_pore_w_solvent_Dict ,
                  residues=residues_Graphene_pore_w_solvent_List ,
                  Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_residues,
                            reorder_res_in_pdb_psf = False
                            )




#**************************************************************
# builds empty graphene slit  for 10 Ang or 1nm (end)
#**************************************************************



