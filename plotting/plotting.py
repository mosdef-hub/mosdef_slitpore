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
            'CP2K': '#9467bd',
            }

    return color_dict[engine]

def get_ls(engine):
    ls_dict = {
            'Cassandra': '-',
            'GOMC': '--',
            'GROMACS': '-.',
            'LAMMPS': ':',
            'CP2K': '--',
            }

    return ls_dict[engine]

def plot_1_water():
    data_path = '../simulations/nvt-pore/1x1x1.0nm_1-layer/'
    gmx_path = 'gromacs/data/'
    #ow_gmx = np.genfromtxt(data_path+gmx_path+"1_mol_o_density.txt", skip_header=1)
    #hw_gmx = np.genfromtxt(data_path+gmx_path+"1_mol_h_density.txt", skip_header=1)
    #s_gmx = np.genfromtxt(data_path+gmx_path+"1_mol_s_order.txt", skip_header=1)
    ow_gmx_sym = np.genfromtxt(data_path+gmx_path+"1_mol_o_density_symmetrize.txt", skip_header=1)
    hw_gmx_sym = np.genfromtxt(data_path+gmx_path+"1_mol_h_density_symmetrize.txt", skip_header=1)
    s_gmx_sym = np.genfromtxt(data_path+gmx_path+"1_mol_s_order_symmetrize.txt", skip_header=1)
    angle_gmx = np.genfromtxt(data_path+gmx_path+"1_mol_angle_dist_normalized.txt", skip_header=1)

    cp2k_path = 'cp2k/data_absz/1water_data/'
    ow_cp2k = np.genfromtxt(data_path+cp2k_path+"o_density.txt", skip_header=1)
    hw_cp2k = np.genfromtxt(data_path+cp2k_path+"h_density.txt", skip_header=1)
    s_cp2k = np.genfromtxt(data_path+cp2k_path+"s_order.txt", skip_header=1)
    cp2k_angle_path = 'cp2k/distribution_data/1water_data/'
    angle_cp2k = np.genfromtxt(data_path+cp2k_angle_path+"angle_dist_normalized.txt", skip_header=1)


    fig, axes = plt.subplots(2, 2, figsize=(9,9))
    # Plot OW
    ax = axes[0][0]
    ax.text(0.05, 0.90, 'a)', transform=ax.transAxes,
            size=20, weight='bold')
    rect = [0.47, 0.7, 0.4, 0.4]
    ax.plot(
        ow_gmx_sym[:,0],
        ow_gmx_sym[:,1],
        linestyle=get_ls("GROMACS"),
        label="GROMACS",
        linewidth=3,
        alpha=0.85,
        color=get_color("GROMACS")
    )
    ax.fill_between(
        ow_gmx_sym[:,0],
        ow_gmx_sym[:,1] - ow_gmx_sym[:,2],
        ow_gmx_sym[:,1] + ow_gmx_sym[:,2],
        alpha=0.3,
        color=get_color("GROMACS")
    )
    ax.plot(
        ow_cp2k[:,0],
        ow_cp2k[:,1],
        linestyle=get_ls("CP2K"),
        dashes=(1,1),
        label="CP2K",
        linewidth=3,
        alpha=0.85,
        color=get_color("CP2K")
    )
    ax.fill_between(
        ow_cp2k[:,0],
        ow_cp2k[:,1] - ow_cp2k[:,2],
        ow_cp2k[:,1] + ow_cp2k[:,2],
        alpha=0.3,
        color=get_color("CP2K")
    )

    ax.set_xlim(0.00, 0.5)
    ax.set_ylim(-1, 12)
    ax.set_xlabel(r"$\mathregular{\vert z \vert, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(\vert z \vert), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(3))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")


    # Plot HW
    ax = axes[0][1]
    ax.text(0.05, 0.90, 'b)', transform=ax.transAxes,
            size=20, weight='bold')
    ax.plot(
        hw_gmx_sym[:,0],
        hw_gmx_sym[:,1],
        linestyle=get_ls("GROMACS"),
        linewidth=3,
        alpha=0.85,
        label="GROMACS",
        color=get_color("GROMACS")
    )
    ax.fill_between(
        hw_gmx_sym[:,0],
        hw_gmx_sym[:,1] - hw_gmx_sym[:,2],
        hw_gmx_sym[:,1] + hw_gmx_sym[:,2],
        alpha=0.3,
        color=get_color("GROMACS")
    )
    ax.plot(
        hw_cp2k[:,0],
        hw_cp2k[:,1],
        linestyle=get_ls("CP2K"),
        dashes=(1,1),
        label="CP2K",
        linewidth=3,
        alpha=0.85,
        color=get_color("CP2K")
    )
    ax.fill_between(
        hw_cp2k[:,0],
        hw_cp2k[:,1] - hw_cp2k[:,2],
        hw_cp2k[:,1] + hw_cp2k[:,2],
        alpha=0.3,
        color=get_color("CP2K")
    )

    ax.set_xlim(0.00, 0.5)
    ax.set_ylim(-1, 12)
    ax.set_xlabel(r"$\mathregular{\vert z \vert, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(\vert z \vert), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(3))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    # Plot S
    ax = axes[1][0]
    ax.text(0.05, 0.90, 'c)', transform=ax.transAxes,
            size=20, weight='bold')
    ax.plot(
        s_gmx_sym[:,0],
        s_gmx_sym[:,1],
        linestyle=get_ls("GROMACS"),
        label="GROMACS",
        linewidth=3,
        alpha=0.9,
        color=get_color("GROMACS")
    )
    ax.fill_between(
        s_gmx_sym[:,0],
        s_gmx_sym[:,1] - s_gmx_sym[:,2],
        s_gmx_sym[:,1] + s_gmx_sym[:,2],
        color=get_color("GROMACS"),
        alpha=0.3,
    )
    ax.plot(
        s_cp2k[:,0],
        s_cp2k[:,1],
        linestyle=get_ls("CP2K"),
        dashes=(1,1),
        label="CP2K",
        linewidth=3,
        alpha=0.9,
        color=get_color("CP2K")
    )
    ax.fill_between(
        s_cp2k[:,0],
        s_cp2k[:,1] - s_cp2k[:,2],
        s_cp2k[:,1] + s_cp2k[:,2],
        alpha=0.3,
        color=get_color("CP2K")
    )

    ax.set_xlim(-0.01, 0.25)
    ax.set_ylim(-0.3, 0.3)
    ax.set_xlabel(r"$\mathregular{\vert z \vert, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{S}$", fontsize=22, labelpad=15, style="italic")

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    legend_ax = ax
    ax = axes[1][1]
    ax.text(0.05, 0.90, 'd)', transform=ax.transAxes,
            size=20, weight='bold')
    ax.hist(angle_gmx[:,0],
            bins=len(angle_gmx[:,0]),
            weights=angle_gmx[:,1],
            color=get_color("GROMACS"),
            label="GROMACS",
            align="left",
            alpha=0.4)
    ax.hist(angle_cp2k[:,0],
            bins=len(angle_cp2k[:,0]),
            weights=angle_cp2k[:,1],
            color=get_color("CP2K"),
            label="CP2K",
            align="left",
            alpha=0.4)

    ax.set_ylim((0.0, 0.04))
    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.set_xlabel(r"$\mathregular{Angle\ \theta, \deg}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{Relative Frequency}$", fontsize=22, labelpad=15)
    ax.xaxis.set_minor_locator(MultipleLocator(20))
    ax.xaxis.set_major_locator(MultipleLocator(60))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")


    handles, labels = legend_ax.get_legend_handles_labels()
    lgd = fig.legend(handles, 
            labels,
            bbox_to_anchor=(0.5, 1.08),
            fontsize=16,
            loc='upper center',
            ncol=2)
    fig.tight_layout()
    fig.savefig("1_water_results.pdf", bbox_inches="tight")

def plot_large_2nm():
    data_path = '../simulations/nvt-pore/3x3x2.0nm_3-layer/'
    gmx_path = 'gromacs/data/'
    ow_gmx = np.genfromtxt(data_path+gmx_path+"485_mol_o_density.txt", skip_header=1)
    hw_gmx = np.genfromtxt(data_path+gmx_path+"485_mol_h_density.txt", skip_header=1)
    s_gmx = np.genfromtxt(data_path+gmx_path+"485_mol_s_order.txt", skip_header=1)

    lmp_path = 'lammps/data/'
    ow_lmp = np.genfromtxt(data_path+lmp_path+"485_mol_o_density.txt", skip_header=1)
    hw_lmp = np.genfromtxt(data_path+lmp_path+"485_mol_h_density.txt", skip_header=1)
    s_lmp = np.genfromtxt(data_path+lmp_path+"485_mol_s_order.txt", skip_header=1)

    ow_gomc = pd.read_csv("2nm_gomc/results_gomc_ow_density.csv", index_col=0)
    hw_gomc = pd.read_csv("2nm_gomc/results_gomc_hw_density.csv", index_col=0)
    s_gomc = pd.read_csv("2nm_gomc/results_gomc_s.csv", index_col=0)

    cass_path = 'cassandra/analysis/'
    all_cass = pd.read_csv(data_path+cass_path+"results_485-water.csv")

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
        linestyle=get_ls("Cassandra"),
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
        linestyle=get_ls("GOMC"),
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
        linestyle=get_ls("GROMACS"),
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
        linestyle=get_ls("LAMMPS"),
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
        linestyle=get_ls("Cassandra"),
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
        linestyle=get_ls("GOMC"),
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
        linestyle=get_ls("GROMACS"),
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
        linestyle=get_ls("LAMMPS"),
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
        linestyle=get_ls("Cassandra"),
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
        linestyle=get_ls("GOMC"),
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
        linestyle=get_ls("GROMACS"),
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
        linestyle=get_ls("LAMMPS"),
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
        color=get_color("LAMMPS"),
    )

    ax.set_xlim(-0.75, 0.75)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{S}$", fontsize=22, labelpad=15, style="italic")

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


