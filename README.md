# MoSDeF Slitpores
A collection of Python functions and scripts to run and analyze simulations of water inside carbon slit pores.

## Project Overview
The goal of this project is to replicate the work of Gubbins and colleagues[1] using the Molecular Simulation and Design Framework (MoSDeF).  MoSDeF aids in the initialization and parametrization of chemical systems for molecular simulation, and aims to be tightly integrated with the numerous molecular simulation codes available.  Such integration allows for comparisons of simulation results from the various engines in a reproducible manner.  Simulations are run using the following engines.
- [Cassandra](https://cassandra.nd.edu)
- [GROMACS](http://www.gromacs.org)
- [LAMMPS](https://lammps.sandia.gov)
- [CP2K](https://www.cp2k.org)
- [GOMC](http://gomc.eng.wayne.edu)

* Add link to SI.

## Simulation details
* LJ, cutoff, no analytical tail corrections
* 9.0 angstrom cutoffs for LJ and Coulombic interactions
* Long range electrostatics 

## Package Overview
All code to run the simulations are contained within the `simulations` directory.
The naming convention is defined by 1) type of simulation 2) dimensions of the
molecular system and 3) simulation engine used.

The initialization and analysis code, as well as the force field files are
contained within the `mosdef_slitpore` directory.

The simulations run with Cassandra, GROMACS, LAMMPS, and CP2K are managed by the [signac](https://signac.io) framework.  There is a specific signac project for each slitpore system and simulation engine.  Each project contains multiple `jobs` with unique `statepoints` which are conditions at which the simulations are run.  Please see signac documentation for additional details.

The data can be visualized with a Jupyter notebook contained in the `notebooks` directory, which calls the plotting functions in the `plotting` directory.

### Installation and Requirements
The conda-installable packages are contained within `environment.yml`.
Additionally, the `GOMC` and `CP2K` packages must be installed from source, as
well as the [Pore-Builder](https://github.com/rmatsum836/Pore-Builder) mBuild
recipe. Please see (link to paper) for detailed installation instructions.

To install this package simply execute the following on the command line: `pip install -e .`



### Running simulations on a supercomputer or cluster
It is highly advised to run these simulations on a supercomputer or cluster.  For the simulations that
are managed with signac, the submission of job operations can be handled by an
`environment` class.  Please see the signac documentation
[here](https://docs.signac.io/projects/flow/en/latest/supported_environments.html) for a list of
supported environments.

## References
1. Striolo, A.; Chialvo, A. A.; Cummings, P. T.; Gubbins, K. E. Water Adsorption in Carbon-Slit Nanopores. Langmuir 2003, 19 (20), 8583–8591.
