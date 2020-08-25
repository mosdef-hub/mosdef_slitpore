import signac
import numpy as np
import unyt as u

def init_project():

    # Initialize project
    project = signac.init_project("gromacs_nvt3x3x1-6nm_3-layer")

    # Define temperature
    temperature = 298.0 * u.K

    # Start with a few different number of waters in the pore
    nwaters = [485, 490, 495, 500]

    for nwater in nwaters:
        # Define the state point
        state_point = {
            "T": float(temperature.in_units(u.K).value),
            "nwater": nwater,
        }

        job = project.open_job(state_point)
        job.init()


if __name__ == "__main__":
    init_project()
