#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mbuild as mb
import subprocess
from cssi_cp2k.classes import SIM as sim
import math
# read this: https://www.cp2k.org/_media/events:2015_cecam_tutorial:watkins_optimization.pdf for more knowledge


# In[2]:


def info_molecule(molecule):
    num_atoms=len(molecule.atoms)
    name_atoms=[];
    mass_atoms=[];
    for i in range(num_atoms):
        name_atoms.append(molecule.atoms[i].element_name)
        mass_atoms.append(molecule.atoms[i].mass)
    
    return name_atoms,mass_atoms


# In[ ]:


def remove_duplicate(x):
    return list(dict.fromkeys(x))

def is_cubic(box):
    angles=box.angles
    for angle in angles:
        if math.isclose(angle, 90.0):
            continue
        else:
            return False
            break
    lengths=box.lengths
    a=lengths[0]
    for length in lengths:
        if math.isclose(length, a):
            continue
        else:
            return False
            break
    return True


# In[ ]:


def basis_set_setter(element_symbol):
    #HERE I should define all the elements and all the basis set
    if element_symbol=='H':
        return "TZV2PX-MOLOPT-GTH"
    elif element_symbol=='F':
        return "TZV2PX-MOLOPT-GTH"
    elif element_symbol=='Cl':
        return "TZV2PX-MOLOPT-GTH"
    elif element_symbol=='I':
        return "DZVP-MOLOPT-SR-GTH"
        


# In[ ]:


def potential(element_symbol,functional):
    return "GTH-"+functional
        
def pressure_ensemble(val):
    if val=='NPE_F' or val=='NPE_I' or val=='NPT_F' or val=='NPT_I':
        return True
    else:
        return False

def temperature_ensemble(val):
    if val=='MSST' or val=='MSST_DAMPED' or val=='NPT_F' or val=='NPT_I' or val=='NVT' or val=='NVT_ADIABATIC':
        return True
    else:
        return False

