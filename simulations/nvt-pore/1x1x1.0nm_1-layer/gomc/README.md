
## Instructions to build and run the GOMC 1x1x1.0nm pore nvt-pore simulations: 

###  GOMC nvt-pore runs in the 1x1x1.0nm graphen pore
The GOMC simulations in this folder simulate water in the 1x1x1.0nm graphene pore. The instructions recreating these simulations are provided below.

Note: These simulations require setup simulations to gather all the data needed to select the correct number of waters.  The number of water molecules is derived from the bulk-waters simulations and the adsorption simulations.  The number of water molecules was determined from these simulations when the water vapor pressures divided by water's saturation pressure equals 1.6 (P/Psat =1.6).  However, the calculated number of water molecules is included in the system build files, so the user can run these simulations without running the setup simulations.  If the user wants to run and calculate the number of water themselves, they can, and they will need to modify the build files accordingly.

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to the NVT_build directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/nvt-pore/1x1x1.0nm_1-layer/gomc/NVT_build). Assuming you are in the nvt-pore gomc directory (mosdef_slitpore/mosdef_slitpore/simulations/nvt-pore/1x1x1.0nm_1-layer/gomc).
* cd NVT_build

2) Run the python build script
* python NVT_build_pore_1x1x1.0nm_1-layer.py


### Step 3 : create the GOMC configuration files (.conf, and Slurm submission script (if needed))
Note: The process is detailed for set1 below, which is the only set for these simulations. 

1) Change the terminal window directory to the set1 directory (i.e., to  mosdef_slitpore/mosdef_slitpore/simulations/nvt-pore/1x1x1.0nm_1-layer/gomc/set1). 
* cd ../set1

2) Obtaining the explicit path, "full_path_to_GOMC_bin_folder".  See the Additional Information Section, Process #2 below.  
Note:  For a laptop or Desktop, Process #1 in the Additional Information Section can also be used so the "full_path_to_GOMC_bin_folder" does not need to be specified, but it will need to be done every time you open a terminal window

3) Modify the python script for your system (ONLY if are running this on an HPC using Slurm). If you are using HPC submission script other than Slurm, you will need to make your own HPC submission scripts. 
Open the python file simbuild.py and change the following variables as needed.
Note: For the examples below, the quotes ("") in the "full_path_to_GOMC_bin_folder" are to specify that it is not the acutal folder name. Therefore, do not enter the quotes ("") in the "full_path_to_GOMC_bin_folder", just enter full_path_to_GOMC_bin_folder
* explicit_path_to_GOMC_executable_string = "full_path_to_GOMC_bin_folder"
* CPU_or_GPU = enter string either CPU or GPU, choose to run on CPU or GPU (this design was intened for CPU)
* module_load_command_1 = Add your HPC specific module command here as a string or set as None
* module_load_command_2 = Add your HPC specific module command here as a string or set as None
* module_load_command_3 = Add your HPC specific module command here as a string or set as None

4) Run the python build script simbuild.py
* python simbuild.py

5) Run the GOMC code.  This will need to be done for each set and the 5 runs per set (1r1, 1r2, 1r3, 1r4, and 1r5).
The instructions below only show the process for set1's 1r1 folder or run.  These instructions are only for running on a laptop or desktop. If you are submitting these runs to an HPC system, you will need to use the slurm's bash scripts (example: wp_NVT_10_1.sh), or use your specific HPC system submission format, and follow the HPC systems specific submission process.  
See the Additional Information Section, Process #2, for more information on this GOMC run commands. Also, the HPC submission scripts (example: wp_NVT_10_1.sh) will have the suggested amount of cores to utilized (see the +p2 values). 
* cd 1r1
Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_NVT +p2 in.conf > out.dat     

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_NVT +p2 in.conf  > out.dat     



### Step 4 : Analyze the data
Change the directory to the analysis folder (mosdef_slitpore/mosdef_slitpore/simulations/nvt-pore/1x1x1.0nm_1-layer/gomc/analysis). This can be done from the last step or from the main folder (mosdef_slitpore/mosdef_slitpore/simulations/nvt-pore/1x1x1.0nm_1-layer/gomc).  The analyis files will be printed in this analysis folder.
Option 1: from the last step
* cd ../../analysis
Option 2: from the main folder
* cd analysis
Run the two (2) python analysis scripts
Note: these python scripts can take alot of memory ~100 to 300 GB, so it is not recommended you run them on a typical laptop or desktop.  
* python Get_No_density_for_all_runs.py
* python Get_order_parameter_s_for_all_runs_test.py







## Additional Information: 

### Process 1 : Obtaining the a temporary path to the GOMC executable file (only works while you have that terminal window open)
How to set a temporary GOMC file path once GOMC is compiled
Note: the below would need to be completed every time you open a new terminal window.
Open a new terminal window and change the directory to the GOMC directory/folder, then run:
* ls ./bin 
Add the GOMC bin folder to our path, so the executable file can be called without the full path infront of it (i.e., by GOMC_CPU_GCMC, GOMC_CPU_GEMC, or GOMC_CPU_NVT)
* LOC_GOMC="$(pwd)/bin" 
* export PATH="${LOC_GOMC}:$PATH"
  

### Process 2 : Obtaining the explicit path, "full_path_to_GOMC_bin_folder", to the GOMC executable using the 'pwd' command, assuming you are already in the GOMC directory.  
Open a new terminal window and change the directory to the GOMC directory/folder, then run:
* cd bin
The output in the terminal window after running the pwd command is the "full_path_to_GOMC_bin_folder" .
* pwd

Note: For the examples below, the quotes ("") in the "full_path_to_GOMC_bin_folder" are to specify that this is not the acutal folder name. Therefore, do not enter the quotes ("") in the "full_path_to_GOMC_bin_folder", just enter full_path_to_GOMC_bin_folder
* Example 1: (GCMC executable path with executable file): "full_path_to_GOMC_bin_folder"/GOMC_CPU_GCMC ;
 
* Example 2: (general GOMC executable path with executable file) : "full_path_to_GOMC_bin_folder"/GOMC_XXX_aaaa

* Example 3: (terminal code to run GOMC with Y cores from the directory containing the in.conf file) :  "full_path_to_GOMC_bin_folder"/GOMC_XXX_aaaa +pY in.conf > out.dat  
