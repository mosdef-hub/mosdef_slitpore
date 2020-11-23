## Plot the adsorption and desorption data for Cassandra, GOMC, and the rescaled Striolo data (see reference 1)

### Plot the adsorption and desorption data for the 3x3x1.0nm and 3x3x1.6nm pores
Note: Both the GOMC and Cassandra analysis output files must be available for the plot to work without modifying the code.  

### Step 1 : Activate the conda environment
1) Open a terminal window and activate the conda environment
* conda activate slitpore37


### Step 2 : build the coordinate, topology, and force field files (PDB, PSF, and FF (.inp))
1) Change the terminal window directory to thePlot_ads_des directory (i.e., to mosdef_slitpore/mosdef_slitpore/simulations/Plot_ads_des).  Assuming you are in the simulations/Plot_ads_des directory (to mosdef_slitpore/mosdef_slitpore/simulations/Plot_ads_des), not action is required.

2) Run the python build script
* python Plot_ads_des_data.py



## References:

(1) Striolo A, Chialvo AA, Cummings PT, Gubbins KE. Water adsorption in carbon-slitnanopores. Langmuir. 2003;19(20):8583–8591
