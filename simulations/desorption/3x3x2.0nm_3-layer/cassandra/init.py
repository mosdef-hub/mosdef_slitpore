import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.init_project("d3x3x2nm_3-layer")

    # Define temperature
    temperature = 298.0 * u.K
    # Define chemical potentials
    mus = [
        -47.25 * u.kJ/u.mol,
    ]

    # Run for 300 M steps
    nsteps_nvt = 5000000
    nsteps_gcmc = 300000000

    # Start with 500 waters in the pore
    nwater = 500

    # For reproducibility
    np.random.seed(20585)

    for mu in mus:
        for run in range(6):
            # Define the state point
            state_point = {
                "T": float(temperature.in_units(u.K).value),
                "mu": float(mu.in_units(u.kJ / u.mol).value),
                "nwater": nwater,
                "nsteps": {
                    "nvt" : nsteps_nvt,
                    "gcmc" : nsteps_gcmc,
                },
                "seed1" : np.random.randint(10**8),
                "seed2" : np.random.randint(10**8),
                "run": run,
            }

            job = project.open_job(state_point)
            job.init()


if __name__ == "__main__":
    init_project()
