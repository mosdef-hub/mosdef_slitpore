## MoSDeF Slitpores
A collection of scripts to run simulations of water inside a carbon slit-pore.  Simulations are run using the following engines:
- [Cassandra](https://cassandra.nd.edu)
- [GROMACS](http://www.gromacs.org)
- [LAMMPS](https://lammps.sandia.gov)
- [CP2K](https://www.cp2k.org)
- [GOMC](http://gomc.eng.wayne.edu)

### Installation and Requirements
The conda-installable packages are contained within `environment.yml`.
Additionally, the `GOMC` and `CP2K` packages must be installed from source, as
well as the [Pore-Builder](https://github.com/rmatsum836/Pore-Builder) mBuild
recipe. Please see (link to paper) for detailed installation instructions.

To install this package simply execute the following on the command line: `pip install -e .`

### Package Overview
All code to run the simulations are contained within the `simulations` directory.
The naming convention is defined by 1) type of simulation 2) dimensions of the
molecular system and 3) simulation engine used.

The initialization and analysis code, as well as the force field files are
contained within the `mosdef_slitpore` directory.  

### Signac
The simulations run with Cassandra, GROMACS, LAMMPS, and CP2K are managed by the [signac](https://signac.io) framework.  There is a specific signac project for each slitpore system and simulation engine.  Each project contains multiple `jobs` with unique `statepoints` which are conditions at which the simulations are run.  Please see signac documentation for additional details.

### Running simulations on a supercomputer or cluster
It is highly advised to run these simulations on a supercomputer or cluster.  For the simulations that
are managed with signac, the submission of job operations can be handled by an
`environment` class.  Please see the signac documentation
[here](https://docs.signac.io/projects/flow/en/latest/supported_environments.html) for a list of
supported environments.

### Simulation details
* LJ, cutoff, no analytical tail corrections
* 9.0 angstrom cutoffs for LJ and Coulombic interactions
* Long range electrostatics 
