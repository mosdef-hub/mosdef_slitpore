import os
import fileinput
import shutil
from shutil import copy2
from shutil import copytree
import numpy as np


#*********************************************************
# data to change if needed (start)
#*********************************************************

explicit_path_to_GOMC_executable_string = None
# if explicit_path_to_GOMC_executable_string = None, it assumes the you are manually entering the path every time you
#open a new terminal window per the install GOMC section
# Example: for explicit_path_to_GOMC_executable_sting, if you just want to enter the explict path for your computer
# or server just replace the above with the following, and you will be the 'GOMC_CPU_GCMC' executable added to it.
# explicit_path_to_GOMC_executable_string = '/home/brad/Programs/GIT_repositories/Test_Slit_pore_mosdef_build/GOMC/bin'

CPU_or_GPU = 'CPU'   # enter string either CPU or GPU, choose to run on CPU or GPU (this design was intened for CPU)

module_load_command_1 = "module swap gnu7/7.3.0 intel/2019"   #  leave as None if no module loaded, or provided as a string
module_load_command_2 = None    # is  leave as None if no module loaded, or provided as a string
module_load_command_3 = None   # is  None if no module loaded, or provided as a string

constaint_command = " --constraint=intel"   # is None if there is no constraint command for the HPC submission, # or provided as a string

#*********************************************************
# data to change if needed (end)
#*********************************************************

def write_slurm(file_out, task, Ncores,server_run_directory, newdir):
    # SLURM boilerplate

    slurm = "#SBATCH"
    intro = "#!/bin/bash"
    Line_2 = ' --job-name '+str(newdir)
    Line_3 = ' -q primary '
    Line_4 = " -N 1"
    Line_5 = " -n "+str(Ncores)
    Line_6 = " --mem=16G"
    Line_7 = " --constraint=intel"
    Line_8 = ' --mail-type=ALL'
    Line_10 = " -o output_%j.out"
    Line_11 = " -e errors_%j.err"
    Line_12 = " -t 336:0:0"

    Line_13 = 'echo  "Running on host" hostname'
    Line_14 = 'echo  "Time is" date'


    #goto_directory = os.getcwd()
    goto_directory = server_run_directory
    file = open(file_out, 'w')

    file.write(intro+"\n\n")
    file.write(slurm+Line_2+"\n")
    file.write(slurm+Line_3+"\n")
    file.write(slurm+Line_4+"\n")
    file.write(slurm + Line_5 + "\n")
    file.write(slurm + Line_6 + "\n")

    if constaint_command != None and isinstance(constaint_command, str):
        file.write(slurm+constaint_command + "\n")

    file.write(slurm+Line_8 + "\n")
    file.write(slurm+Line_10 + "\n")
    file.write(slurm+Line_11 + "\n")
    file.write(slurm + Line_12 + "\n\n")
    file.write(Line_13 + "\n")
    file.write(Line_14 + "\n\n")

    if module_load_command_1 != None and isinstance(module_load_command_1,str):
        file.write(module_load_command_1 + "\n")
    if module_load_command_2 != None and isinstance(module_load_command_2, str):
        file.write(module_load_command_1 + "\n")
    if module_load_command_3 != None and isinstance(module_load_command_3, str):
        file.write(module_load_command_1 + "\n")

    file.write("\n\n")
    file.write("cd " + goto_directory + "\n\n")
    file.write(task+"\n")
    file.close()
    return


if isinstance(CPU_or_GPU, str):
    if CPU_or_GPU == 'CPU':
        print('GOMC run using CPU')
    elif CPU_or_GPU == 'GPU':
        print('GOMC run using GPU')
    else:
        print("Error: neither 'CPU' or 'GPU' was selected for the CPU_or_GPU variable")
else:
    print("Error: neither 'CPU' or 'GPU' was selected for the CPU_or_GPU variable")



executable_file_part_1 =  'GOMC_'    # this can be changed to GPU if the user wants to run the GPU code
executable_file_part_2 =  '_NVT'    # this can be changed to GPU if the user wants to run the GPU code
executable_file = executable_file_part_1 + CPU_or_GPU + executable_file_part_2


if explicit_path_to_GOMC_executable_string != None :
    if isinstance(explicit_path_to_GOMC_executable_string,str):
        if explicit_path_to_GOMC_executable_string[-1] == '/':
            length = len(explicit_path_to_GOMC_executable_string)-1
            explicit_path_to_GOMC_executable_string = explicit_path_to_GOMC_executable_string[0:length] + executable_file

        else:

            prog = explicit_path_to_GOMC_executable_string + '/' + executable_file
    else:
        print('ERROR: the explicit_path_to_GOMC_executable_string variable is not a string')

else:
    prog = executable_file

goto_directory = os.getcwd()
server_run_directory = goto_directory



