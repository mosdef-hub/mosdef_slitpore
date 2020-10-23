from mbuild.recipes.porebuilder import GraphenePore
import mbuild as mb
from foyer import Forcefield
import mbuild.formats.charmm_writer as mf_charmm


Water_res_name = 'H2O'
Fake_water_res_name = 'h2o'

FF_file = '../../../../../mosdef_slitpore/ffxml/pore-spce.xml'
FF_file_fake_water = '../../../../../mosdef_slitpore/ffxml/FF_Fake_SPCE.xml'


water = mb.load('O', smiles=True)
water.name = Water_res_name
print('water.name = '+str(water.name))

water.energy_minimization(forcefield = FF_file , steps=10**9)

Fake_water = mb.load('O', smiles=True)
Fake_water.name = Fake_water_res_name
Fake_water.energy_minimization(forcefield = FF_file_fake_water , steps=10**9)


FF_Graphene_pore_w_solvent_fake_water_Dict = {'H2O' : FF_file, 'h2o' : FF_file_fake_water , 'BOT': FF_file, 'TOP': FF_file}
residues_Graphene_pore_w_solvent_fake_water_List = [Fake_water.name, water.name,  'BOT', 'TOP']
Fix_bonds_angles_fake_water_residues = [ water.name, Fake_water.name]

Fix_Graphene_residue = [ 'BOT', 'TOP']



#**************************************************************
# builds water reservoir (start)
#**************************************************************

box_reservior_w_fake_water = mb.fill_box(compound=[water,Fake_water],density=600,
                            box=[6,6,6], compound_ratio=[0.8,0.2])
#**************************************************************
# builds water reservoir (end)
#**************************************************************

#**************************************************************
# builds filled graphene slit  for 20 Ang or 2nm (start)
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

z_shift= 0

#note the default spacing of 0.2 automatically accounted for in the water box packing (i.e. adding 0.2 nm for 1 wall is really 0.4 nm)
water_between_pores = mb.fill_box(compound=[water,Fake_water], n_compounds= [n_waters, n_fake_waters] , box=[3.0, 3.0, pore_width_nm - water_spacing_from_walls*1])
water_between_pores.translate([0,  0, sheet_spacing*(2*No_sheets-1) + water_spacing_from_walls])
water_between_pores.translate([ -water_between_pores.center[0],   -water_between_pores.center[1], z_shift])

empty_graphene_pore.translate([ -empty_graphene_pore.center[0],   -empty_graphene_pore.center[1], z_shift])

filled_pore = empty_graphene_pore
filled_pore.add(water_between_pores, inherit_periodicity=False)
filled_pore.translate([ -filled_pore.center[0],   -filled_pore.center[1], 0])
filled_pore.periodicity[2] = sheet_spacing*(2*No_sheets-1)+pore_width_nm

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



#**************************************************************
# builds filled graphene slit  for 20 Ang or 2nm (end)
#**************************************************************


