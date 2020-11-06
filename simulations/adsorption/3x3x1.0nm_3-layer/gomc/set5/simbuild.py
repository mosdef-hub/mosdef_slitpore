import os
import fileinput
import shutil
from shutil import copy2
from shutil import copytree
import numpy as np



def write_slurm(file_out, task, Ncores,server_run_directory):
    # SLURM boilerplate


    NCPU = Ncores
    NTASK = 2

    slurm = "#PBS"
    intro = "#!/bin/bash"
    Line_2 = ' -l select=1:ncpus='+str(NCPU)+':mem=16gb:cpu_type=Intel'
    Line_3 = " -j oe"
    Line_4 = " -m aeb"
    Line_5 = " -M bc118@wayne.edu"
    Line_6 = " -r y"

    Line_7 = 'echo  "Running on host" hostname'
    Line_8 = 'echo  "Time is" date'
    Line_9 = "module swap gnu7/7.3.0 intel/2019"
    #goto_directory = os.getcwd()
    goto_directory = server_run_directory
    file = open(file_out, 'w')

    file.write(intro+"\n")
    file.write(slurm+Line_2+"\n")
    file.write(slurm+Line_3+"\n")
    file.write(slurm+Line_4+"\n")
    file.write(slurm + Line_5 + "\n")
    file.write(slurm + Line_6 + "\n\n")
    file.write(Line_7 + "\n")
    file.write(Line_8 + "\n")
    file.write(Line_9 + "\n\n")
    file.write(Line_8 + "\n\n")
    file.write("cd " + goto_directory + "\n\n")
    file.write(task+"\n")
    file.close()
    return









prog = '/wsu/home/hf/hf68/hf6839/GOMC-2_6-master/bin/GOMC_CPU_GCMC'
#prog = '/home/brad/Programs/GOMC/GOMC-2_6-master/bin/GOMC_CPU_GCMC'
server_run_directory = 'Simulations/Graphene_water/Graphene_water_MoSDeF/mosdef_slitpore/simulations/adsorption/3x3x1.0nm_3-layer/gomc/set5'
job_name='wp_10'
parameters='../../../../../gomc_pdb_psf_FF/Grapene_Water_builder/GOMC_pore_fake_water_FF.inp'
outputname = 'SPCE_PORE_10'
RSF='false'
#init_pdb=[" ", " "]
#psf_file=[" ", " "]
cell_basis_vectors=[29.472, 29.777, 26.750]
CBV2=60
resname = ['H2O','h2o','TOP', 'BOT']
runs = [1, 2, 3, 4, 5, 6, 7, 8]
temp = [298, 298, 298, 298, 298, 298, 298, 298]
mus1 = [    -5573,     -5212,    -4852,      -4491, -4370, -4250, -4130, -3769 ]
mus2 = [-10000000, -10000000, -10000000, -10000000, -1500, -1500, -1500, -1000]
mus3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
phase=  ['v', 'v', 'v', 'v', 'b', 'l', 'l', 'l']
restart=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

adsorption_or_desorption = 'ads'  # 'ads' or 'des'
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
    print("Run number: ",runs[irun]," Phase: ", phase[irun], "Restart: ",restart[irun], "Temp: ",temp[irun], "Mu_1: ", mus1[irun], "Mu_2: ", mus2[irun])
    if restart[irun] == 0:
        RSF='False'
        if adsorption_or_desorption == 'ads' :
	        pdb_name = ['../../../../../gomc_pdb_psf_FF/Grapene_Water_builder/pore_3x3x1.0nm_3-layer.pdb', '../../../../../gomc_pdb_psf_FF/Grapene_Water_builder/GOMC_reservior_fake_water_box.pdb']
	        psf_name = ['../../../../../gomc_pdb_psf_FF/Grapene_Water_builder/pore_3x3x1.0nm_3-layer.psf', '../../../../../gomc_pdb_psf_FF/Grapene_Water_builder/GOMC_reservior_fake_water_box.psf']
        elif adsorption_or_desorption == 'des':
	        pdb_name = ['../../../../../NVT/3x3x1.0nm_3-layer/gomc/Output_data_BOX_0_restart.pdb', '../../../../../gomc_pdb_psf_FF/Grapene_Water_builder/GOMC_reservior_fake_water_box.pdb']
	        psf_name = ['../../../../../NVT/3x3x1.0nm_3-layer/gomc/Output_data_merged.psf',        '../../../../../gomc_pdb_psf_FF/Grapene_Water_builder/GOMC_reservior_fake_water_box.psf']
        else:
            print('pick a desorption or adsorption')

    elif restart[irun] == 1:
        RSF='True'
        #pdb_name = ['../../../../NVT/3x3x2.0nm_3-layer/gomc/Output_data_BOX_0_restart.pdb', '../../../../gomc_pdb_psf_FF/Grapene_Water_builder/GOMC_reservior_fake_water_box.pdb']
        #psf_name = ['../../../../NVT/3x3x2.0nm_3-layer/gomc/Output_data_BOX_0_restart.psf', '../../../../gomc_pdb_psf_FF/Grapene_Water_builder/GOMC_reservior_fake_water_box.psf']

    
    os.chdir(newdir)
    if phase[irun] == 'v':
        runsteps=150000000
        equilsteps=5000000
    elif phase[irun] == 'l':
        runsteps=50000000
        equilsteps=5000000
    elif phase[irun] == 'b':
        runsteps = 150000000
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

    newdata = newdata.replace("CCC1", str(mus1[irun]))
    if phase[irun] == 'v':
        newdata = newdata.replace("CCC2", str(-10000000))
    elif phase[irun] == 'l':
        newdata = newdata.replace("CCC2", str(mus2[irun]))
    elif phase[irun] == 'b':
        newdata = newdata.replace("CCC2", str(mus2[irun]))
    newdata = newdata.replace("CCC3", str(mus3[irun]))

    newdata = newdata.replace("RSS", str(runsteps))
    newdata = newdata.replace("ESS", str(equilsteps))

    if phase[irun] == 'v':
        newdata = newdata.replace("SWPFreq", str(0.5))
        newdata = newdata.replace("RegFreq", str(0.2))
        newdata = newdata.replace("MEMC2Freq", str(0.0))
    else:
        newdata = newdata.replace("SWPFreq", str(0.40))
        newdata = newdata.replace("RegFreq", str(0.10))
        newdata = newdata.replace("MEMC2Freq", str(0.20))

    if phase[irun] == 'v':
        newdata = newdata.replace("CBF", str(3))
        newdata = newdata.replace("CBN", str(2))
    elif phase[irun] == 'l':
        newdata = newdata.replace("CBF", str(16))
        newdata = newdata.replace("CBN", str(8))
    elif phase[irun] == 'b':
        newdata = newdata.replace("CBF", str(16))
        newdata = newdata.replace("CBN", str(8))
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
        task =  prog + ' +p4 in.conf > out' + str(runs[irun]) + 'a.dat'
        Ncores = 4
    # write slurm script
    file_sim = job_name+'_'+str(irun+1)+'.txt'
    server_run_directory_print = server_run_directory +'/'+ str(newdir)
    write_slurm(file_sim, task, Ncores, server_run_directory_print)
    os.chdir('..')










