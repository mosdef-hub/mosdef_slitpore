import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from matplotlib.ticker import MultipleLocator
from matplotlib import rcParams

rcParams['font.sans-serif'] = 'Arial'
rcParams['font.family'] = 'sans-serif'

def add_subplot_axes(ax,rect):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height])
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

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

def main():

    #seaborn.set_palette("dark")
    data_path = '../simulations/nvt-pore/1x1x1.0nm_1-layer/'
    gmx_path = 'gromacs/data/'
    ow_gmx = np.genfromtxt(data_path+gmx_path+"1_mol_o_density.txt", skip_header=1)
    hw_gmx = np.genfromtxt(data_path+gmx_path+"1_mol_h_density.txt", skip_header=1)
    s_gmx = np.genfromtxt(data_path+gmx_path+"1_mol_s_order.txt", skip_header=1)

    cp2k_path = 'cp2k/data_absz/1water_data/'
    ow_cp2k = np.genfromtxt(data_path+cp2k_path+"o_density.txt", skip_header=1)
    hw_cp2k = np.genfromtxt(data_path+cp2k_path+"h_density.txt", skip_header=1)
    s_cp2k = np.genfromtxt(data_path+cp2k_path+"s_order.txt", skip_header=1)


    fig, axes = plt.subplots(1, 3, figsize=(15,5))
    # Plot OW
    ax = axes[0]
    ax.text(0.05, 0.90, 'a)', transform=ax.transAxes,
            size=20, weight='bold')
    rect = [0.465, 0.7, 0.4, 0.4]
    ax2 = add_subplot_axes(ax, rect)
    ax2.plot(
        ow_gmx[:,0],
        ow_gmx[:,1],
        linestyle=get_ls("GROMACS"),
        label="GROMACS",
        linewidth=3,
        alpha=0.85,
        color=get_color("GROMACS")
    )
    ax2.fill_between(
        ow_gmx[:,0],
        ow_gmx[:,1] - ow_gmx[:,2],
        ow_gmx[:,1] + ow_gmx[:,2],
        alpha=0.3,
        color=get_color("GROMACS")
    )
    ax2.set_xlim((-0.3, 0.3))
    ax2.set_ylim((0.0, 25))
    ax2.set_xlabel(r"$\mathregular{z, nm}$", fontsize=12, labelpad=9)
    ax2.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=12,
            labelpad=9)
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

    ax.set_xlim(-0.01, 0.5)
    ax.set_ylim(-2, 25)
    ax.set_xlabel(r"$\mathregular{\vert z \vert, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(\vert z \vert), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(2))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")


    # Plot HW
    ax = axes[1]
    ax.text(0.05, 0.90, 'b)', transform=ax.transAxes,
            size=20, weight='bold')
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
    rect = [0.7, 0.7, 0.4, 0.4]
    ax2 = add_subplot_axes(ax, rect)
    ax2.plot(
        hw_gmx[:,0],
        hw_gmx[:,1],
        linestyle=get_ls("GROMACS"),
        label="GROMACS",
        linewidth=3,
        alpha=0.85,
        color=get_color("GROMACS")
    )
    ax2.fill_between(
        hw_gmx[:,0],
        hw_gmx[:,1] - hw_gmx[:,2],
        hw_gmx[:,1] + hw_gmx[:,2],
        alpha=0.3,
        color=get_color("GROMACS")
    )
    ax2.set_xlim((-0.3, 0.3))
    ax2.set_ylim((0.0, 25))
    ax2.set_xlabel(r"$\mathregular{z, nm}$", fontsize=12, labelpad=9)
    ax2.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=12,
            labelpad=9)
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

    ax.set_xlim(-0.01, 0.5)
    ax.set_ylim(-2, 25)
    ax.set_xlabel(r"$\mathregular{\vert z \vert, nm}$", fontsize=22, labelpad=15)
    ax.set_ylabel(r"$\mathregular{\rho(z), nm^{-3}}$", fontsize=22, labelpad=15)

    ax.tick_params(axis="both", which="both", direction="in", labelsize=16, pad=6)
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(2))
    ax.xaxis.set_ticks_position("both")
    ax.yaxis.set_ticks_position("both")

    # Plot S
    ax = axes[2]
    ax.text(0.05, 0.90, 'c)', transform=ax.transAxes,
            size=20, weight='bold')
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

    ax.set_xlim(0.0, 0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel(r"$\mathregular{\vert z \vert, nm}$", fontsize=22, labelpad=15)
    #ax.set_ylabel(r"$\mathregular{\rho(\vert z \vert), nm^{-3}}$", fontsize=22, labelpad=15)
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
            ncol=5)
    fig.tight_layout()
    fig.savefig("1_water_results.pdf", bbox_inches="tight")

if __name__ == "__main__":
    main()

