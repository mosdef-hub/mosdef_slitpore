## MoSDeF Slitpores
A collection of scripts to run simulations of water inside a carbon slit-pore.  Simulations are run using the following engines:
- [Cassandra](https://cassandra.nd.edu)
- [GROMACS](http://www.gromacs.org)
- [CP2K](https://www.cp2k.org)
- [GOMC](http://gomc.eng.wayne.edu)

### Installation and Requirements
The conda-installable packages are contained within `environment.yml`.
Additionally, the `GOMC` and `CP2K` packages must be installed from source, as
well as the [Pore-Builder](https://github.com/rmatsum836/Pore-Builder) mBuild
recipe. Please see (link to paper) for detailed installation instructions.

### Package Overview
All code to run the simulations are contained within the `simulations` directory.
The naming convention is defined by 1) type of simulation 2) dimensions of the
molecular system and 3) simulation engine used.

The initialization and analysis code, as well as the force field files are
contained within the `mosdef_slitpore` directory.

### Simulation details
* LJ, cutoff, no analytical tail corrections
* 9.0 angstrom cutoffs for LJ and Coulombic interactions
* Long range electrostatics 