def single_molecule_opt_files(instance):
    molecule=instance.molecule;
    functional=instance.functional;
    box=instance.box;
    cutoff=instance.cutoff
    scf_tolerance=instance.scf_tolerance
    basis_set=instance.basis_set
    basis_set_filename=instance.basis_set_filename
    potential_filename=instance.potential_filename;
    fixed_list=instance.fixed_list;
    periodicity=instance.periodicity
    n_iter=instance.n_iter
    input_filename=instance.input_filename
    output_filename=instance.output_filename

    name=molecule.name
    filled_box=mb.packing.fill_box(molecule,1,box)
    mol_unopt_coord=name+"_unoptimized_coord.xyz"
    #opt_inp_file=name+'_optimization_input.inp'
    filled_box.save(mol_unopt_coord,overwrite='True')
    with open(mol_unopt_coord, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(mol_unopt_coord, 'w') as fout:
        fout.writelines(data[2:]) #deleting first two lines
    print('Initial structure saved as {}'.format(mol_unopt_coord))
    
    molecule=molecule.to_parmed()
    atom_list,mass_list=info_molecule(molecule)
    unique_atom_list=remove_duplicate(atom_list)
    unique_atom_list.sort()
    num_atoms=len(atom_list)
    num_unique_atoms=len(unique_atom_list)

    mySim = sim.SIM()
    #setting defaults
    
    mySim.GLOBAL.RUN_TYPE = "GEO_OPT"
    mySim.GLOBAL.PROJECT_NAME  = name+"_opt"
    mySim.GLOBAL.PRINT_LEVEL = "LOW"
    #FORCE EVAL SECTION
    mySim.FORCE_EVAL.METHOD='QUICKSTEP'
    mySim.FORCE_EVAL.SUBSYS.CELL.ABC='{a} {b} {c}'.format(a=10*box.lengths[0],b=10*box.lengths[1],c=10*box.lengths[2])
    mySim.FORCE_EVAL.SUBSYS.CELL.ALPHA_BETA_GAMMA='{a} {b} {c}'.format(a=box.angles[0],b=box.angles[1],c=box.angles[2])
    mySim.FORCE_EVAL.SUBSYS.CELL.PERIODIC=periodicity
    mySim.FORCE_EVAL.SUBSYS.COORD.DEFAULT_KEYWORD=mol_unopt_coord
    mySim.FORCE_EVAL.SUBSYS.init_atoms(num_atoms);
    
    for i in range(num_unique_atoms):
        mySim.FORCE_EVAL.SUBSYS.KIND[i+1].SECTION_PARAMETERS=unique_atom_list[i]
        
        if basis_set==[None]:
            
            mySim.FORCE_EVAL.SUBSYS.KIND[i+1].BASIS_SET=basis_set_setter(unique_atom_list[i])
        else:
            mySim.FORCE_EVAL.SUBSYS.KIND[i+1].BASIS_SET=basis_set[unique_atom_list[i]]
        mySim.FORCE_EVAL.SUBSYS.KIND[i+1].POTENTIAL=potential(unique_atom_list[i],functional)

    mySim.FORCE_EVAL.DFT.BASIS_SET_FILE_NAME=basis_set_filename;
    mySim.FORCE_EVAL.DFT.POTENTIAL_FILE_NAME=potential_filename;
    mySim.FORCE_EVAL.DFT.QS.EPS_DEFAULT=1E-7
    
    mySim.FORCE_EVAL.DFT.MGRID.CUTOFF=cutoff
    mySim.FORCE_EVAL.DFT.MGRID.REL_CUTOFF=50
    mySim.FORCE_EVAL.DFT.MGRID.NGRIDS=4

    mySim.FORCE_EVAL.DFT.XC.XC_FUNCTIONAL.SECTION_PARAMETERS=functional
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.POTENTIAL_TYPE='PAIR_POTENTIAL'
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.TYPE='DFTD3'
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.PARAMETER_FILE_NAME='dftd3.dat'
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.REFERENCE_FUNCTIONAL=functional
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.R_CUTOFF=8

    mySim.FORCE_EVAL.DFT.SCF.SCF_GUESS='ATOMIC'
    mySim.FORCE_EVAL.DFT.SCF.MAX_SCF=30
    mySim.FORCE_EVAL.DFT.SCF.EPS_SCF=scf_tolerance
    if periodicity=='NONE':
        mySim.FORCE_EVAL.DFT.POISSON.PERIODIC='NONE'
        mySim.FORCE_EVAL.DFT.POISSON.POISSON_SOLVER='WAVELET'
        print('The box should be cubic for non-periodic calculations and the box must be around 15 times the size of the molecule when periodicity is NONE')
    if not is_cubic(box) and periodicity=='NONE':
        print('The box should be cubic for non-periodic calculations and the box must be around 15 times the size of the molecule')

    mySim.MOTION.GEO_OPT.TYPE='MINIMIZATION'
    mySim.MOTION.GEO_OPT.OPTIMIZER='BFGS'
    mySim.MOTION.GEO_OPT.MAX_ITER=n_iter
    mySim.MOTION.GEO_OPT.MAX_DR=1e-3

    mySim.MOTION.CONSTRAINT.FIXED_ATOMS.LIST =fixed_list
    mySim.write_changeLog(fn="mol_opt-changeLog.out")
    mySim.write_errorLog()
    mySim.write_inputFile(fn=input_filename)
    print('Molecule optimization file saved as {}'.format(input_filename))

def md_files(instance):
    molecules=instance.molecules;
    functional=instance.functional;
    box=instance.box;
    cutoff=instance.cutoff
    scf_tolerance=instance.scf_tolerance
    basis_set=instance.basis_set
    basis_set_filename=instance.basis_set_filename
    potential_filename=instance.potential_filename;
    fixed_list=instance.fixed_list;
    periodicity=instance.periodicity
    simulation_time=instance.simulation_time
    time_step=instance.time_step
    ensemble=instance.ensemble
    project_name=instance.project_name
    temperature=instance.temperature
    pressure=instance.pressure
    n_molecules=instance.n_molecules
    thermostat=instance.thermostat
    traj_type=instance.traj_type
    traj_freq=instance.traj_freq
    seed=instance.seed
    input_filename=instance.input_filename
    output_filename=instance.output_filename
    initial_coordinate_filename=instance.initial_coordinate_filename

    if initial_coordinate_filename is None:

        filled_box=mb.packing.fill_box(compound=molecules,n_compounds=n_molecules,box=box)
        initial_coord_file=project_name+".xyz"
        filled_box.save(initial_coord_file,overwrite='True')
        with open(initial_coord_file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(initial_coord_file, 'w') as fout:
            fout.writelines(data[2:]) #deleting first two lines
    else:
        filled_box=mb.load(initial_coordinate_filename)
        initial_coord_file=project_name+".xyz"
        filled_box.save(initial_coord_file,overwrite='True')
        with open(initial_coord_file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(initial_coord_file, 'w') as fout:
            fout.writelines(data[2:]) #deleting first two lines 

    atom_list=[];
    mass_list=[];
    for i in range(len(molecules)):
        current_molecule=mb.clone(molecules[i])
        current_molecule_pmd=current_molecule.to_parmed()
        x,y=info_molecule(current_molecule_pmd);
        atom_list.extend(x)
        mass_list.extend(y)
    unique_atom_list=remove_duplicate(atom_list)
    num_atoms=len(atom_list)
    num_unique_atoms=len(unique_atom_list)
    unique_atom_list.sort()

    mySim = sim.SIM()
    #setting defaults
    
    
    n_steps=int(simulation_time/time_step)
    mySim.GLOBAL.RUN_TYPE = "MD"
    mySim.GLOBAL.PROJECT_NAME  = project_name
    mySim.GLOBAL.PRINT_LEVEL = "LOW"
    mySim.GLOBAL.SEED=seed

    #FORCE EVAL SECTION
    mySim.FORCE_EVAL.METHOD='QUICKSTEP'
    mySim.FORCE_EVAL.STRESS_TENSOR='ANALYTICAL';

    mySim.FORCE_EVAL.DFT.BASIS_SET_FILE_NAME=basis_set_filename
    mySim.FORCE_EVAL.DFT.POTENTIAL_FILE_NAME=potential_filename
    mySim.FORCE_EVAL.DFT.CHARGE=0
    mySim.FORCE_EVAL.DFT.MULTIPLICITY=1
    mySim.FORCE_EVAL.DFT.MGRID.CUTOFF=cutoff
    mySim.FORCE_EVAL.DFT.MGRID.REL_CUTOFF=50
    mySim.FORCE_EVAL.DFT.MGRID.NGRIDS=4
    mySim.FORCE_EVAL.DFT.QS.METHOD='GPW'
    mySim.FORCE_EVAL.DFT.QS.EPS_DEFAULT=1E-8
    mySim.FORCE_EVAL.DFT.QS.EXTRAPOLATION='ASPC'
    mySim.FORCE_EVAL.DFT.POISSON.PERIODIC=periodicity
    mySim.FORCE_EVAL.DFT.PRINT.E_DENSITY_CUBE.SECTION_PARAMETERS="OFF"
    mySim.FORCE_EVAL.DFT.SCF.SCF_GUESS='ATOMIC'
    mySim.FORCE_EVAL.DFT.SCF.MAX_SCF=30
    mySim.FORCE_EVAL.DFT.SCF.EPS_SCF=scf_tolerance

    mySim.FORCE_EVAL.DFT.SCF.OT.SECTION_PARAMETERS=".TRUE."
    mySim.FORCE_EVAL.DFT.SCF.OT.PRECONDITIONER="FULL_SINGLE_INVERSE"
    mySim.FORCE_EVAL.DFT.SCF.OT.MINIMIZER="DIIS"
    mySim.FORCE_EVAL.DFT.SCF.OUTER_SCF.SECTION_PARAMETERS='.TRUE.'

    mySim.FORCE_EVAL.DFT.SCF.OUTER_SCF.MAX_SCF=10
    mySim.FORCE_EVAL.DFT.SCF.OUTER_SCF.EPS_SCF=1e-6
    mySim.FORCE_EVAL.DFT.SCF.PRINT.RESTART.SECTION_PARAMETERS='OFF'
    mySim.FORCE_EVAL.DFT.SCF.PRINT.DM_RESTART_WRITE='.TRUE.'

    mySim.FORCE_EVAL.DFT.XC.XC_FUNCTIONAL.SECTION_PARAMETERS=functional
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.POTENTIAL_TYPE='PAIR_POTENTIAL'
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.TYPE='DFTD3'
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.PARAMETER_FILE_NAME='dftd3.dat'
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.REFERENCE_FUNCTIONAL=functional
    mySim.FORCE_EVAL.DFT.XC.VDW_POTENTIAL.PAIR_POTENTIAL.R_CUTOFF=8

    mySim.FORCE_EVAL.SUBSYS.COORD.DEFAULT_KEYWORD=project_name+".xyz";
    mySim.FORCE_EVAL.SUBSYS.init_atoms(num_atoms);

    for i in range(num_unique_atoms):
        mySim.FORCE_EVAL.SUBSYS.KIND[i+1].SECTION_PARAMETERS=unique_atom_list[i]
        if basis_set==[None]:

            mySim.FORCE_EVAL.SUBSYS.KIND[i+1].BASIS_SET=basis_set_setter(unique_atom_list[i])
        else:
            mySim.FORCE_EVAL.SUBSYS.KIND[i+1].BASIS_SET=basis_set[unique_atom_list[i]]
        mySim.FORCE_EVAL.SUBSYS.KIND[i+1].POTENTIAL=potential(unique_atom_list[i],functional)

    mySim.FORCE_EVAL.SUBSYS.CELL.ABC='{a} {b} {c}'.format(a=10*box.lengths[0],b=10*box.lengths[1],c=10*box.lengths[2])
    mySim.FORCE_EVAL.SUBSYS.CELL.ALPHA_BETA_GAMMA='{a} {b} {c}'.format(a=box.angles[0],b=box.angles[1],c=box.angles[2])

    #MOTION SECTION
    mySim.MOTION.GEO_OPT.OPTIMIZER='BFGS'
    mySim.MOTION.GEO_OPT.MAX_ITER=100
    mySim.MOTION.GEO_OPT.MAX_DR=0.003

    mySim.MOTION.MD.ENSEMBLE = ensemble
    mySim.MOTION.MD.STEPS  = n_steps
    mySim.MOTION.MD.TIMESTEP = time_step

    if temperature_ensemble(ensemble):
        mySim.MOTION.MD.TEMPERATURE = temperature
        mySim.MOTION.MD.THERMOSTAT.TYPE = thermostat
    
        mySim.MOTION.MD.THERMOSTAT.REGION = "MASSIVE"
        mySim.MOTION.MD.THERMOSTAT.NOSE.LENGTH = 5
        mySim.MOTION.MD.THERMOSTAT.NOSE.YOSHIDA = 3
        mySim.MOTION.MD.THERMOSTAT.NOSE.TIMECON = 1000.0
        mySim.MOTION.MD.THERMOSTAT.NOSE.MTS = 2

    if pressure_ensemble(ensemble):

        mySim.MOTION.MD.BAROSTAT.PRESSURE = pressure
        if pressure==None:
            print('you need to define pressure')
    if fixed_list is not None:

        mySim.MOTION.CONSTRAINT.FIXED_ATOMS.LIST =fixed_list
        mySim.MOTION.MD.THERMOSTAT.REGION = "GLOBAL"





    if periodicity=='NONE':
        mySim.FORCE_EVAL.DFT.POISSON.PERIODIC='NONE'
        mySim.FORCE_EVAL.DFT.POISSON.POISSON_SOLVER='WAVELET'
    if not is_cubic(box) and periodicity=='NONE':
        print('The box should be cubic for non-periodic calculations and the box must be around 15 times the size of the molecule')

    mySim.MOTION.PRINT.STRESS.SECTION_PARAMETERS='OFF'
    mySim.MOTION.PRINT.TRAJECTORY.EACH.MD=traj_freq
    mySim.MOTION.PRINT.TRAJECTORY.FORMAT=traj_type
    mySim.MOTION.PRINT.VELOCITIES.SECTION_PARAMETERS='OFF'
    mySim.MOTION.PRINT.FORCES.SECTION_PARAMETERS="OFF"
    mySim.MOTION.PRINT.RESTART_HISTORY.SECTION_PARAMETERS="ON"
    mySim.MOTION.PRINT.RESTART_HISTORY.EACH.MD=500
    mySim.MOTION.PRINT.RESTART.SECTION_PARAMETERS="ON"
    mySim.MOTION.PRINT.RESTART.BACKUP_COPIES=3

    mySim.MOTION.PRINT.RESTART.EACH.MD=1


    mySim.write_changeLog(fn="md-changeLog.out")
    mySim.write_errorLog()
    mySim.write_inputFile(fn=input_filename)
    print('MD input file saved as {}'.format(input_filename))

