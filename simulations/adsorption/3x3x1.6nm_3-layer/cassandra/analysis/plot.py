import unyt as u
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress

plt.rc("font", family="serif")


def main():

    data_nd_ads = pd.read_csv("results_nd.csv")
    data_nd_des = pd.read_csv("../../../../desorption/3x3x1.6nm_3-layer/cassandra/analysis/results_nd.csv")
    data_nd_pure = pd.read_csv("../../../../bulk-water/cassandra/analysis/results_nd.csv")

    # Fit a line to mu vs. P
    slope, intercept, r_value, p_value, stderr = linregress(
         data_nd_pure["mu-cassandra_kJmol"].values,
         y=np.log(data_nd_pure["press_bar"].values)
    )

    nd_ads_run = 0
    nd_des_run = 2
    pvap_spce = 0.01 * u.bar

    nd_ads_n = data_nd_ads[data_nd_ads["run"] == nd_ads_run]["nmols_per_nm^2"]
    nd_des_n = data_nd_des[data_nd_des["run"] == nd_des_run]["nmols_per_nm^2"]

    nd_ads_mus = data_nd_ads[data_nd_ads["run"] == nd_ads_run]["mu-cassandra_kJmol"]
    nd_des_mus = data_nd_des[data_nd_des["run"] == nd_des_run]["mu-cassandra_kJmol"]

    nd_ads_press = np.exp(slope * nd_ads_mus + intercept) * u.bar
    nd_des_press = np.exp(slope * nd_des_mus + intercept) * u.bar
    nd_ads_ppvap = nd_ads_press / pvap_spce
    nd_des_ppvap = nd_des_press / pvap_spce

    fig, ax = plt.subplots()
    # Plot ND results
    ax.plot(
        nd_ads_ppvap,
        nd_ads_n,
        marker="s",
        markersize=9,
        c="#0c2340",
        alpha=0.9,
        label="Adsorption",
    )
    ax.plot(
        nd_des_ppvap,
        nd_des_n,
        marker="s",
        markersize=9,
        c="#a9924f",
        alpha=0.9,
        label="Desorption",
    )


    # Plot shifted WS results
    #mass_methane = 16.043 * u.amu
    #temperature = 298.0 * u.K
    #debroglie = u.h / np.sqrt(2 * np.pi * mass_methane * u.kb * temperature)
    #ws_offset = 3 * u.kb * temperature * np.log(debroglie.to_value(u.angstrom))
    #ax.scatter(
    #    mus_ws.to_value("kJ/mol") + ws_offset.to_value("kJ/mol"),
    #    nmols_ws_desktop,
    #    marker="o",
    #    s=50,
    #    c="#406b46",
    #    alpha=0.9,
    #    label="Wayne State Desktop",
    #)
    #ax.scatter(
    #    mus_ws.to_value("kJ/mol") + ws_offset.to_value("kJ/mol"),
    #    nmols_ws_server,
    #    marker="x",
    #    s=50,
    #    c="#f6ca5d",
    #    alpha=0.9,
    #    label="Wayne State Server",
    #)

    ax.set_ylim(-2,30)
    ax.set_xscale("log")
    ax.set_xlabel("P/P$^{sat}$", fontsize=16, labelpad=15)
    ax.set_ylabel("$\\xi$, nm$^{-2}$", fontsize=16, labelpad=15)
    ax.tick_params(axis="both", which="major", labelsize=14)
    ax.legend()

    fig.tight_layout()
    fig.savefig("ads-des.pdf")


if __name__ == "__main__":
    main()
