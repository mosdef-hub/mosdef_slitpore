import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rcParams
rcParams['font.family'] = 'serif'

def main():

    df_dict = {
        485 : pd.read_csv("results_nd_485-water.csv", index_col=0),
        490 : pd.read_csv("results_nd_490-water.csv", index_col=0),
        495 : pd.read_csv("results_nd_495-water.csv", index_col=0),
        500 : pd.read_csv("results_nd_500-water.csv", index_col=0),
        505 : pd.read_csv("results_nd_505-water.csv", index_col=0),
    }

    for nwater, df in df_dict.items():
        fig, ax = plt.subplots()
        ax.plot(
            df["z-loc_nm"],
            df[f"density-ow_nm^-3"],
            label="OW",
        )
        ax.plot(
            df["z-loc_nm"],
            df[f"density-hw_nm^-3"],
            label="HW",
        )
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-2, 160)
        ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=18, labelpad=15)
        ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=18, labelpad=15)

        ax.tick_params(axis="both", which="both", direction="in", labelsize=12, pad=6)
        ax.xaxis.set_minor_locator(MultipleLocator(0.05))
        ax.yaxis.set_minor_locator(MultipleLocator(5))
        ax.xaxis.set_ticks_position("both")
        ax.yaxis.set_ticks_position("both")

        fig.legend(loc=(0.45,0.80), fontsize=18)
        fig.tight_layout()
        fig.savefig(f"density-{nwater}.pdf")

    for nwater, df in df_dict.items():
        fig, ax = plt.subplots()
        ax.plot(
            df["z-loc_nm"],
            df[f"s_value"],
        )
        ax.set_xlim(-1.1, 1.1)
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

