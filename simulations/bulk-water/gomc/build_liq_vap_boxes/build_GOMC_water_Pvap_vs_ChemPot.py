import mbuild as mb
from foyer import Forcefield
import mbuild.formats.charmm_writer as mf_charmm

filename_box_info = 'Water_Pvap_vs_Chempot' # no extention

Water_res_name = 'H2O'
FF_file = '../../../../mosdef_slitpore/ffxml/pore-spce.xml'

water = mb.load('O', smiles=True)
water.name = Water_res_name
water.energy_minimization(forcefield = FF_file , steps=10**9)

Molecule_Type_List_BC = [water]
residues_Water_box_List = [water.name]
fix_bonds_angle_names = [water.name]

box_reservior = mb.fill_box(compound=[water],density=600, box=[6,6,6])

mf_charmm.charmm_psf_psb_FF(box_reservior,
                            filename_box_info+'_reservior',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =filename_box_info ,
                            forcefield_files= FF_file ,
                            residues= residues_Water_box_List ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = fix_bonds_angle_names,
                            reorder_res_in_pdb_psf = False
                            )


#create an empty 25 Angstrom box
Empty_box_25A = mb.Compound()
Empty_box_25A.periodicity[0] = 25 / 10
Empty_box_25A.periodicity[1] = 25 / 10
Empty_box_25A.periodicity[2] = 25 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_25A,
                            'Water_boxes_for_test_box_25A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 30 Angstrom box
Empty_box_30A = mb.Compound()
Empty_box_30A.periodicity[0] = 30 / 10
Empty_box_30A.periodicity[1] = 30 / 10
Empty_box_30A.periodicity[2] = 30 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_30A,
                            'Water_boxes_for_test_box_30A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 60 Angstrom box
Empty_box_60A = mb.Compound()
Empty_box_60A.periodicity[0] = 60 / 10
Empty_box_60A.periodicity[1] = 60 / 10
Empty_box_60A.periodicity[2] = 60 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_60A,
                            'Water_boxes_for_test_box_60A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 100 Angstrom box
Empty_box_100A = mb.Compound()
Empty_box_100A.periodicity[0] = 100 / 10
Empty_box_100A.periodicity[1] = 100 / 10
Empty_box_100A.periodicity[2] = 100 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_100A,
                            'Water_boxes_for_test_box_100A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )


#create an empty 200 Angstrom box
Empty_box_200A = mb.Compound()
Empty_box_200A.periodicity[0] = 200 / 10
Empty_box_200A.periodicity[1] = 200 / 10
Empty_box_200A.periodicity[2] = 200 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_200A,
                            'Water_boxes_for_test_box_200A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 300 Angstrom box
Empty_box_300A = mb.Compound()
Empty_box_300A.periodicity[0] = 300 / 10
Empty_box_300A.periodicity[1] = 300 / 10
Empty_box_300A.periodicity[2] = 300 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_300A,
                            'Water_boxes_for_test_box_300A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 400 Angstrom box
Empty_box_400A = mb.Compound()
Empty_box_400A.periodicity[0] = 400 / 10
Empty_box_400A.periodicity[1] = 400 / 10
Empty_box_400A.periodicity[2] = 400 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_400A,
                            'Water_boxes_for_test_box_400A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 500 Angstrom box
Empty_box_500A = mb.Compound()
Empty_box_500A.periodicity[0] = 500 / 10
Empty_box_500A.periodicity[1] = 500 / 10
Empty_box_500A.periodicity[2] = 500 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_500A,
                            'Water_boxes_for_test_box_500A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 600 Angstrom box
Empty_box_600A = mb.Compound()
Empty_box_600A.periodicity[0] = 600 / 10
Empty_box_600A.periodicity[1] = 600 / 10
Empty_box_600A.periodicity[2] = 600 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_600A,
                            'Water_boxes_for_test_box_600A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 800 Angstrom box
Empty_box_800A = mb.Compound()
Empty_box_800A.periodicity[0] = 800 / 10
Empty_box_800A.periodicity[1] = 800 / 10
Empty_box_800A.periodicity[2] = 800 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_800A,
                            'Water_boxes_for_test_box_800A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 1000 Angstrom box
Empty_box_1000A = mb.Compound()
Empty_box_1000A.periodicity[0] = 1000 / 10
Empty_box_1000A.periodicity[1] = 1000 / 10
Empty_box_1000A.periodicity[2] = 1000 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_1000A,
                            'Water_boxes_for_test_box_1000A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 1500 Angstrom box
Empty_box_1500A = mb.Compound()
Empty_box_1500A.periodicity[0] = 1500 / 10
Empty_box_1500A.periodicity[1] = 1500 / 10
Empty_box_1500A.periodicity[2] = 1500 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_1500A,
                            'Water_boxes_for_test_box_1500A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 2000 Angstrom box
Empty_box_2000A = mb.Compound()
Empty_box_2000A.periodicity[0] = 2000 / 10
Empty_box_2000A.periodicity[1] = 2000 / 10
Empty_box_2000A.periodicity[2] = 2000 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_2000A,
                            'Water_boxes_for_test_box_2000A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 3000 Angstrom box
Empty_box_3000A = mb.Compound()
Empty_box_3000A.periodicity[0] = 3000 / 10
Empty_box_3000A.periodicity[1] = 3000 / 10
Empty_box_3000A.periodicity[2] = 3000 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_3000A,
                            'Water_boxes_for_test_box_3000A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 4000 Angstrom box
Empty_box_4000A = mb.Compound()
Empty_box_4000A.periodicity[0] = 4000 / 10
Empty_box_4000A.periodicity[1] = 4000 / 10
Empty_box_4000A.periodicity[2] = 4000 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_4000A,
                            'Water_boxes_for_test_box_4000A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )

#create an empty 5000 Angstrom box
Empty_box_5000A = mb.Compound()
Empty_box_5000A.periodicity[0] = 5000 / 10
Empty_box_5000A.periodicity[1] = 5000 / 10
Empty_box_5000A.periodicity[2] = 5000 / 10
mf_charmm.charmm_psf_psb_FF(Empty_box_5000A,
                            'Water_boxes_for_test_box_5000A',
                            structure_1 = None,
                            filename_1 = None,
                            GOMC_FF_filename =None ,
                            forcefield_files= FF_file  ,
                            residues= [] ,
                            Bead_to_atom_name_dict = None,
                            fix_residue = None,
                            fix_res_bonds_angles = None,
                            reorder_res_in_pdb_psf = False
                            )