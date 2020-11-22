
## Instructions to build and run the GOMC bulk water simulations: 

### GOMC bulk water simulations
The GOMC simulations in this folder simulate the bulk water properties. These simulations are used determine the pressure divided by the saturation pressure (P/Psat), so the simulation's data can be translated to the experimental data by utilizing the experimental Psat.  The simulations also determine the the chemical potenial vs. pressure in the simulations, and are used to approximate the Striolo data (see reference (1) and the highest_mu_and_rho_for_vap folder).
The instructions for recreating these simulations are provided below. There are 2 parts to these bulk water simulations, which are:
* Part 1: The newly simulated saturation pressure (P/Psat), and chemical potenial vs. pressure data (mu vs. P) -- everything but the Striolo data (see reference (1) and Part 2)
* Part 2: Obtaining the critical data for rescaling of the Striolo data (Optional) -- (see Reference (1) and the highest_mu_and_rho_for_vap folder for the maximum mu before water condenses to a liquid)

Note: These simulations do not require any setup simulations, as the simulations are all started directly.
Note: Part 1's simulation data will be used later for setting up simulations and in their analysis.

## Part 1: The newly simulated saturation pressure (P/Psat), and chemical potenial vs. pressure data (mu vs. P) simulations

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to the build_reservior directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/bulk-water/gomc/build_liq_vap_boxes). Assuming you are in the main bulk-water gomc directory (mosdef_slitpore/simulations/bulk-water/gomc).
* cd build_liq_vap_boxes

2) Run the python build script
* python build_GOMC_water_Pvap_vs_ChemPot.py


### Step 3 : create the GOMC configuration files (.conf, and Slurm submission script (if needed))
Note: The process is detailed for set 1 below.  The process will need to be repeated for set 2, set 3, set 4, and set 5. This is done by replacing set1 with set2, set3, set4, or set5.

1) Change the terminal window directory to the set1 directory (i.e., to mosdef_slitpore/simulations/bulk-water/gomc/set1).
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
The instructions below only show the process for set1's 1r1 folder or run.  These instructions are only for running on a laptop or desktop. If you are submitting these runs to an HPC system, you will need to use the slurm's bash scripts (example: SPCE_Pvap_1.sh), or use your specific HPC system submission format, and follow the HPC systems specific submission process.  
See the Additional Information Section, Process #2, for more information on this GOMC run commands. Also, the HPC submission scripts (example: SPCE_Pvap_1.sh) will have the suggested amount of cores to utilized (see the +p2 values). 
* cd 1r1
Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_GCMC +p2 in.conf > out.dat     

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_GCMC +p2 in.conf  > out.dat     



### Step 4 : Analyze the data
Change the directory to the analysis folder (mosdef_slitpore/mosdef_slitpore/simulations/bulk-water/gomc/analysis). This can be done from the last step or from the main folder (mosdef_slitpore/simulations/bulk-water/gomc).  The analyis files will be printed in this analysis folder.
Option 1: from the last step
* cd ../../analysis
Option 2: from the main folder 
* cd analysis
Run the python analysis script
* python Data_analysis.py
To compare the results of pressure with the ideal gas law run the following plotting script
* python Plot_pure_comp_data.py







## Part 2: Obtaining the critical data for rescaling of the Striolo data (Optional)-- (see Reference (1) and the highest_mu_and_rho_for_vap folder for the maximum mu before water condenses to a liquid)
Note: Part 1's steps 1 and 2 must be completed before Part 2 is started, as Part 2 uses the coordinate, topology, and force field files (PDB, PSF, and FF (.inp)) from Part 1.

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37

### Step 2 : Run the simulations from the configuration files (Slurm submission script not available )
Note: The process is detailed for set1 below, which is the only set in these simulations.

1) Change the terminal window directory to the set1 directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/bulk-water/gomc/highest_mu_and_rho_for_vap/u_n_3889/set1).  This is assuming that you are currently in the main bulk-water gomc directory (i.e., mosdef_slitpore/mosdef_slitpore/simulations/bulk-water/gomc)
* cd highest_mu_and_rho_for_vap/u_n_3889/set1

2) Obtaining the explicit path, "full_path_to_GOMC_bin_folder".  See the Additional Information Section, Process #2 below.  
Note:  For a laptop or Desktop, Process #1 in the Additional Information Section can also be used so the "full_path_to_GOMC_bin_folder" does not need to be specified, but it will need to be done every time you open a terminal window

3) Run the GOMC code.  This will need to be done for each set and the 8 runs per set (1r1, 1r2, 1r3, 1r4, 1r5, 1r6, 1r7, and 1r8).
The instructions below only show the process for set1's 1r1 folder or run.  These instructions are only for running on a laptop or desktop. If you are submitting these runs to an HPC system, you will need to write your own HPC submission scripts with your specific HPC system submission format. 
See the Additional Information Section, Process #2, for more information on this GOMC run commands. 
* cd 1r1
Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_GCMC +p1 water_GCMC.conf > out.dat 

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_GCMC +p1 water_GCMC.conf  > out.dat 

### Step 3 : Analyze the data
Change the directory to the analysis folder (mosdef_slitpore/simulations/bulk-water/gomc/highest_mu_and_rho_for_vap/u_n_3889/analysis). This can be done from the last step or from the main folder (mosdef_slitpore/simulations/bulk-water/gomc)
Option 1: from the last step
* cd ../../analysis
Option 2: from the main folder 
* cd highest_mu_and_rho_for_vap/u_n_3889/analysis
Run the python analysis script
* python Data_analysis.py
To analyze the results of open the SPCE_Rho_o_and_P_o_at_298K_df.csv or SPCE_Rho_o_and_P_o_at_298K_df.txt files, and confirm that the densities are all in the gas phase with a minimal standard devations for the 5 runs. If all simulations are in the gas phase with a minimal standard devations, then the desired result was obtained.  More advanced users can change the chemical potential of water in the .conf files, testing when the chemical potenial is to high and the water condenses.





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



## References:

(1) Striolo A, Chialvo AA, Cummings PT, Gubbins KE. Water adsorption in carbon-slitnanopores. Langmuir. 2003;19(20):8583–8591
