import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import signac
import os
from mosdef_slitpore.analysis import compute_density, compute_s
from mosdef_slitpore.utils.utils import get_bond_array

project = signac.get_project()


def number_density(job, symmetrize=False):
    dim = 1
    box_range = [0.167, 1.167]
    pore_center = (box_range[1] - box_range[0]) / 2 + box_range[0]
    o_densities = list()
    h_densities = list()
    fig, ax = plt.subplots()
    if job.sp.nwater == 1:
        skip = 1
    else:
        skip = 5001
    for trj in md.iterload(
        os.path.join(job.ws, "nvt.trr"),
        top=os.path.join(job.ws, "nvt.gro"),
        chunk=5000,
        skip=skip,
    ):
        water_o = trj.atom_slice(trj.topology.select("name O"))
        water_h = trj.atom_slice(trj.topology.select("name H"))
        area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]

        for water_trj in (water_o, water_h):
            bins, density = compute_density(
                water_trj,
                area,
                dim,
                pore_center=pore_center,
                bin_width=0.01,
                symmetrize=symmetrize,
            )
            label_name = list(set([i.name for i in water_trj.topology.atoms]))
            if label_name[0] == "O":
                o_densities.append(density)
            else:
                h_densities.append(density)

    o_mean = np.mean(o_densities, axis=0)
    h_mean = np.mean(h_densities, axis=0)
    o_std = np.std(o_densities, axis=0)
    h_std = np.std(h_densities, axis=0)

    plt.plot(bins, o_mean, label="O")
    plt.fill_between(bins, o_mean + o_std, o_mean - o_std, alpha=0.2)
    plt.plot(bins, h_mean, label="H")
    plt.fill_between(bins, h_mean + h_std, h_mean - h_std, alpha=0.2)
    plt.xlabel("z-position (nm)")
    plt.ylabel("Number Density ($nm^-3$)")

    plt.legend()
    if symmetrize == True:
        extension = "_symmetrize"
    else:
        extension = ""
    with job:
        np.savetxt(
            f"o_density{extension}.txt",
            np.transpose(np.vstack([bins, o_mean, o_std])),
            header="Bins\tDensity_mean\tDensity_std",
        )

        np.savetxt(
            f"h_density{extension}.txt",
            np.transpose(np.vstack([bins, h_mean, h_std])),
            header="Bins\tDensity_mean\tDensity_std",
        )
        plt.savefig(f"numberdensity{extension}.pdf")
    np.savetxt(
        f"data/{job.sp.nwater}_mol_o_density{extension}.txt",
        np.transpose(np.vstack([bins, o_mean, o_std])),
        header="Bins\tDensity_mean\tDensity_std",
    )

    np.savetxt(
        f"data/{job.sp.nwater}_mol_h_density{extension}.txt",
        np.transpose(np.vstack([bins, h_mean, h_std])),
        header="Bins\tDensity_mean\tDensity_std",
    )


def s_order(job, symmetrize=False):
    dim = 1
    box_range = [0.167, 1.167]
    pore_center = (box_range[1] - box_range[0]) / 2 + box_range[0]
    fig, ax = plt.subplots()
    s_list = list()
    if job.sp.nwater == 1:
        skip = 1
    else:
        skip = 5001
    for trj in md.iterload(
        os.path.join(job.ws, "nvt.trr"),
        top=os.path.join(job.ws, "init.mol2"),
        chunk=5000,
        skip=skip,
    ):
        water_bonds = get_bond_array(trj)
        bins, s_values = compute_s(
            trj,
            dim,
            pore_center=pore_center,
            bond_array=water_bonds,
            symmetrize=symmetrize,
        )
        s_list.append(s_values)

    s_mean = np.mean(s_list, axis=0)
    s_std = np.std(s_list, axis=0)

    plt.plot(bins, s_mean)
    plt.fill_between(bins, s_mean + s_std, s_mean - s_std, alpha=0.2)
    plt.xlabel("z-position (nm)")
    plt.ylabel("S")

    if symmetrize == True:
        extension = "_symmetrize"
    else:
        extension = ""
    with job:
        plt.savefig(f"s_order{extension}.pdf")

        np.savetxt(
            f"s_order{extension}.txt",
            np.transpose(np.vstack([bins, s_mean, s_std])),
            header="Bins\tS_mean\tS_std",
        )
    np.savetxt(
        f"data/{job.sp.nwater}_mol_s_order{extension}.txt",
        np.transpose(np.vstack([bins, s_mean, s_std])),
        header="Bins\tS_mean\tS_std",
    )


def area(job):
    """Calculate molecules of water per area on graphene surface"""
    with job:
        trj = md.load("sample.trr", top="sample.gro")[5000:]

    box_range = [0.167, 1.167]
    area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]
    dim = 1

    n_bins = 200

    fig, ax = plt.subplots()
    areas, bins = compute_mol_per_area(trj, area, dim, box_range, n_bins, shift=False)

    cutoff_indices = np.where(bins < bins[0] + cutoff)
    area_sum = sum(areas[: cutoff_indices[0][-1]])

    cumsum = np.cumsum(areas)
    new_bins = [bi - box_range[0] for bi in bins]
    plt.plot(new_bins, cumsum)
    plt.scatter(bins[cutoff_indices[0][-1]] - box_range[0], area_sum)
    plt.text(0.5, 5, f"n_molecules = {(area_sum):.3f}")
    plt.xlabel("z-position (nm)")
    plt.ylabel("cumulative sum of molecules")
    with job:
        plt.savefig("cumulative_area.pdf")


if __name__ == "__main__":
    for job in project.find_jobs():
        number_density(job)
        s_order(job)
        number_density(job, symmetrize=True)
        s_order(job, symmetrize=True)
