import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from matplotlib.ticker import MultipleLocator

from matplotlib import rcParams
rcParams['font.sans-serif'] = 'Arial'
rcParams['font.family'] = 'sans-serif'

def get_color(engine):
    color_dict = {
            'Cassandra': '#1f77b4',
            'GOMC': '#ff7f0e',
            'GROMACS': '#2ca02c',
            'LAMMPS': '#d62728',
            }

    return color_dict[engine]

def main():

    #seaborn.set_palette("dark")
    ow_gmx = np.genfromtxt("results_gmx_ow_density.txt", skip_header=1)
    hw_gmx = np.genfromtxt("results_gmx_hw_density.txt", skip_header=1)
    s_gmx = np.genfromtxt("results_gmx_s.txt", skip_header=1)

    ow_lmp = np.genfromtxt("results_lmp_ow_density.txt", skip_header=1)
    hw_lmp = np.genfromtxt("results_lmp_hw_density.txt", skip_header=1)
    s_lmp = np.genfromtxt("results_lmp_s.txt", skip_header=1)

    ow_gomc = pd.read_csv("results_gomc_ow_density.csv", index_col=0)
    hw_gomc = pd.read_csv("results_gomc_hw_density.csv", index_col=0)
    s_gomc = pd.read_csv("results_gomc_s.csv", index_col=0)

    all_cass = pd.read_csv("results_cass_485-water.csv")

    fig, axes = plt.subplots(1, 3, figsize=(15,5))
    # Plot OW
    ax = axes[0]
    ax.text(0.05, 0.90, 'a)', transform=ax.transAxes,
            size=20, weight='bold')
    ax.plot(
        all_cass["z-loc_nm"],
        all_cass["density-ow_nm^-3_mean"],
        label="Cassandra",
        linewidth=3,
        alpha=0.85,
        color=get_color("Cassandra"),
    )
    ax.fill_between(
        all_cass["z-loc_nm"],
        all_cass["density-ow_nm^-3_mean"] - all_cass["density-ow_nm^-3_std"],
        all_cass["density-ow_nm^-3_mean"] + all_cass["density-ow_nm^-3_std"],
        alpha=0.3,
    ) 
    ax.plot(
        ow_gomc["distance_nm"],
        ow_gomc["Avg_No_density_per_nm_sq"],
        '--',
        dashes=(4,3),
        label="GOMC",
        linewidth=3,
        alpha=0.85,
        color=get_color("GOMC"),
    )
    ax.fill_between(
        ow_gomc["distance_nm"],
        ow_gomc["Avg_No_density_per_nm_sq"] - ow_gomc["StdDev_No_density_per_nm_sq"],
        ow_gomc["Avg_No_density_per_nm_sq"] + ow_gomc["StdDev_No_density_per_nm_sq"],
        alpha=0.3
    )
    ax.plot(
        ow_gmx[:,0],
        ow_gmx[:,1],
        ':',
        dashes=(1,2),
        label="GROMACS",
        linewidth=3,
        alpha=0.85,
        color=get_color("GROMACS"),
    )
    ax.fill_between(
        ow_gmx[:,0],
        ow_gmx[:,1] - ow_gmx[:,2],
        ow_gmx[:,1] + ow_gmx[:,2],
        alpha=0.3,
    )
    ax.plot(
        ow_lmp[:,0],
        ow_lmp[:,1],
        ':',
        dashes=(1,2),
        label="LAMMPS",
        linewidth=3,
        alpha=0.85,
        color=get_color("LAMMPS"),
    )
    ax.fill_between(
        ow_lmp[:,0],
        ow_lmp[:,1] - ow_lmp[:,2],
        ow_lmp[:,1] + ow_lmp[:,2],
        alpha=0.3,
    )

    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-2, 180)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(40))
    ax.yaxis.set_minor_locator(MultipleLocator(20))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    # Plot HW
    ax = axes[1]
    ax.text(0.05, 0.90, 'b)', transform=ax.transAxes,
            size=20, weight='bold')
    ax.plot(
        all_cass["z-loc_nm"],
        all_cass["density-hw_nm^-3_mean"],
        linewidth=3,
        alpha=0.85,
        color=get_color("Cassandra"),
    )
    ax.fill_between(
        all_cass["z-loc_nm"],
        all_cass["density-hw_nm^-3_mean"] - all_cass["density-hw_nm^-3_std"],
        all_cass["density-hw_nm^-3_mean"] + all_cass["density-hw_nm^-3_std"],
        alpha=0.3,
    ) 
    ax.plot(
        hw_gomc["distance_nm"],
        hw_gomc["Avg_No_density_per_nm_sq"],
        '--',
        dashes=(4,3),
        linewidth=3,
        alpha=0.85,
        color=get_color("GOMC"),
    )
    ax.fill_between(
        hw_gomc["distance_nm"],
        hw_gomc["Avg_No_density_per_nm_sq"] - hw_gomc["StdDev_No_density_per_nm_sq"],
        hw_gomc["Avg_No_density_per_nm_sq"] + hw_gomc["StdDev_No_density_per_nm_sq"],
        alpha=0.3
    )
    ax.plot(
        hw_gmx[:,0],
        hw_gmx[:,1],
        ':',
        dashes=(1,2),
        linewidth=3,
        alpha=0.85,
        color=get_color("GROMACS"),
    )
    ax.fill_between(
        hw_gmx[:,0],
        hw_gmx[:,1] - hw_gmx[:,2],
        hw_gmx[:,1] + hw_gmx[:,2],
        alpha=0.3,
    )
    ax.plot(
        hw_lmp[:,0],
        hw_lmp[:,1],
        ':',
        dashes=(1,2),
        linewidth=3,
        alpha=0.85,
        color=get_color("LAMMPS"),
    )
    ax.fill_between(
        hw_lmp[:,0],
        hw_lmp[:,1] - hw_lmp[:,2],
        hw_lmp[:,1] + hw_lmp[:,2],
        alpha=0.3,
    )

    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-2, 180)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(40))
    ax.yaxis.set_minor_locator(MultipleLocator(20))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")
    #ax.text(0.0, 50,'Oxygen', fontsize=20, ha='center')
    #ax.text(0.0, 80,'Hydrogen', fontsize=20, ha='center')

    # Plot S
    ax = axes[2]
    ax.text(0.05, 0.90, 'c)', transform=ax.transAxes,
            size=20, weight='bold')
    ax.plot(
        all_cass["z-loc_nm"],
        all_cass["s_value_mean"],
        label="Cassandra",
        linewidth=3,
        alpha=0.9,
        color=get_color("Cassandra"),
    )
    ax.fill_between(
        all_cass["z-loc_nm"],
        all_cass["s_value_mean"] - all_cass["s_value_std"],
        all_cass["s_value_mean"] + all_cass["s_value_std"],
        alpha=0.3,
    ) 
    ax.plot(
        s_gomc["distance_nm"],
        s_gomc["Avg_order_param"],
        '--',
        dashes=(4,3),
        label="GOMC",
        linewidth=3,
        alpha=0.9,
        color=get_color("GOMC"),
    )
    ax.fill_between(
        s_gomc["distance_nm"],
        s_gomc["Avg_order_param"] - s_gomc["StdDev_order_param"],
        s_gomc["Avg_order_param"] + s_gomc["StdDev_order_param"],
        alpha=0.3
    )
    ax.plot(
        s_gmx[:,0],
        s_gmx[:,1],
        ':',
        dashes=(1,2),
        label="GROMACS",
        linewidth=3,
        alpha=0.9,
        color=get_color("GROMACS"),
    )
    ax.fill_between(
        s_gmx[:,0],
        s_gmx[:,1] - s_gmx[:,2],
        s_gmx[:,1] + s_gmx[:,2],
        alpha=0.3,
    )
    ax.plot(
        s_lmp[:,0],
        s_lmp[:,1],
        ':',
        dashes=(1,2),
        label="LAMMPS",
        linewidth=3,
        alpha=0.9,
        color=get_color("LAMMPS"),
    )
    ax.fill_between(
        s_lmp[:,0],
        s_lmp[:,1] - s_lmp[:,2],
        s_lmp[:,1] + s_lmp[:,2],
        alpha=0.3,
    )

    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{S}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    handles, labels = ax.get_legend_handles_labels()
    lgd = fig.legend(handles, 
            labels,
            bbox_to_anchor=(0.5, 1.07),
            fontsize=16,
            loc='upper center',
            ncol=4)
    fig.tight_layout()
    fig.savefig("2nm_results.pdf", bbox_inches="tight")

if __name__ == "__main__":
    main()

