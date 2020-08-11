## MoSDeF Slitpores
A collection of scripts to run simulations of water inside a carbon slit-pore.  Simulations are run using the following engines:
- [Cassandra](https://cassandra.nd.edu)
- [GROMACS](http://www.gromacs.org)
- [CP2K](https://www.cp2k.org)
- [GOMC](http://gomc.eng.wayne.edu)

### Requirements
- [mBuild](https://github.com/mosdef-hub/mbuild)
- [Foyer](https://github.com/mosdef-hub/foyer)
- [Cassandra](https://cassandra.nd.edu)
- [GROMACS](http://www.gromacs.org)
- [GOMC](http://gomc.eng.wayne.edu)
- [MDTraj](http://mdtraj.org/1.9.3/)
- [MDAnalysis](https://www.mdanalysis.org)
- [Pore-Builder](https://github.com/rmatsum836/Pore-Builder)
- [ramtools](https://github.com/rmatsum836/ramtools)

### Simulation details

* LJ, cutoff, no analytical tail corrections
* 9.0 angstrom cutoffs for LJ and Coulombic interactions
* No long range electrostatics 

### Instructions
All code to run simulations is contained within the `simulations` directory of the repository.  Instructions to run simulations in each software package are detailed below.
#### GOMC

#### Cassandra

#### GROMACS
The MD simulations of the water and graphene slit-pore model are contained within the `gromacs_pore` directory.  The module `build_pore.py` contains the code to initialize the system using mBuild and foyer.  In addition, the appropriate bond constraint information for SPC/E water and GROMACS index files will be generated.  After running `build_pore.py` the necessary files to run the GROMACS simulations will be contained in separate directory that display the number of waters in each system.

The first step is to run a short energy minimization in GROMACS, which will remove any highly-energetic atomic overlaps.  To run energy minimization, type the following commands on the command line:
- `gmx grompp -f ../mdp_files/em.mdp -c init.gro -p init.top -n index.ndx -o em.tpr`
- `gmx mdrun -v -deffnm em`

Once the system has undergone energy minimization, the next step is to run a NVT simulation for 50 ns.  During the analysis steps, the first 5 ns of this simulation trajectory will be discarded as the system is going through equilibration.  It is highly recommended that you run this simulation on a HPC cluster.  On our in-house cluster, this simulation took about 3 hours and 45 minutes to complete.  To run type the following:
- `gmx grompp -f ../mdp_files/nvt.mdp -c em.gro -p init.top -n index.ndx -o nvt.tpr`
- `gmx mdrun -deffnm nvt`

Once your simulation is complete, the system(s) can be analyzed using `analysis.py`.  Within this file, the number density profile of the water within the pore and the `S` order parameter will be calculated using MDTraj and MDAnalysis.  To run simply type: `python analysis.py`
