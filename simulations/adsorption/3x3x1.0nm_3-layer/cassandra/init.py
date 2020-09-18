import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.init_project("a3x3x1nm_3-layer")

    # Define temperature
    temperature = 298.0 * u.K
    # Define chemical potentials
    mus = [
        -51.0 * u.kJ / u.mol,
        -48.0 * u.kJ / u.mol,
        -47.0 * u.kJ / u.mol,
        -46.0 * u.kJ / u.mol,
        -45.0 * u.kJ / u.mol,
        -44.0 * u.kJ / u.mol,
        -43.0 * u.kJ / u.mol,
        -42.0 * u.kJ / u.mol,
    ]

    # Run for 150 M steps
    nsteps = 150000000

    for mu in mus:
        for run in range(3):
            # Define the state point
            state_point = {
                "T": float(temperature.in_units(u.K).value),
                "mu": float(mu.in_units(u.kJ / u.mol).value),
                "nsteps": nsteps,
                "run": run,
            }

            job = project.open_job(state_point)
            job.init()


if __name__ == "__main__":
    init_project()
