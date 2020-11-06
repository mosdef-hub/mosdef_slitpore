import unyt as u
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from scipy.stats import linregress

plt.rc("font", family="serif")


def main():

    data_nd_ads16 = pd.read_csv("results_nd.csv").sort_values("mu-cassandra_kJmol")
    data_nd_des16 = pd.read_csv("../../../../desorption/3x3x1.6nm_3-layer/cassandra/analysis/results_nd.csv").sort_values("mu-cassandra_kJmol")
    data_nd_ads10 = pd.read_csv("../../../../adsorption/3x3x1.0nm_3-layer/cassandra/analysis/results_nd.csv").sort_values("mu-cassandra_kJmol")
    data_nd_des10 = pd.read_csv("../../../../desorption/3x3x1.0nm_3-layer/cassandra/analysis/results_nd.csv").sort_values("mu-cassandra_kJmol")
    data_nd_pure = pd.read_csv("../../../../bulk-water/cassandra/analysis/results_nd.csv").sort_values("mu-cassandra_kJmol")

    # Fit a line to mu vs. P
    slope, intercept, r_value, p_value, stderr = linregress(
         data_nd_pure["mu-cassandra_kJmol"].values,
         y=np.log(data_nd_pure["press_bar"].values)
    )

    # NIST SPCE 300 K, 1 bar
    pvap_spce = 0.01017 * u.bar

    nd_ads16_n = data_nd_ads16.groupby("mu-cassandra_kJmol").mean()["nmols_per_nm^2"].values
    nd_ads10_n = data_nd_ads10.groupby("mu-cassandra_kJmol").mean()["nmols_per_nm^2"].values
    nd_des16_n = data_nd_des16.groupby("mu-cassandra_kJmol").mean()["nmols_per_nm^2"].values
    nd_des10_n = data_nd_des10.groupby("mu-cassandra_kJmol").mean()["nmols_per_nm^2"].values

    nd_ads16_ppvap = np.exp(slope * data_nd_ads16["mu-cassandra_kJmol"].unique() + intercept) * u.bar / pvap_spce
    nd_des16_ppvap = np.exp(slope * data_nd_des16["mu-cassandra_kJmol"].unique() + intercept) * u.bar / pvap_spce
    nd_ads10_ppvap = np.exp(slope * data_nd_ads10["mu-cassandra_kJmol"].unique() + intercept) * u.bar / pvap_spce
    nd_des10_ppvap = np.exp(slope * data_nd_des10["mu-cassandra_kJmol"].unique() + intercept) * u.bar / pvap_spce


    fig, ax = plt.subplots()
    # Plot ND results
    ax.plot(
        nd_ads16_ppvap,
        nd_ads16_n,
        marker="s",
        markersize=9,
        c="#0c2340",
        alpha=0.9,
        label="Adsorption 16 A",
    )
    ax.plot(
        nd_ads10_ppvap,
        nd_ads10_n,
        "--o",
        markersize=9,
        c="#0c2340",
        alpha=0.9,
        label="Adsorption 10 A",
    )

    ax.plot(
        nd_des16_ppvap,
        nd_des16_n,
        marker="s",
        markersize=9,
        c="#a9924f",
        alpha=0.9,
        label="Desorption 16 A",
    )
    ax.plot(
        nd_des10_ppvap,
        nd_des10_n,
        "--o",
        markersize=9,
        c="#a9924f",
        alpha=0.9,
        label="Desorption 10 A",
    )

    data_ws_ads16 = pd.read_csv("adsorption_16A_gomc.csv")
    data_ws_des16 = pd.read_csv("desorption_16A_gomc.csv")
    data_ws_ads10 = pd.read_csv("adsorption_10A_gomc.csv")
    data_ws_des10 = pd.read_csv("desorption_10A_gomc.csv")

    ax.set_ylim(-2,30)
    ax.set_xscale("log")
    ax.set_xlabel("P/P$^{sat}$", fontsize=16, labelpad=15)
    ax.set_ylabel("$\\xi$, nm$^{-2}$", fontsize=16, labelpad=15)
    ax.tick_params(axis="both", which="major", labelsize=14)
    ax.legend()

    fig.tight_layout()
    fig.savefig("ads-des.pdf")


    # Plot Comparison
    fig, ax = plt.subplots()
    ax.plot(
        nd_ads16_ppvap,
        nd_ads16_n,
        "-o",
        markersize=9,
        c="#0c2340",
        alpha=0.9,
        label="ND Ads 16 $\mathregular{\AA}$",
    )
    ax.plot(
        nd_des16_ppvap,
        nd_des16_n,
        "--o",
        fillstyle="none",
        markersize=9,
        c="#0c2340",
        alpha=0.9,
        label="ND Des 16 $\mathregular{\AA}$",
    )
    ax.plot(
        nd_ads10_ppvap,
        nd_ads10_n,
        "-v",
        markersize=9,
        c="#0c2340",
        alpha=0.9,
        label="ND Ads 10 $\mathregular{\AA}$",
    )
    ax.plot(
        nd_des10_ppvap,
        nd_des10_n,
        "--v",
        fillstyle="none",
        markersize=9,
        c="#0c2340",
        alpha=0.9,
        label="ND Des 10 $\mathregular{\AA}$",
    )

    ax.plot(
        data_ws_ads16["Psat_ratio"],
        data_ws_ads16["Avg_E_No_water_per_nm_sq"],
        "-o",
        markersize=9,
        c="#406b46",
        alpha=0.9,
        label="WS Ads 16 $\mathregular{\AA}$",
    )
    ax.plot(
        data_ws_des16["Psat_ratio"],
        data_ws_des16["Avg_E_No_water_per_nm_sq"],
        "--o",
        markersize=9,
        fillstyle="none",
        c="#406b46",
        alpha=0.9,
        label="WS Des 16 $\mathregular{\AA}$",
    )
    ax.plot(
        data_ws_ads10["Psat_ratio"],
        data_ws_ads10["Avg_E_No_water_per_nm_sq"],
        "-v",
        markersize=9,
        c="#406b46",
        alpha=0.9,
        label="WS Ads 10 $\mathregular{\AA}$",
    )
    ax.plot(
        data_ws_des10["Psat_ratio"],
        data_ws_des10["Avg_E_No_water_per_nm_sq"],
        "--v",
        markersize=9,
        fillstyle="none",
        c="#406b46",
        alpha=0.9,
        label="WS Des 10 $\mathregular{\AA}$",
    )

    ax.set_ylim(-1,30)
    ax.set_xscale("log")
    ax.set_xlabel("P/P$^{sat}$", fontsize=20, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\xi}$, nm$\mathregular{^{-2}}$", fontsize=20, labelpad=15)
    ax.tick_params("both", direction="in", which="both", length=2, labelsize=16)
    ax.tick_params("both", which="major", length=4)
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.legend(fontsize=14)

    fig.tight_layout()
    fig.savefig("ads-des_compare.pdf")



def ppsat(a, a_0, rho_0):
    return (2 * a * a_0**2 + (rho_0-a_0)*a**2) / (rho_0 + a_0)*a_0**2

def activity(mu, debroglie, beta):
    return np.exp(beta * mu) / debroglie**3

def mu_from_mushift(mu_shift, beta):
    q_rot = 43.45
    return mu_shift - (1./beta) * np.log(q_rot)

def debroglie(mass, beta):
    return u.h / np.sqrt(2 * np.pi * mass / beta)

if __name__ == "__main__":
    main()
