import unyt as u
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rc("font", family="serif")


def main():

    data_nd = pd.read_csv("results_nd.csv")
    fig, ax = plt.subplots()
    ax.errorbar(
        data_nd["mu-cassandra_kJmol"],
        data_nd["press_bar"],
        yerr=[2 * p for p in data_nd["press-stdev_bar"]],
        fmt="s",
        markersize=8,
        color="#0C2340",
        alpha=0.7,
    )
    ax.set_yscale("log")
    ax.set_xlabel("$\mu'$, kJ/mol", fontsize=14, labelpad=15)
    ax.set_ylabel("Pressure, bar", fontsize=14, labelpad=15)
    ax.tick_params(axis="both", which="major", labelsize=12)

    fig.tight_layout()
    fig.savefig("chempot-nd.pdf")

    data_ws = pd.read_csv("results_ws.txt", sep="\s+")
    mus_ws = data_ws["ChemPot_K"].values * u.K * u.kb
    press_ws = data_ws["P_bar"].values * u.bar

    # @300 K, https://www.nist.gov/mml/csd/informatics/sat-tmmc-liquid-vapor-coexistence-properties-spce-water-lrc
    psat_nist = 1.017e-02 * u.bar

    fig, ax = plt.subplots()
    # Plot ND results
    ax.scatter(
        data_nd["mu-cassandra_kJmol"],
        data_nd["press_bar"],
        marker="s",
        s=50,
        c="#0C2340",
        alpha=0.9,
        label="Notre Dame",
    )
    # Plot WS results
    ax.scatter(
        mus_ws.to_value("kJ/mol"),
        press_ws.to_value("bar"),
        marker="o",
        s=50,
        c="#406b46",
        alpha=0.4,
        label="Wayne State reported $\mu$",
    )
    # Plot shifted WS results
    mass_water = 18.015 * u.amu
    temperature = 298.0 * u.K
    debroglie = u.h / np.sqrt(2 * np.pi * mass_water * u.kb * temperature)
    ws_offset = 3 * u.kb * temperature * np.log(debroglie.to_value(u.angstrom))
    ax.scatter(
        mus_ws.to_value("kJ/mol") + ws_offset.to_value("kJ/mol"),
        press_ws.to_value("bar"),
        marker="o",
        s=50,
        c="#406b46",
        alpha=0.9,
        label="Wayne State $\mu + 3RTln(\Lambda)$",
    )

    # Plot NIST Pvap
    ax.axhline(
        psat_nist.to_value("bar"),
        color="black",
        ls="--",
        label="NIST SPC/E $P^{sat}$"
    )
    
    ax.set_yscale("log")
    ax.set_xlabel("$\mu'$, kJ/mol", fontsize=14, labelpad=15)
    ax.set_ylabel("Pressure, bar", fontsize=14, labelpad=15)
    ax.tick_params(axis="both", which="major", labelsize=12)
    ax.legend()

    fig.tight_layout()
    fig.savefig("chempot-compare.pdf")

    mass_density_ws = data_ws["Density_kg_per_mcubed"].values * u.kg / u.m ** 3
    density_ws = mass_density_ws / mass_water

    # @300 K, https://www.nist.gov/mml/csd/informatics/sat-tmmc-liquid-vapor-coexistence-properties-spce-water-lrc
    mass_density_nist = 7.373e-03 * u.kg / u.m ** 3
    density_nist = mass_density_nist / mass_water

    fig, ax = plt.subplots()
    # Plot ND results
    ax.scatter(
        data_nd["mu-cassandra_kJmol"],
        (data_nd["density_molec-nm^3"].values / u.nm ** 3).to_value(
            "mol/dm**3"
        ),
        marker="s",
        s=50,
        c="#0C2340",
        alpha=0.9,
        label="Notre Dame",
    )
    # Plot WS results
    ax.scatter(
        mus_ws.to_value("kJ/mol") + ws_offset.to_value("kJ/mol"),
        density_ws.to_value("mol/dm**3"),
        marker="o",
        s=50,
        c="#406b46",
        alpha=0.9,
        label="Wayne State $\mu + 3RTln(\Lambda)$",
    )
    # Plot NIST SPC/E results
    ax.axhline(
        density_nist.to_value("mol/dm**3"),
        color="black",
        ls="--",
        label=r"NIST SPC/E $\rho^{vap}$",
    )

    ax.set_yscale("log")
    ax.set_xlabel("$\mu'$, kJ/mol", fontsize=14, labelpad=15)
    ax.set_ylabel("Density, mol/dm$^3$", fontsize=14, labelpad=15)
    ax.tick_params(axis="both", which="major", labelsize=12)
    ax.legend()

    fig.tight_layout()
    fig.savefig("density-compare.pdf")


if __name__ == "__main__":
    main()
