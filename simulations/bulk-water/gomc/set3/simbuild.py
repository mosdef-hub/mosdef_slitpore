import os
import fileinput
import shutil
from shutil import copy2
from shutil import copytree
import numpy as np

explicit_path_to_GOMC_executable_string = None
# if explicit_path_to_GOMC_executable_string = None, it assumes the you are manually entering the path every time you
#open a new terminal window per the install GOMC section
# Example: for explicit_path_to_GOMC_executable_sting, if you just want to enter the explict path for your computer
# or server just replace the above with the following, and you will be the 'GOMC_CPU_GCMC' executable added to it.
# explicit_path_to_GOMC_executable_string = '/home/brad/Programs/GIT_repositories/Test_Slit_pore_mosdef_build/GOMC/bin'

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
    Line_15 = "module swap gnu7/7.3.0 intel/2019"

    #goto_directory = os.getcwd()
    goto_directory = server_run_directory
    file = open(file_out, 'w')

    file.write(intro+"\n\n")
    file.write(slurm+Line_2+"\n")
    file.write(slurm+Line_3+"\n")
    file.write(slurm+Line_4+"\n")
    file.write(slurm + Line_5 + "\n")
    file.write(slurm + Line_6 + "\n")
    file.write(slurm+Line_7 + "\n")
    file.write(slurm+Line_8 + "\n")
    file.write(slurm+Line_10 + "\n")
    file.write(slurm+Line_11 + "\n")
    file.write(slurm + Line_12 + "\n\n")
    file.write(Line_13 + "\n")
    file.write(Line_14 + "\n")
    file.write(Line_15 + "\n\n")
    file.write("cd " + goto_directory + "\n\n")
    file.write(task+"\n")
    file.close()
    return





executable_file =  '/wsu/home/hf/hf68/hf6839/GOMC-2_6-master/bin/GOMC_CPU_GCMC'

if explicit_path_to_GOMC_executable_string != None:
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

#prog = '/home/brad/Programs/GOMC/GOMC-2_6-master/bin/GOMC_CPU_GCMC'
server_run_directory = '/wsu/home/hf/hf68/hf6839/Simulations/Graphene_water/Graphene_water_MoSDeF/mosdef_slitpore/simulations/bulk-water/gomc/set3'

#goto_directory = os.getcwd()
#server_run_directory = goto_directory
job_name='SPCE_Pvap'
parameters='../../build_liq_vap_boxes/Water_Pvap_vs_Chempot.inp'
outputname = 'SPCE_Pvap'
RSF='false'
#init_pdb=[" ", " "]
#psf_file=[" ", " "]

resname = ['H2O','h2o','TOP', 'BOT']
runs = [1, 2, 3, 4, 5, 6, 7, 8]
temp = [298, 298, 298, 298, 298, 298, 298, 298]
phase=  ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v']
restart= [0, 0, 0, 0, 0, 0, 0, 0]
#mus1 =                [-6295, -5934, -5573, -5212, -4852, -4671, -4491, -4446, -4401, -4310, -4130, -4085, -4040, -3995, -3950]
#cubic_box_length_Ang = [5000,  3000,  2000,  1500,  1000,   800,   600,   600,   600,   500,   400,   400,   400,   400,   300]
mus1 =                [-6295,        -5573,        -4852,        -4491,        -4401,        -4130,        -4040,        -3950]
cubic_box_length_Ang = [5000,         2000,         1000,          600,          600,          400,          400,          300]
Rcut_vap             = [ 320,          320,          320,          120,          120,          120,          120,          120]
cubic_box_reservoir_length_Ang = 8000
type_sim = 'vapor_pressure'  # 'vapor_pressure'


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
    print("Run number: ",runs[irun]," Phase: ", phase[irun], "Restart: ",restart[irun], "Temp: ",temp[irun], "Mu_1: ", mus1[irun])
    if restart[irun] == 0:
        RSF='False'
        if type_sim == 'vapor_pressure'  :
	        pdb_name = ['../../build_liq_vap_boxes/Water_boxes_for_test_box_'+str(cubic_box_length_Ang[irun])+'A.pdb', '../../build_liq_vap_boxes/Water_Pvap_vs_Chempot_reservior.pdb']
	        psf_name = ['../../build_liq_vap_boxes/Water_boxes_for_test_box_'+str(cubic_box_length_Ang[irun])+'A.psf', '../../build_liq_vap_boxes/Water_Pvap_vs_Chempot_reservior.psf']
        else:
            print('pick a desorption or adsorption')

    elif restart[irun] == 1:
        RSF='True'
        print('This are quick simulations, so no real need to restart')

    cell_basis_vectors = [cubic_box_length_Ang[irun], cubic_box_length_Ang[irun], cubic_box_length_Ang[irun]]

    os.chdir(newdir)
    if phase[irun] == 'v':
        runsteps=  100000000
        equilsteps= 10000000
    elif phase[irun] == 'l':
        runsteps=  100000000
        equilsteps= 10000000
    elif phase[irun] == 'b':
        runsteps=  100000000
        equilsteps= 10000000

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

    newdata = newdata.replace("CCC1", str(mus1[irun]))

    newdata = newdata.replace("VapCut0", str(Rcut_vap[irun]))
    newdata = newdata.replace("VapCut1", str(Rcut_vap[irun]))

    newdata = newdata.replace("RSS", str(runsteps))
    newdata = newdata.replace("ESS", str(equilsteps))

    if phase[irun] == 'v':
        newdata = newdata.replace("SWPFreq", str(0.6))
        newdata = newdata.replace("RegFreq", str(0.1))
    else:

        newdata = newdata.replace("SWPFreq", str(0.6))
        newdata = newdata.replace("RegFreq", str(0.1))

    if phase[irun] == 'v':
        newdata = newdata.replace("CBF", str(16))
        newdata = newdata.replace("CBN", str(8))
    else:
        newdata = newdata.replace("CBF", str(16))
        newdata = newdata.replace("CBN", str(8))

    newdata = newdata.replace("RUNN", str(runs[irun]))
    newdata = newdata.replace("CBV1", str(cell_basis_vectors[0]))
    newdata = newdata.replace("CBV2", str(cell_basis_vectors[1]))
    newdata = newdata.replace("CBV3", str(cell_basis_vectors[2]))
    newdata = newdata.replace("LLL", str(cubic_box_reservoir_length_Ang))

    newdata = newdata.replace("OUTFILE", outputname)
    
    newdata = newdata.replace("RSF", RSF)

    f2.write(newdata)
    f2.close()

    if phase[irun] == 'v':
        task = prog+' +p1 in.conf > out'+str(runs[irun])+'a.dat'
        Ncores= 1
    elif phase[irun] == 'l':
        task =  prog + ' +p1 in.conf > out'+str(runs[irun])+'a.dat'
        Ncores = 1
    elif phase[irun] == 'b':
        task =  prog + ' +p1 in.conf > out' + str(runs[irun]) + 'a.dat'
        Ncores = 1

    # write slurm script
    file_sim = job_name+'_'+str(irun+1)+'.sh'
    server_run_directory_print = server_run_directory +'/'+ str(newdir)
    write_slurm(file_sim, task, Ncores, server_run_directory_print, newdir)
    os.chdir('..')










