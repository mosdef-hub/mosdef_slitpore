import signac
import numpy as np
import unyt as u


def init_project():

    # Initialize project
    project = signac.init_project("bulk-water")

    # Define temperature
    temperature = 298.0 * u.K

    # Define chemical potentials
    mus = [
        -66 * u.kJ / u.mol,
        -63 * u.kJ / u.mol,
        -60 * u.kJ / u.mol,
        -57 * u.kJ / u.mol,
        -54 * u.kJ / u.mol,
        -51 * u.kJ / u.mol,
        -48 * u.kJ / u.mol,
        -47 * u.kJ / u.mol,
        -46 * u.kJ / u.mol,
        -45 * u.kJ / u.mol,
        -44 * u.kJ / u.mol,
        -43 * u.kJ / u.mol,
    ]

    # Run for 5 M steps
    nsteps_eq = 1000000
    nsteps_prod = 6000000

    # For reproducibility
    np.random.seed(22)

    for mu in mus:
        # Define the state point
        state_point = {
            "T": float(temperature.in_units(u.K).value),
            "nsteps": {
                "equil" : nsteps_eq,
                "prod" : nsteps_prod,
            },
            "mu": mu.to_value("kJ/mol"),
            "seed1" : np.random.randint(10**8),
            "seed2" : np.random.randint(10**8),
        }

        job = project.open_job(state_point)
        job.init()


if __name__ == "__main__":
    init_project()
