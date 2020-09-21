import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.init_project("nvt3x3x1-6nm_3-layer")

    # Define temperature
    temperature = 298.0 * u.K

    # Run for 150 M steps
    nsteps_eq = 5000000
    nsteps_prod = 150000000

    # Start with a few different number of waters in the pore
    nwaters = [485, 490, 495, 500, 505]

    for nwater in nwaters:
        for run in range(3):
            # Define the state point
            state_point = {
                "T": float(temperature.in_units(u.K).value),
                "nwater": nwater,
                "nsteps_eq": nsteps_eq,
                "nsteps_prod": nsteps_prod,
                "run": run,
            }

            job = project.open_job(state_point)
            job.init()


if __name__ == "__main__":
    init_project()