def plot_small_1nm():
    data_path = '../simulations/nvt-pore/1x1x1.0nm_1-layer/'
    gmx_path = 'gromacs/data/'
    ow_gmx = np.genfromtxt(data_path+gmx_path+"24_mol_o_density.txt", skip_header=1)
    hw_gmx = np.genfromtxt(data_path+gmx_path+"24_mol_h_density.txt", skip_header=1)
    s_gmx = np.genfromtxt(data_path+gmx_path+"24_mol_s_order.txt", skip_header=1)

    lmp_path = 'lammps/data/'
    ow_lmp = np.genfromtxt(data_path+lmp_path+"24_mol_o_density.txt", skip_header=1)
    hw_lmp = np.genfromtxt(data_path+lmp_path+"24_mol_h_density.txt", skip_header=1)
    s_lmp = np.genfromtxt(data_path+lmp_path+"24_mol_s_order.txt", skip_header=1)

    ow_gomc = pd.read_csv("1nm_gomc/results_gomc_ow_density.csv", index_col=0)
    hw_gomc = pd.read_csv("1nm_gomc/results_gomc_hw_density.csv", index_col=0)
    s_gomc = pd.read_csv("1nm_gomc/results_gomc_s.csv", index_col=0)

    cp2k_path = 'cp2k/data/24water_data/'
    ow_cp2k = np.genfromtxt(data_path+cp2k_path+"o_density.txt", skip_header=1)
    hw_cp2k = np.genfromtxt(data_path+cp2k_path+"h_density.txt", skip_header=1)
    s_cp2k = np.genfromtxt(data_path+cp2k_path+"s_order.txt", skip_header=1)

    cass_path = 'cassandra/analysis/'
    all_cass = pd.read_csv(data_path+cass_path+"results_24-water.csv")

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
        linestyle=get_ls("Cassandra"),
    )
    ax.fill_between(
        all_cass["z-loc_nm"],
        all_cass["density-ow_nm^-3_mean"] - all_cass["density-ow_nm^-3_std"],
        all_cass["density-ow_nm^-3_mean"] + all_cass["density-ow_nm^-3_std"],
        alpha=0.3,
        color=get_color("Cassandra")
    ) 
    ax.plot(
        ow_gomc["distance_nm"],
        ow_gomc["Avg_No_density_per_nm_sq"],
        linestyle=get_ls("GOMC"),
        dashes=(4,3),
        label="GOMC",
        linewidth=3,
        alpha=0.85,
        color=get_color("GOMC")
    )
    ax.fill_between(
        ow_gomc["distance_nm"],
        ow_gomc["Avg_No_density_per_nm_sq"] - ow_gomc["StdDev_No_density_per_nm_sq"],
        ow_gomc["Avg_No_density_per_nm_sq"] + ow_gomc["StdDev_No_density_per_nm_sq"],
        alpha=0.3,
        color=get_color("GOMC")
    )
    ax.plot(
        ow_gmx[:,0],
        ow_gmx[:,1],
        linestyle=get_ls("GROMACS"),
        label="GROMACS",
        linewidth=3,
        alpha=0.85,
        color=get_color("GROMACS")
    )
    ax.fill_between(
        ow_gmx[:,0],
        ow_gmx[:,1] - ow_gmx[:,2],
        ow_gmx[:,1] + ow_gmx[:,2],
        alpha=0.3,
        color=get_color("GROMACS")
    )
    ax.plot(
        ow_lmp[:,0],
        ow_lmp[:,1],
        linestyle=get_ls("LAMMPS"),
        dashes=(1,2),
        label="LAMMPS",
        linewidth=3,
        alpha=0.85,
        color=get_color("LAMMPS")
    )
    ax.fill_between(
        ow_lmp[:,0],
        ow_lmp[:,1] - ow_lmp[:,2],
        ow_lmp[:,1] + ow_lmp[:,2],
        alpha=0.3,
        color=get_color("LAMMPS")
    )
    ax.plot(
        ow_cp2k[:,0],
        ow_cp2k[:,1],
        linestyle=get_ls("CP2K"),
        dashes=(1,1),
        label="CP2K",
        linewidth=3,
        alpha=0.85,
        color=get_color("CP2K")
    )
    ax.fill_between(
        ow_cp2k[:,0],
        ow_cp2k[:,1] - ow_cp2k[:,2],
        ow_cp2k[:,1] + ow_cp2k[:,2],
        alpha=0.3,
        color=get_color("CP2K")
    )

    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-2, 140)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.yaxis.set_minor_locator(MultipleLocator(10))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    #ax.legend(loc=(0.75,0.80), fontsize=12)

    ax = axes[1]
    ax.text(0.05, 0.90, 'b)', transform=ax.transAxes,
            size=20, weight='bold')
    # Plot HW
    ax.plot(
        all_cass["z-loc_nm"],
        all_cass["density-hw_nm^-3_mean"],
        linestyle=get_ls("Cassandra"),
        linewidth=3,
        alpha=0.85,
        label="Cassandra",
        color=get_color("Cassandra")
    )
    ax.fill_between(
        all_cass["z-loc_nm"],
        all_cass["density-hw_nm^-3_mean"] - all_cass["density-hw_nm^-3_std"],
        all_cass["density-hw_nm^-3_mean"] + all_cass["density-hw_nm^-3_std"],
        alpha=0.3,
        color=get_color("Cassandra")
    ) 
    ax.plot(
        hw_gomc["distance_nm"],
        hw_gomc["Avg_No_density_per_nm_sq"],
        linestyle=get_ls("GOMC"),
        dashes=(4,3),
        linewidth=3,
        alpha=0.85,
        label="GOMC",
        color=get_color("GOMC")
    )
    ax.fill_between(
        hw_gomc["distance_nm"],
        hw_gomc["Avg_No_density_per_nm_sq"] - hw_gomc["StdDev_No_density_per_nm_sq"],
        hw_gomc["Avg_No_density_per_nm_sq"] + hw_gomc["StdDev_No_density_per_nm_sq"],
        alpha=0.3,
        color=get_color("GOMC")
    )
    ax.plot(
        hw_gmx[:,0],
        hw_gmx[:,1],
        linestyle=get_ls("GROMACS"),
        linewidth=3,
        alpha=0.85,
        label="GROMACS",
        color=get_color("GROMACS")
    )
    ax.fill_between(
        hw_gmx[:,0],
        hw_gmx[:,1] - hw_gmx[:,2],
        hw_gmx[:,1] + hw_gmx[:,2],
        alpha=0.3,
        color=get_color("GROMACS")
    )
    ax.plot(
        hw_lmp[:,0],
        hw_lmp[:,1],
        linestyle=get_ls("LAMMPS"),
        dashes=(1,2),
        linewidth=3,
        alpha=0.85,
        label="LAMMPS",
        color=get_color("LAMMPS")
    )
    ax.fill_between(
        hw_lmp[:,0],
        hw_lmp[:,1] - hw_lmp[:,2],
        hw_lmp[:,1] + hw_lmp[:,2],
        alpha=0.3,
        color=get_color("LAMMPS")
    )
    ax.plot(
        hw_cp2k[:,0],
        hw_cp2k[:,1],
        linestyle=get_ls("CP2K"),
        dashes=(1,1),
        label="CP2K",
        linewidth=3,
        alpha=0.85,
        color=get_color("CP2K")
    )
    ax.fill_between(
        hw_cp2k[:,0],
        hw_cp2k[:,1] - hw_cp2k[:,2],
        hw_cp2k[:,1] + hw_cp2k[:,2],
        alpha=0.3,
        color=get_color("CP2K")
    )

    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-2, 240)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(40))
    ax.yaxis.set_minor_locator(MultipleLocator(20))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    # Plot S
    ax = axes[2]
    ax.text(0.05, 0.90, 'c)', transform=ax.transAxes,
            size=20, weight='bold')
    ax.plot(
        all_cass["z-loc_nm"],
        all_cass["s_value_mean"],
        linestyle=get_ls("Cassandra"),
        label="Cassandra",
        linewidth=3,
        alpha=0.9,
        color=get_color("Cassandra")
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
        linestyle=get_ls("GOMC"),
        dashes=(4,3),
        label="GOMC",
        linewidth=3,
        alpha=0.9,
        color=get_color("GOMC")
    )
    ax.fill_between(
        s_gomc["distance_nm"],
        s_gomc["Avg_order_param"] - s_gomc["StdDev_order_param"],
        s_gomc["Avg_order_param"] + s_gomc["StdDev_order_param"],
        alpha=0.3,
        color=get_color("GOMC")
    )
    ax.plot(
        s_gmx[:,0],
        s_gmx[:,1],
        linestyle=get_ls("GROMACS"),
        label="GROMACS",
        linewidth=3,
        alpha=0.9,
        color=get_color("GROMACS")
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
        linestyle=get_ls("LAMMPS"),
        dashes=(1,2),
        label="LAMMPS",
        linewidth=3,
        alpha=0.9,
        color=get_color("LAMMPS")
    )
    ax.fill_between(
        s_lmp[:,0],
        s_lmp[:,1] - s_lmp[:,2],
        s_lmp[:,1] + s_lmp[:,2],
        alpha=0.3,
    )
    ax.plot(
        s_cp2k[:,0],
        s_cp2k[:,1],
        linestyle=get_ls("CP2K"),
        dashes=(1,1),
        label="CP2K",
        linewidth=3,
        alpha=0.9,
        color=get_color("CP2K")
    )
    ax.fill_between(
        s_cp2k[:,0],
        s_cp2k[:,1] - s_cp2k[:,2],
        s_cp2k[:,1] + s_cp2k[:,2],
        alpha=0.3,
        color=get_color("CP2K")
    )

    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel(r"$\mathregular{z, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{S}$", fontsize=22, labelpad=15, style="italic")

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
            ncol=5)
    fig.tight_layout()
    fig.savefig("1nm_results.pdf", bbox_inches="tight")

plot_1_water()
plot_large_2nm()
plot_small_1nm()
