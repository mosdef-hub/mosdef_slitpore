import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.init_project("nvt-1x1x1nm_1-layer")

    # Define temperature
    temperature = 298.0 * u.K

    # Define number of waters in the pore
    nwater = 24

    # Run for 500 M steps
    nsteps_eq = 5000000
    nsteps_prod = 505000000

    # For reproducibility
    np.random.seed(1)

    for run in range(3):
        # Define the state point
        state_point = {
            "T": float(temperature.in_units(u.K).value),
            "nsteps": {
                "equil" : nsteps_eq,
                "prod" : nsteps_prod,
            },
            "run": run,
            "nwater" : nwater,
            "seed1" : np.random.randint(10**8),
            "seed2" : np.random.randint(10**8),
        }

        job = project.open_job(state_point)
        job.init()


if __name__ == "__main__":
    init_project()
