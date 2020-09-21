import unyt as u
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mosdef_cassandra.analysis import ThermoProps
from block_average import block_average


def main():

    # Define conditions
    temperature = 298.0 * u.K
    # Define a range of (shifted) chemical potentials
    mus_vap = np.arange(-60, -36, 3) * u.Unit("kJ/mol")

    press_vap = []
    press_vap_unc = []
    dens_vap = []
    for mu in mus_vap:
        dirname = f"pure_vap_T_{temperature:0.1f}_mu_{mu:.1f}".replace(
            " ", "_"
        ).replace("/", "-")
        dirname = "../" + dirname
        thermo = ThermoProps(dirname + "/prod.out.prp")
        (means_est, vars_est, vars_err) = block_average(
            thermo.prop("Pressure")
        )
        press_vap.append(thermo.prop("Pressure").mean())
        press_vap_unc.append(np.max(np.sqrt(vars_est)) * u.bar)
        dens_vap.append(
            thermo.prop("Nmols").mean() / thermo.prop("Volume").mean()
        )

        fig, ax = plt.subplots()
        ax.errorbar(
            np.arange(len(vars_est)), vars_est, yerr=vars_err,
        )
        ax.set_xlabel("Number of blocking operations")
        ax.set_ylabel("Variance, bar")
        fig.savefig(f"blkavg_mu_{mu.value}.png")

    press_vap = u.unyt_array(press_vap)
    press_vap_unc = u.unyt_array(press_vap_unc)
    dens_vap = u.unyt_array(dens_vap)

    df = pd.DataFrame(
        columns=["mu-cassandra_kJmol", "press_bar", "press-stdev_bar"]
    )
    df["mu-cassandra_kJmol"] = mus_vap.to_value("kJ/mol")
    df["press_bar"] = press_vap.to_value("bar")
    df["press-stdev_bar"] = press_vap_unc.to_value("bar")
    df["density_molec-nm^3"] = dens_vap.to_value("1/nm**3")
    df.to_csv("results_nd.csv")


if __name__ == "__main__":
    main()
