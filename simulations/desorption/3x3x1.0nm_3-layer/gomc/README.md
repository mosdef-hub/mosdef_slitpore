## Instructions to build and run the GOMC 3x3x1.0nm pore desorption simulations: 

### GOMC desorption runs in the 3x3x1.0nm pore
The GOMC simulations in this folder simulate water desorption into 3x3x1.0nm pore. The instructions recreating these simulations are provided below. 

Note: These simulations require setup simulations, as simulations need to start with the pores filled at a high pressure divided by the saturation pressure (P/Psat).  These setup simulations are listed as optional since the endpoints from the required setup simulations are provided.  However, the instructions for the two (2) setup simulations are provided as optional simulations for the user. The simulations for desorption are as follows:
* Part 1 (optional): Simulations to determine the number of waters in the graphene pore at a high chemical potential (see the setup_high_P_div_Po directory).
* Part 2 (optional): Stabilizing the determined the number of waters in the graphene pore from Part 1 via NVT simulations (see the setup_run_NVT directory).
* Part 3 : Desorption simulations starting from a high number of waters in the graphene pore (i.e.,  starting from the end of Part 2's simulations)).  



## Part 1 (optional): Simulations to determine the number of waters in the graphene pore at a high chemical potential (see the setup_high_P_div_Po directory).
Note: This simulation's data uses the average number of waters in the graphene pore for Part 2.  
Note: Part 2 can be simulated without simulating Part 1.

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to the build_ads_system directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/build_ads_system).  Assuming you are in the adsorptoin gomc directory (mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc).
* cd build_reservior

2) Run the python build script
* python build_Graphene_water.py


### Step 3 : Run the simulation from the configuration file (Slurm submission script not available )
1) Change the terminal window directory to the u_n_3769 directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/setup_high_P_div_Po/u_n_3769).  This is assuming that you are currently in the build_reservior directory (i.e., mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/build_reservior)
* cd ../setup_high_P_div_Po/u_n_3769

2) Run the GOMC code.  There is only 1 simulation to run, which is used as the starting point for the 3x3x1.0nm_3-layer desorption simulations.
See the Additional Information Section, Process #2, for more information on this GOMC run commands and how to obtain the "full_path_to_GOMC_bin_folder" path. If available, use 2 to 8 cores (i.e., +p2 to +p8) for these simulations.
* cd 1r1
Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_GCMC +p1 slit_water_GCMC.conf > out.dat     

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_GCMC +p1 slit_water_GCMC.conf  > out.dat     


### Step 4 : Analyze the data
There is no built-in analysis code. However, to get an answer, the user can analyze the total number of waters in the Blk_Output_data_BOX_0.dat file, generated in the same directory as the slit_water_GCMC.conf file (see Step 3).





## Part 2 (optional): Stabilizing the determined the number of waters in the graphene pore from Part 1 via NVT simulations (see the setup_run_NVT directory).
Note: This simulation stabilizes the number of waters in the graphene pore, determined in Part 1.  The stabilization is done by building a new single simulation box and running an NVT simulation.  The endpoint of this NVT simulation is used as a starting point for Part 3.
Note: Part 3 can be simulated without simulating Part 1 and/or 2.

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to the NVT_build directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/setup_run_NVT/NVT_build).  Assuming you are in the main desorption gomc directory (mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc).
* cd setup_run_NVT/NVT_build

2) Run the python build script
* python build_NVT_pore_3x3x1.0nm_3-layer.py


### Step 3 : Run the simulations from the configuration files (Slurm submission script not available )
1) Change the terminal window directory to the setup_run_NVT directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/setup_run_NVT).  This is assuming that you are currently in the NVT_build directory (i.e., mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/setup_run_NVT/NVT_build)
* cd ../

2) Run the GOMC code.  There is only 1 simulation to run, which is used as the starting point for the 3x3x1.0nm_3-layer desorption simulations.
See the Additional Information Section, Process #2, for more information on this GOMC run commands and how to obtain the "full_path_to_GOMC_bin_folder" path. If available, use 2 to 8 cores (i.e., +p2 to +p8) for these simulations.

Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_NVT +p2 slit_water_NVT.conf > out.dat     

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_NVT +p2 slit_water_NVT.conf  > out.dat     


### Step 4 : Analyze the data
There is no analysis for this NVT simulation, as it is just a starting point for simulations in Part 3. 






## Part 3: Desorption simulations starting from a high number of waters in the graphene pore (i.e., starting the end of Part 2's simulations)

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to the build_reservior directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/build_reservior).  Assuming you are in the main desorption gomc directory (mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc).
* cd build_reservior

2) Run the python build script
* python build_Graphene_water.py


### Step 3 : create the GOMC configuration files (.conf, and Slurm submission script (if needed))
Note: The process is detailed for set 1 below.  The process will need to be repeated for set 2, set 3, set 4, and set 5. This is done by replacing set1 with set2, set3, set4, or set5.

1) Change the terminal window directory to the set1 directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/set1).
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

5) Run the GOMC code.  This will need to be done for each set and the 8 runs per set (1r1, 1r2, 1r3, 1r4, 1r5, 1r6, 1r7, and 1r8).
The instructions below only show the process for set1's 1r1 folder or run.  These instructions are only for running on a laptop or desktop. If you are submitting these runs to an HPC system, you will need to use the slurm's bash scripts (example: wp_10_1.sh), or use your specific HPC system submission format, and follow the HPC systems specific submission process.  
See the Additional Information Section, Process #2, for more information on this GOMC run commands. Also, the HPC submission scripts (example: wp_10_1.sh) will have the suggested amount of cores to utilized (see the +p2 values). 
* cd 1r1
Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_GCMC +p2 in.conf > out.dat     

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_GCMC +p2 in.conf  > out.dat     


### Step 4 : Analyze the data
Change the directory to the analysis folder (mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc/analysis). This can be done from the last step or from the main folder (mosdef_slitpore/mosdef_slitpore/simulations/desorption/3x3x1.0nm_3-layer/gomc).  The analyis files will be printed in this analysis folder.
Option 1: from the last step
* cd ../../analysis
Option 2: from the main folder
* cd analysis
Run the python analysis script
* python Data_analysis.py





## Additional Information: 

### 
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
