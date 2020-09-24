import os
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import signac
import shutil
from mosdef_slitpore.analysis import compute_density, compute_s

project = signac.get_project()


def create_data_folder():
    data_path = "data"
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.makedirs(data_path)


def create_individual_data_folder(job):
    os.chdir("data")
    os.makedirs(str(job.sp.nwater) + "water_data")
    os.chdir("..")


def number_density(job):
    dim = 1
    box_range = [0.5, 1.5]
    pore_center = (box_range[1] - box_range[0]) / 2 + box_range[0]
    o_densities = list()
    h_densities = list()
    fig, ax = plt.subplots()
    for trj in md.iterload(
        os.path.join(job.ws, "carbon_water-pos-1.pdb"),
        top=os.path.join(job.ws, "init.mol2"),
        chunk=5000,
        skip=6000,
    ):
        water_o = trj.atom_slice(trj.topology.select("name O"))
        water_h = trj.atom_slice(trj.topology.select("name H"))
        area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]

        for water_trj in (water_o, water_h):
            bins, density = compute_density(
                water_trj, area, dim, pore_center=pore_center, bin_width=0.01
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
    with job:
        np.savetxt(
            project.root_directory()
            + "/data/{}/o_density.txt".format(str(job.sp.nwater) + "water_data"),
            np.transpose(np.vstack([bins, o_mean, o_std])),
            header = "Bins\tDensity_mean\tDensity_std",
        )

        np.savetxt(
            project.root_directory()
            + "/data/{}/h_density.txt".format(str(job.sp.nwater) + "water_data"),
            np.transpose(np.vstack([bins, h_mean, h_std])),
            header = "Bins\tDensity_mean\tDensity_std",
        )
        plt.savefig(
            project.root_directory()
            + "/data/{}/numberdensity.pdf".format(str(job.sp.nwater) + "water_data")
        )


def s_order(job):
    dim = 1
    box_range = [0.5, 1.5]
    pore_center = (box_range[1] - box_range[0]) / 2 + box_range[0]
    fig, ax = plt.subplots()
    s_list = list()
    trj = md.load(os.path.join(job.ws, "carbon_water-pos-1.pdb"))
    trj.save(os.path.join(job.ws, "carbon_water-pos-1.xyz"), force_overwrite=True)

    for trj in md.iterload(
        os.path.join(job.ws, "carbon_water-pos-1.xyz"),
        top = os.path.join(job.ws, "init.mol2"),
        chunk = 5000,
        skip = 6000,
    ):
        trj = md.Trajectory(
            trj.xyz,
            trj.top,
            unitcell_lengths = np.tile([0.9824, 2.0000, 1.0635], (trj.n_frames, 1)),
            unitcell_angles = np.tile([90.0, 90.0, 90.0], (trj.n_frames, 1)),
        )

        bins, s_values = compute_s(trj, dim, pore_center=pore_center)
        s_list.append(s_values)

    s_mean = np.mean(s_list, axis=0)
    s_std = np.std(s_list, axis=0)

    plt.plot(bins, s_mean)
    plt.fill_between(bins, s_mean + s_std, s_mean - s_std, alpha=0.2)
    plt.xlabel("z-position (nm)")
    plt.ylabel("S")

    with job:
        plt.savefig(
            project.root_directory()
            + "/data/{}/s_order.pdf".format(str(job.sp.nwater) + "water_data")
        )

        np.savetxt(
            project.root_directory()
            + "/data/{}/s_order.txt".format(str(job.sp.nwater) + "water_data"),
            np.transpose(np.vstack([bins, s_mean, s_std])),
            header = "Bins\tS_mean\tS_std",
        )


if __name__ == "__main__":
    create_data_folder()
    for job in project.find_jobs():
        create_individual_data_folder(job)
        number_density(job)
        s_order(job)
