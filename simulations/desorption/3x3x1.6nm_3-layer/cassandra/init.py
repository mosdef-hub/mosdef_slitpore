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
        -57.0 * u.kJ / u.mol,
        -53.0 * u.kJ / u.mol,
        -52.0 * u.kJ / u.mol,
        -51.0 * u.kJ / u.mol,
        -50.0 * u.kJ / u.mol,
        -49.0 * u.kJ / u.mol,
        -48.0 * u.kJ / u.mol,
        -45.0 * u.kJ / u.mol,
    ]

    # Run for 300 M steps
    nsteps_nvt = 5000000
    nsteps_gcmc = 300000000

    # Start with 400 waters in pore
    nwater = 400

    # For reproducibility
    np.random.seed(5048279)

    for mu in mus:
        for run in range(3):
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
