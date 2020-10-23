import os
import fileinput
import shutil
from shutil import copy2
from shutil import copytree
import numpy as np



def write_slurm(file_out, task, Ncores,server_run_directory, newdir):
    # SLURM boilerplate


    NCPU = Ncores
    NTASK = 2

    slurm = "#SBATCH"
    intro = "#!/bin/bash"
    Line_2 = ' --job-name '+str(newdir)
    Line_3 = ' -q primary '
    Line_4 = " -N 1"
    Line_5 = " -n "+str(Ncores)
    Line_6 = " --mem=16G"
    Line_7 = " --constraint=intel"
    Line_8 = ' --mail-type=ALL'
    Line_9 = ' --mail-user=bc118@wayne.edu'
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
    file.write(slurm+Line_9 + "\n")
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









prog = '/wsu/home/hf/hf68/hf6839/GOMC-2_6-master/bin/GOMC_CPU_NVT'
#prog = '/home/brad/Programs/GOMC/GOMC-2_6-master/bin/GOMC_CPU_GCMC'
server_run_directory = '/wsu/home/hf/hf68/hf6839/Simulations/Graphene_water/Graphene_water_MoSDeF/mosdef_slitpore/simulations/surface/1x1x1.0nm_1-layer/gomc/NVT/set1'
job_name='wp_NVT_10'
parameters='../../NVT_build/GOMC_pore_water_FF.inp'
outputname = 'SPCE_PORE_NVT_10'
RSF='false'
#init_pdb=[" ", " "]
#psf_file=[" ", " "]
cell_basis_vectors=[9.824,   10.635,   20]
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
	        pdb_name = ['../../NVT_build/filled_pore_water_1x1x1.0nm_1-layer.pdb', '../../NVT_build/filled_pore_water_1x1x1.0nm_1-layer.pdb']
	        psf_name = ['../../NVT_build/filled_pore_water_1x1x1.0nm_1-layer.psf', '../../NVT_build/filled_pore_water_1x1x1.0nm_1-layer.psf']
        else:
            print('pick Ensemble_type= NVT')

    elif restart[irun] == 1:
        RSF='True'
        pdb_name = ['../../Restart_files/'+newdir+'/SPCE_PORE_NVT_10_BOX_0_restart.pdb', '../../Restart_files/'+newdir+'/SPCE_PORE_NVT_10_BOX_0_restart.pdb']
        psf_name = ['../../Restart_files/'+newdir+'/SPCE_PORE_NVT_10_merged.psf', '../../Restart_files/'+newdir+'/SPCE_PORE_NVT_10_merged.psf']

    
    os.chdir(newdir)
    if phase[irun] == 'v':
        runsteps=150000000
        equilsteps=5000000
    elif phase[irun] == 'l':
        runsteps=400000000  # 50000000
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
        task =  prog + ' +p4 in.conf > out'+str(runs[irun])+'a.dat'
        Ncores = 4
    elif phase[irun] == 'b':
        task =  prog + ' +p2 in.conf > out' + str(runs[irun]) + 'a.dat'
        Ncores = 2
    # write slurm script
    file_sim = job_name+'_'+str(irun+1)+'.sh'
    server_run_directory_print = server_run_directory +'/'+ str(newdir)
    write_slurm(file_sim, task, Ncores, server_run_directory_print, newdir)
    os.chdir('..')










