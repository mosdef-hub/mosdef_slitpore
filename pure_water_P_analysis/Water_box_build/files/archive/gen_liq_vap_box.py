import mbuild as mb
import cg_bead_builds
import generate_sim_boxes

filename_box_info_BC = 'Testing_Box_Generator' # no extention

approx_total_No_atoms_liq_BC = 10000
approx_total_No_atoms_per_cg_atom_BC = 2.7    # 1 for AA and ~2.5 to 2.75 for UA.
min_atom_spacing_BC = 0.3
vol_vap_div_vol_liq_BC = 10
molecules_vap_div_molecules_liq_BC = 0.1
random_seed_No_BC = 12345
forcefield_file_to_use_bc = 'trappe-ua.xml'#'trappe-ua.xml'
Print_Individ_molecules_BC = False
combining_rules = 'lorentz'

mol_fraction_Molecule_0 = 0.1
mol_fraction_Molecule_1 = 0.2
mol_fraction_Molecule_2 = 0.3
mol_fraction_Molecule_3 = 0.4

Molecule_0 = cg_bead_builds.ethane(name='cm0')
Molecule_1 = cg_bead_builds.isoButane(name='cm1')
Molecule_2 = cg_bead_builds.Alkane_Bead(chain_length=4, name='cm2')
Molecule_3 = cg_bead_builds.Alkane_Bead(chain_length=6, name='cm3')


Molecule_Type_List_BC = [Molecule_0, Molecule_1 , Molecule_2, Molecule_3]
Molecule_mol_Fraction_List_BC = [mol_fraction_Molecule_0, mol_fraction_Molecule_1, mol_fraction_Molecule_2, mol_fraction_Molecule_3]


#filename_box_info = filename_box_info_BC

generate_sim_boxes.Gen_Liq_and_Vap_Boxes(filename_box_info = filename_box_info_BC,
                                         Molecule_Type_List = Molecule_Type_List_BC,
                                         Molecule_mol_Fraction_List= Molecule_mol_Fraction_List_BC,
                                         forcefield_file_to_use = forcefield_file_to_use_bc,
                                         Print_Individ_molecules=Print_Individ_molecules_BC,
                                         approx_total_No_atoms_liq=approx_total_No_atoms_liq_BC,
                                        approx_total_No_atoms_per_cg_atom=approx_total_No_atoms_per_cg_atom_BC,
                                         min_atom_spacing =min_atom_spacing_BC,
                                         vol_vap_div_vol_liq = vol_vap_div_vol_liq_BC,
                                         molecules_vap_div_molecules_liq = molecules_vap_div_molecules_liq_BC,
                                         random_seed_No = random_seed_No_BC,
                                         combining_rules=combining_rules)


