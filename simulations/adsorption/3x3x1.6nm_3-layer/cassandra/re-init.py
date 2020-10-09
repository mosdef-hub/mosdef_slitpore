import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.get_project("./")

    # Define temperature
    temperature = 298.0 * u.K
    # Define chemical potentials
    mus = [
        -47.0 * u.kJ / u.mol,
        -46.0 * u.kJ / u.mol,
    ]

    # Run for 300 M steps
    nsteps_gcmc = 300000000

    # For reproducibility
    np.random.seed(594875)

    for mu in mus:
        for run in range(3):
            # Define the state point
            state_point = {
                "T": float(temperature.in_units(u.K).value),
                "mu": float(mu.in_units(u.kJ / u.mol).value),
                "nsteps_gcmc": nsteps_gcmc,
                "seed1" : np.random.randint(10**8),
                "seed2" : np.random.randint(10**8),
                "run": run,
            }

            job = project.open_job(state_point)
            job.init()


if __name__ == "__main__":
    init_project()
