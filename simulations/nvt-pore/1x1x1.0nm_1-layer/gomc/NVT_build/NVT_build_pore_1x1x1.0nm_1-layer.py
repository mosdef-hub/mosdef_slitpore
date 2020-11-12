from mbuild import recipes
import mbuild as mb
from foyer import Forcefield
import parmed.structure
import foyer
import sys
sys.path.append('../../../../../')
from mosdef_slitpore.utils import charmm_writer as mf_charmm

Water_res_name = 'H2O'

FF_file = '../../../../../mosdef_slitpore/ffxml/pore-spce.xml'

water = mb.load('O', smiles=True)
water.name = Water_res_name
water.energy_minimize(forcefield = FF_file , steps=10**9)


FF_Graphene_pore_w_solvent_water_Dict = {'H2O' : FF_file, 'BOT': FF_file, 'TOP': FF_file}
residues_Graphene_pore_w_solvent_water_List = [ water.name,  'BOT', 'TOP' ]
Fix_bonds_angles_water_residues = [ water.name ]

Fix_Graphene_residue = [ 'BOT', 'TOP']


#**************************************************************
# builds empty graphene slit  for 10 Ang or 1nm (start)
#**************************************************************
# Create graphene system
pore_width_nm = 1.0
No_sheets = 1
sheet_spacing = 1

water_spacing_from_walls = 0.2

n_waters = 24

empty_graphene_pore =recipes.GraphenePore( pore_width=sheet_spacing ,
                                    pore_length=1.0 ,
                                    pore_depth=1.1 ,
                                    n_sheets=No_sheets,
                                    slit_pore_dim=2 )

empty_graphene_pore_shifted = empty_graphene_pore



#note the default spacing of 0.2 automatically accounted for in the water box packing (i.e. adding 0.2 nm for 1 wall is really 0.4 nm)
water_between_pores = mb.fill_box(compound=[water], n_compounds= [n_waters] , box=[1, 1, pore_width_nm - water_spacing_from_walls*1])
water_between_pores.translate([0,  0, 0.2])


filled_pore = empty_graphene_pore
filled_pore.add(water_between_pores, inherit_periodicity=False)
filled_pore.translate([ -filled_pore.center[0]-0.0204/2,   -filled_pore.center[1]-0.182/2-0.0232, 0.5])
filled_pore.periodicity[2] = 2.0


mf_charmm.charmm_psf_psb_FF(filled_pore,
                            'filled_pore_water_1x1x1.0nm_1-layer',
                            structure_1 = None ,
                            filename_1 = None,
                            FF_filename ="GOMC_pore_water_FF" ,
                            forcefield_files= FF_Graphene_pore_w_solvent_water_Dict ,
                            residues= residues_Graphene_pore_w_solvent_water_List ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = Fix_Graphene_residue,
                            fix_res_bonds_angles = Fix_bonds_angles_water_residues,
                            reorder_res_in_pdb_psf = False
                            )



#**************************************************************
# builds empty graphene slit  for 10 Ang or 1nm (end)
#**************************************************************


