import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rcParams
rcParams['font.family'] = 'serif'

def main():

    nwater=24
    df = pd.read_csv(f"results_nd_{nwater}-water.csv")

    fig, ax = plt.subplots()
    ax.plot(
        df["z-loc_nm"],
        df[f"density-ow_nm^-3_mean"],
        label="OW",
        linewidth=3,
        alpha=0.85,
    )
    ax.fill_between(
        df["z-loc_nm"],
        df[f"density-ow_nm^-3_mean"] - df[f"density-ow_nm^-3_std"],
        df[f"density-ow_nm^-3_mean"] + df[f"density-ow_nm^-3_std"],
        alpha=0.3,
    )
    ax.plot(
        df["z-loc_nm"],
        df[f"density-hw_nm^-3_mean"],
        label="HW",
        linewidth=3,
        alpha=0.85,
    )
    ax.fill_between(
        df["z-loc_nm"],
        df[f"density-hw_nm^-3_mean"]-df[f"density-hw_nm^-3_std"],
        df[f"density-hw_nm^-3_mean"]+df[f"density-hw_nm^-3_std"],
        alpha=0.3,
    )

    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(0, 250)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=18, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=18, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=12, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    fig.legend(loc=(0.45,0.80), fontsize=18)
    fig.tight_layout()
    fig.savefig(f"density-{nwater}.pdf")

    fig, ax = plt.subplots()
    ax.plot(
        df["z-loc_nm"],
        df[f"s_value_mean"],
        linewidth=3,
        alpha=0.85,
    )
    ax.fill_between(
        df["z-loc_nm"],
        df[f"s_value_mean"]-df[f"s_value_std"],
        df[f"s_value_mean"]+df[f"s_value_std"],
        alpha=0.3,
    )

    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=18, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=18, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=12, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    fig.tight_layout()
    fig.savefig(f"s-{nwater}.pdf")

if __name__ == "__main__":
    main()

