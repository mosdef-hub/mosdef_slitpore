import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.init_project("nvt-3x3x2nm_3-layer")

    # Define temperature
    temperature = 298.0 * u.K

    # Define number of waters in the pore
    nwater = 485

    # Run for 100 M steps
    nsteps_eq = 5000000
    nsteps_prod = 155000000

    # For reproducibility
    np.random.seed(10)

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
