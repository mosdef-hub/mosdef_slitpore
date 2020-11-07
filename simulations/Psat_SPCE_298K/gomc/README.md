
## Instructions to build and run the GOMC saturation pressure (Psat) simulations for SPC/E water at 298K: 

###  GOMC saturation pressure (Psat) simulations (GEMC-NVT)
The GOMC simulations in this folder simulate the saturation pressure (Psat) of water. The instructions recreating these simulations are provided below.
Note: These simulations do require a liquid water box stabilization step, but are listed as optional since they are already simulated and provided.  These simulations provide the saturation pressure (Psat) of water, which normalizes the data for the rest of the simulations.
* Part 1 (optional) : Create a stabilized water box as a starting point for the GOMC saturation pressure (Psat) simulations
* Part 2 : GOMC saturation pressure (Psat) simulations (GEMC-NVT)



## Part 1 (optional) : Create a stabilized water box as a starting point for the GOMC saturation pressure (Psat) simulations

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to the build_liq_vap_boxes directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc/build_liq_vap_boxes). Assuming you are in the Psat_SPCE_298K gomc directory (mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc).
* cd build_liq_vap_boxes

2) Run the python build script
* python GEMC_NVT_Psat_water_298K.py


### Step 3 : Run the GOMC simulations
Note: There is only 1 simulation to run. 

1) Change the terminal window directory to the set1 directory (i.e., to  mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc/equilb_liq_box/NPT). 
* cd ../equilb_liq_box/NPT

2) Obtaining the explicit path, "full_path_to_GOMC_bin_folder".  See the Additional Information Section, Process #2 below.  
Note:  For a laptop or Desktop, Process #1 in the Additional Information Section can also be used so the "full_path_to_GOMC_bin_folder" does not need to be specified, but it will need to be done every time you open a terminal window

3) Run the GOMC code.  These instructions are only for running on a laptop or desktop. If you are submitting these runs to an HPC system, you will need to provide your own submissions scripts since none are provided. If available, use 2 to 8 cores (i.e., +p2 to +p8) for these simulations.
Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_NPT +p2 liquid_water_NPT.conf > out.dat     

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_NPT +p2 liquid_water_NPT.conf  > out.dat     


### Step 4 : Analyze the data
No analysis is required since this is just an equilibriated starting point for Part 2.



## Part 2 : GOMC saturation pressure (Psat) simulations (GEMC-NVT)

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to the build_liq_vap_boxes directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc/build_liq_vap_boxes). Assuming you are in the Psat_SPCE_298K gomc directory (mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc).
* cd build_liq_vap_boxes

2) Run the python build script
* python GEMC_NVT_Psat_water_298K.py


### Step 3 : Run the GOMC simulations
Note: The process is detailed for set1 below, which is the only set for these simulations.

1) Change the terminal window directory to the set1 directory (i.e., to  mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc/set1/1r1). 
* cd ../set1

2) Obtaining the explicit path, "full_path_to_GOMC_bin_folder".  See the Additional Information Section, Process #2 below.  
Note:  For a laptop or Desktop, Process #1 in the Additional Information Section can also be used so the "full_path_to_GOMC_bin_folder" does not need to be specified, but it will need to be done every time you open a terminal window

3) Run the GOMC code.  This will need to be done for each set and the 5 runs per set (1r1, 1r2, 1r3, 1r4, and 1r5).
The instructions below only show the process for set1's 1r1 folder or run.  These instructions are only for running on a laptop or desktop. If you are submitting these runs to an HPC system, you will need to provide your own submissions scripts since none are provided. If available, use 2 to 8 cores (i.e., +p2 to +p8) for these simulations.
* cd 1r1
Run the code using the CPU:
* "full_path_to_GOMC_bin_folder"/GOMC_CPU_GEMC +p2 water_GEMC_NVT_298K.conf > out.dat     

Alternatively, Run the code using the CPU/GPU:
* "full_path_to_GOMC_bin_folder"/GOMC_GPU_GEMC +p2 water_GEMC_NVT_298K.conf  > out.dat     



### Step 4 : Analyze the data
Change the directory to the analysis folder (mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc/analysis). This can be done from the last step or from the main folder (mosdef_slitpore/mosdef_slitpore/simulations/Psat_SPCE_298K/gomc).  The analyis files will be printed in this analysis folder.
Option 1: from the last step
* cd ../../analysis
Option 2: from the main folder
* cd analysis
Run the two (2) python analysis scripts
* python Data_analysis.py







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