job_name='wp_NVT_20'
parameters='../../NVT_build/GOMC_pore_water_FF.inp'
outputname = 'SPCE_PORE_NVT_20'
RSF='false'
#init_pdb=[" ", " "]
#psf_file=[" ", " "]
cell_basis_vectors=[29.472,   29.777,   60.0]
CBV2=60
resname = ['H2O','h2o','TOP', 'BOT']
runs = [1, 2, 3, 4, 5]
temp = [298, 298, 298, 298, 298]
phase=  ['l', 'l', 'l', 'l', 'l']
restart=[0, 0, 0, 0, 0]

Ensemble_type = 'NVT'  # 'ads' or 'des'
#restart=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

# read input file template and do find/replace
nruns = len(runs)
for irun in range(0, nruns):
    # build input file from template
    file_in = open('input/in.conf', 'r')
    filedata = file_in.read()
    file_in.close()
    newdir = '1r'+str(runs[irun])
    os.makedirs(newdir,exist_ok=True)
    #copy2(prog,newdir)
    print("Run number: ",runs[irun]," Phase: ", phase[irun], "Restart: ",restart[irun], "Temp: ",temp[irun])
    if restart[irun] == 0:
        RSF='False'
        if Ensemble_type == 'NVT' :
	        pdb_name = ['../../NVT_build/filled_pore_water_3x3x2.0nm_3-layer.pdb', '../../NVT_build/filled_pore_water_3x3x2.0nm_3-layer.pdb']
	        psf_name = ['../../NVT_build/filled_pore_water_3x3x2.0nm_3-layer.psf', '../../NVT_build/filled_pore_water_3x3x2.0nm_3-layer.psf']
        else:
            print('pick Ensemble_type= NVT')

    elif restart[irun] == 1:
        RSF='True'
        pdb_name = ['../../Restart_files/'+newdir+'/SPCE_PORE_NVT_20_BOX_0_restart.pdb', '../../Restart_files/'+newdir+'/SPCE_PORE_NVT_20_BOX_0_restart.pdb']
        psf_name = ['../../Restart_files/'+newdir+'/SPCE_PORE_NVT_20_merged.psf', '../../Restart_files/'+newdir+'/SPCE_PORE_NVT_20_merged.psf']

    
    os.chdir(newdir)
    if phase[irun] == 'v':
        runsteps=150000000
        equilsteps=5000000
    elif phase[irun] == 'l':
        runsteps=110000000  # 20M to stabilize 40M to analyze
        equilsteps=10000000
    elif phase[irun] == 'b':
        runsteps = 100000000
        equilsteps = 5000000

    f2 = open('in.conf', 'w')
    newdata = filedata.replace("TTT", str(temp[irun]))
    newdata = newdata.replace("PARMFILE", parameters)

    newdata = newdata.replace("INITPDB_0", pdb_name[0])
    newdata = newdata.replace("INITPDB_1", pdb_name[1])
    newdata = newdata.replace("PSF_0", psf_name[0])
    newdata = newdata.replace("PSF_1", psf_name[1])

    newdata = newdata.replace("RESNAME1", resname[0])
    newdata = newdata.replace("RESNAME2", resname[1])
    newdata = newdata.replace("RESNAME3", resname[2])
    newdata = newdata.replace("RESNAME4", resname[3])


    newdata = newdata.replace("RSS", str(runsteps))
    newdata = newdata.replace("ESS", str(equilsteps))

    if phase[irun] == 'v':
        newdata = newdata.replace("CBF", str(3))
        newdata = newdata.replace("CBN", str(2))
    else:
        newdata = newdata.replace("CBF", str(12))
        newdata = newdata.replace("CBN", str(10))
    newdata = newdata.replace("RUNN", str(runs[irun]))
    newdata = newdata.replace("CBV1", str(cell_basis_vectors[0]))
    newdata = newdata.replace("CBV2", str(cell_basis_vectors[1]))
    newdata = newdata.replace("CBV3", str(cell_basis_vectors[2]))
    newdata = newdata.replace("LLL", str(CBV2))

    newdata = newdata.replace("OUTFILE", outputname)
    
    newdata = newdata.replace("RSF", RSF)

    f2.write(newdata)
    f2.close()

    if phase[irun] == 'v':
        task = prog+' +p1 in.conf > out'+str(runs[irun])+'a.dat'
        Ncores= 1
    elif phase[irun] == 'l':
        task =  prog + ' +p12 in.conf > out'+str(runs[irun])+'a.dat'
        Ncores = 12
    elif phase[irun] == 'b':
        task =  prog + ' +p2 in.conf > out' + str(runs[irun]) + 'a.dat'
        Ncores = 2
    # write slurm script
    file_sim = job_name+'_'+str(irun+1)+'.sh'
    server_run_directory_print = server_run_directory +'/'+ str(newdir)
    write_slurm(file_sim, task, Ncores, server_run_directory_print, newdir)
    os.chdir('..')










