import signac
import unyt as u
import numpy as np
import pandas as pd

from mosdef_cassandra.analysis import ThermoProps


def main():

    # Define conditions
    temperature = 298.0 * u.K

    project = signac.get_project("../")

    mus = []
    pressures = []

    for job in project:
        mus.append(job.sp.mu * u.kJ/u.mol)
        thermo = ThermoProps(job.fn("prod.out.prp"))
        pressures.append(thermo.prop("Pressure").mean())

    mus = u.unyt_array(mus)
    pressures = u.unyt_array(pressures)

    df = pd.DataFrame(
        columns=["mu-cassandra_kJmol", "pressure_bar"]
    )
    df["mu-cassandra_kJmol"] = mus.to_value("kJ/mol")
    df["pressure_bar"] = pressures.to_value("bar")
    df.to_csv("results_nd.csv")


if __name__ == "__main__":
    main()
