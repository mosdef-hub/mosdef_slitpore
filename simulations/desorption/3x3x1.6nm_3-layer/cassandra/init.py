import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.init_project("d3x3x1-6nm_3-layer")

    # Define temperature
    temperature = 298.0 * u.K
    # Define chemical potentials
    mus = [
        -63.0 * u.kJ / u.mol,
        -60.0 * u.kJ / u.mol,
        -57.0 * u.kJ / u.mol,
        -54.0 * u.kJ / u.mol,
        -51.0 * u.kJ / u.mol,
        -48.0 * u.kJ / u.mol,
        -45.0 * u.kJ / u.mol,
    ]

    # Run for 150 M steps
    nsteps_eq = 1000000
    nsteps_prod = 150000000

    # Start with 405 waters in pore
    nwater = 405

    for mu in mus:
        for run in range(3):
            # Define the state point
            state_point = {
                "T": float(temperature.in_units(u.K).value),
                "mu": float(mu.in_units(u.kJ / u.mol).value),
                "nwater": nwater,
                "nsteps_eq": nsteps_eq,
                "nsteps_prod": nsteps_prod,
                "run": run,
            }

            job = project.open_job(state_point)
            job.init()


if __name__ == "__main__":
    init_project()