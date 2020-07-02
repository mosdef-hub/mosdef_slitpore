import mbuild as mb
import os
import datetime
import xml.dom.minidom


def Gen_Liq_and_Vap_Boxes(filename_box_info,
                                         Molecule_Type_List = None,
                                         Molecule_mol_Fraction_List= None,
                                         Molecule_ResName_List = None,
                                         forcefield_file_to_use = None,
                                         GOMC_fix_residue = None,
                                         GOMC_fix_residue_in_box = None,
                                         Bead_to_atom_name_dict =  None,
                                         Density_box_box_kg_m_cubed = None ,
                                         Density_reservoir_box_kg_m_cubed =None,
                                         Dim_box_box_nm = None,
                                         Dim_reservoir_box_nm = None, **kwargs):


    if filename_box_info == None:
        print("ERROR: No filename was provided for the variable filename_box_info.\n")

    else:
        with open(filename_box_info+'.txt', 'w') as data_Gen_boxes:

            if Molecule_Type_List == None:
                data_Gen_boxes.write("ERROR: Molecule types are not provided.\n")
                print("ERROR: Molecule types are not provided.")
            elif Molecule_mol_Fraction_List == None:
                data_Gen_boxes.write("ERROR: Molecule fractions for the molecule types are not provided.\n")
                print("ERROR: Molecule fractions for the molecule types are not provided.")
            elif len(Molecule_mol_Fraction_List) != len(Molecule_Type_List):
                data_Gen_boxes.write("ERROR: The number of molecule fractions and molecule types are not equal.\n")
                print("ERROR: The number of molecule fractions and molecule types are not equal.")
            elif sum(Molecule_mol_Fraction_List) != 1:
                data_Gen_boxes.write("ERROR: The total sum of the molecule fractions not equal to zero.\n")
                print("ERROR: The total sum of the molecule fractions not equal to zero.")
            elif forcefield_file_to_use == None:
                data_Gen_boxes.write("ERROR: No force file xml provided are not provided.\n")
                print("ERROR: No force file xml provided are not provided.")
            elif os.path.splitext(forcefield_file_to_use[0])[-1] != '.xml':
                data_Gen_boxes.write("ERROR: No force file not correct or not in xml format.\n")
                print("ERROR: No force file not correct or not in xml format.")
                extension = os.path.splitext(filename)[-1]

            elif len(Molecule_mol_Fraction_List) == len(Molecule_Type_List):
                #enter all the function data here (start)

                print('Running: box packing')
                box_liq = mb.fill_box(compound=Molecule_Type_List,
                                      density=Density_box_box_kg_m_cubed,
                                      box=Dim_box_box_nm,
                                      compound_ratio=Molecule_mol_Fraction_List)
                print('Completed:  box packing')
                print('Running: reservoir packing')
                box_vap = mb.fill_box(compound=Molecule_Type_List,
                                      density=Density_reservoir_box_kg_m_cubed,
                                      box=Dim_reservoir_box_nm,
                                      compound_ratio=Molecule_mol_Fraction_List)
                print('Completed: reservoir packing')



                All_molecule_user_input_interation_lammps_gen_liq = str(filename_box_info)+'_box' + '.lammps'
                All_molecule_user_input_interation_GOMC_gen_liq = str(filename_box_info)+'_box' + '.inp'
                All_molecule_user_input_interation_pdb_gen_liq = str(filename_box_info)+'_box' + '.pdb'
                All_molecule_user_input_interation_psf_gen_liq = str(filename_box_info)+'_box' + '.psf'

                All_molecule_user_input_interation_lammps_gen_vap = str(filename_box_info)+'_reservoir' + '.lammps'
                All_molecule_user_input_interation_GOMC_gen_vap = str(filename_box_info)+'_reservoir' + '.inp'
                All_molecule_user_input_interation_pdb_gen_vap = str(filename_box_info)+'_reservoir' + '.pdb'
                All_molecule_user_input_interation_psf_gen_vap = str(filename_box_info)+'_reservoir' + '.psf'

                print('Running: box pdb, psf, and parameter generator')
                box_liq.save(All_molecule_user_input_interation_pdb_gen_liq, residues=Molecule_ResName_List,
                             GOMC_fix_residue= GOMC_fix_residue, GOMC_fix_residue_in_box=GOMC_fix_residue_in_box, overwrite=True, Bead_to_atom_name_dict = Bead_to_atom_name_dict)
                box_liq.save(All_molecule_user_input_interation_psf_gen_liq, forcefield_files=forcefield_file_to_use, residues=Molecule_ResName_List, overwrite=True, Bead_to_atom_name_dict = Bead_to_atom_name_dict, use_FF_per_residue=True)
                #box_liq.save(All_molecule_user_input_interation_lammps_gen_liq, forcefield_files=forcefield_file_to_use, atom_style=atom_style_to_use, residues=Molecule_ResName_List, overwrite=True, combining_rule=combining_rules, use_FF_per_residue=True)
                #box_liq.save(All_molecule_user_input_interation_GOMC_gen_liq, forcefield_files=forcefield_file_to_use, overwrite=True, residues=Molecule_ResName_List, use_FF_per_residue=True)
                print('Completed: box   pdb, psf, and parameter generator ')
                
                print('Running: reservoir pdb, psf, and parameter generator')
                box_vap.save(All_molecule_user_input_interation_pdb_gen_vap, residues=Molecule_ResName_List,
                             GOMC_fix_residue= GOMC_fix_residue, GOMC_fix_residue_in_box=GOMC_fix_residue_in_box, overwrite=True, Bead_to_atom_name_dict = Bead_to_atom_name_dict)
                box_vap.save(All_molecule_user_input_interation_psf_gen_vap,forcefield_files=forcefield_file_to_use, residues=Molecule_ResName_List, overwrite=True, Bead_to_atom_name_dict = Bead_to_atom_name_dict, use_FF_per_residue=True)
                #box_vap.save(All_molecule_user_input_interation_lammps_gen_vap, forcefield_files=forcefield_file_to_use,atom_style=atom_style_to_use, residues=Molecule_ResName_List, overwrite=True, combining_rule=combining_rules, use_FF_per_residue=True)
                box_vap.save(All_molecule_user_input_interation_GOMC_gen_vap, forcefield_files=forcefield_file_to_use, overwrite=True, residues=Molecule_ResName_List, use_FF_per_residue=True)
                print('Completed: reservoir pdb, psf, and parameter generator ')

            else:
                print('Function is not working properly.')

