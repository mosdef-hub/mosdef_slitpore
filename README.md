# MoSDeF Slitpores
A collection of Python functions and scripts to run and analyze simulations of water inside carbon slit pores.

## Project Overview
The goal of this project is to replicate the work of Gubbins and colleagues[1] using the Molecular Simulation and Design Framework (MoSDeF)[2,3].  MoSDeF aids in the initialization and parametrization of chemical systems for molecular simulation, and aims to be tightly integrated with the numerous molecular simulation codes available.  Such integration allows for comparisons of simulation results from the various engines in a reproducible manner.  Simulations are run using the following engines.
- [Cassandra](https://cassandra.nd.edu)
- [GROMACS](http://www.gromacs.org)
- [LAMMPS](https://lammps.sandia.gov)
- [CP2K](https://www.cp2k.org)
- [GOMC](http://gomc.eng.wayne.edu)

* Add link to SI.

## Simulation details
* Lennard-Jones (LJ) 12-6 potentials, cutoff, no analytical tail corrections
* 9.0 angstrom cutoffs for LJ and Coulombic interactions
* Long range electrostatics 

## Package Overview
All code to run the simulations are contained within the `simulations` directory.
The naming convention is defined by 1) type of simulation 2) dimensions of the
molecular system and 3) simulation engine used.

The initialization and analysis code, as well as the force field files are
contained within the `mosdef_slitpore` directory.

The simulations run with Cassandra, GROMACS, LAMMPS, and CP2K are managed by the [signac](https://signac.io) framework[4].  There is a specific signac project for each slitpore system and simulation engine.  Each project contains multiple `jobs` with unique `statepoints` which are conditions at which the simulations are run.  Please see signac documentation for additional details.

The data can be visualized with a Jupyter notebook contained in the `notebooks` directory, which calls the plotting functions in the `plotting` directory.

### Installation and Requirements
The conda-installable packages are contained within `environment.yml`.
Additionally, the `GOMC` and `CP2K` packages must be installed from source, as
well as the [Pore-Builder](https://github.com/rmatsum836/Pore-Builder) mBuild
recipe. Please see (link to paper) for detailed installation instructions.

To install this package simply execute the following on the command line: `pip install -e .`

#### Docker Image
The simulations and analysis in this package can also be run with using Docker.  To run the docker image, execute the following command `docker run -it rmatsum/mosdef-slitpore:latest` which will pull the latest docker image from Docker Hub.  Running this image will drop you into a `bash` shell in the container at the location `/workspace`.  In general, containers are intended to be used as an "application", meaning no persistent data should be stored in the container.  If you are in a working directory with necessary input files, such as LAMMPS, you can run `lammps` with the following command:
```
docker run --mount type=bind,source=$(pwd),target=/workspace rmatsum/mosdef-slitpore:latest "lmp_mpi < in.lammps"
```

### Running simulations on a supercomputer or cluster
It is highly advised to run these simulations on a supercomputer or cluster.  For the simulations that
are managed with signac, the submission of job operations can be handled by an
`environment` class.  Please see the signac documentation
[here](https://docs.signac.io/projects/flow/en/latest/supported_environments.html) for a list of
supported environments.

## References
1. Striolo, A.; Chialvo, A. A.; Cummings, P. T.; Gubbins, K. E. Water Adsorption in Carbon-Slit Nanopores. Langmuir, 2003, 19 (20), 8583–8591.
2. Klein, C.; Sallai, J.; Jones, T.; Iacovella, C. R.; McCabe, C.; Cummings, P. T. A Hierarchical, Component Based Approach to Screening Properties of Soft Matter. Foundations of Molecular Modeling and simulation, 2016.
3. Klein, C.; Summers, A. Z; Thompson, M. W.; Gilmer, J. B.; McCabe, C.; Cummings, P. T.; Sallai, J.; Iacovella, C. R. Formalizing Atom-typing and the Dissemination of Force Fields with Foyer. Comput. Mater. Sci., 2019, 167, 215-227.
4. Adorf, C. S.; Dodd, P. M.; Ramasubramani, V.; & Glotzer, S. C. Simple Data and Workflow Management with the Signac Framework. Comput. Mater. Sci., 2018, 146, 220-229.
