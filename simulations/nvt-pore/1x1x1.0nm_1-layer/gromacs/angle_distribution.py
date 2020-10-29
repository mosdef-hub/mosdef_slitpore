import os
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import signac
import shutil
from mosdef_slitpore.analysis import compute_density, compute_s, compute_angle
from scipy import stats
from mosdef_slitpore.utils.utils import get_bond_array

project = signac.get_project()


def angle_dist(job):
    dim = 1
    #box_range = [0.167, 1.167]
    box_range = [0.5, 0.8]
    pore_center = (box_range[1] - box_range[0]) / 2 + box_range[0]
    fig, ax = plt.subplots()
    cos_angle_list = list()
    all_cos_angle_list = list()
    for trj in md.iterload(
        os.path.join(job.ws, "nvt.trr"),
        top=os.path.join(job.ws, "init.mol2"),
        chunk=5000,
        skip=1,
    ):

        water_bonds = get_bond_array(trj)
        bins, cos_angle_values, all_cos_angles = compute_angle(
            trj, dim, pore_center=pore_center, bond_array=water_bonds
        )
        cos_angle_list.append(cos_angle_values)
        all_cos_angle_list.extend(all_cos_angles)
    cos_angle_mean = np.mean(cos_angle_list, axis=0)
    cos_angle_std = np.std(cos_angle_list, axis=0)

    plt.plot(bins, cos_angle_mean)
    plt.fill_between(
        bins, cos_angle_mean + cos_angle_std, cos_angle_mean - cos_angle_std, alpha=0.2
    )
    plt.xlabel("z-position (nm)")
    plt.ylabel("cos(angle)")

    with job:
        plt.savefig(
            project.root_directory()
            + "/data/{}_mol_angle_profile.pdf".format(
                str(job.sp.nwater)
            )
        )

        np.savetxt(
            project.root_directory()
            + "/data/{}_mol_angle_profile.txt".format(
                str(job.sp.nwater)
            ),
            np.transpose(np.vstack([bins, cos_angle_mean, cos_angle_std])),
            header="Bins\tcos_angle_mean\tcos_angle_std",
        )

    plt.figure()
    all_cos_angle_list = np.asarray(all_cos_angle_list)
    all_angle_list = (180 / np.pi) * np.arccos(all_cos_angle_list)
    counts, cos_angle_bins, bars = plt.hist(
        all_cos_angle_list, bins=60, alpha=0.5, density=False
    )
    cos_angle_bins_center = (cos_angle_bins[:-1] + cos_angle_bins[1:]) / 2
    plt.xlabel("cos(angle)")
    plt.ylabel("Relative frequency")
    with job:
        plt.savefig(
            project.root_directory()
            + "/data/{}_mol_cos_angle_dist.pdf".format(
                str(job.sp.nwater)
            )
        )

        np.savetxt(
            project.root_directory()
            + "/data/{}_mol_cos_angle_dist.txt".format(
                str(job.sp.nwater)
            ),
            np.transpose(np.vstack([cos_angle_bins_center, counts])),
            header="cos_Angle_bins\tRelativeFreq",
        )
    plt.figure()
    bins = np.linspace(0, 180, num=61)
    weights = np.ones_like(all_angle_list) / len(all_angle_list)
    counts, angle_bins, bars = plt.hist(
        all_angle_list, bins=bins, weights=weights, alpha=0.5
    )
    plt.xlabel("Angle (degress)")
    plt.ylabel("Relative frequency")
    plt.title("Unnormalized distribution")
    angle_bins_center = (angle_bins[:-1] + angle_bins[1:]) / 2
    with job:
        plt.savefig(
            project.root_directory()
            + "/data/{}_mol_angle_dist_unnormalized.pdf".format(
                str(job.sp.nwater)
            )
        )

        np.savetxt(
            project.root_directory()
            + "/data/{}_mol_angle_dist_unnormalized.txt".format(
                str(job.sp.nwater)
            ),
            np.transpose(np.vstack([angle_bins_center, counts])),
            header="Angle_bins\tRelativeFreq",
        )

    plt.figure()
    weights = np.ones_like(angle_bins_center) / len(angle_bins_center)
    normalized_counts = np.divide(
        counts, abs(np.sin((np.pi / 180) * angle_bins_center))
    )
    normalized_counts /= np.sum(normalized_counts)
    arr = plt.hist(angle_bins_center, weights=normalized_counts, bins=bins, density=False)
    plt.xlabel("Angle (degress)")
    plt.ylabel("Relative frequency")
    plt.title("Normalized distribution")
    with job:
        plt.savefig(
            project.root_directory()
            + "/data/{}_mol_angle_dist_normalized.pdf".format(
                str(job.sp.nwater)
            )
        )

        np.savetxt(
            project.root_directory()
            + "/data/{}_mol_angle_dist_normalized.txt".format(
                str(job.sp.nwater)
            ),
            np.transpose(np.vstack([angle_bins_center, normalized_counts])),
            header="Angle_bins\tRelativeFreq",
        )


if __name__ == "__main__":
    for job in project.find_jobs():
        if job.sp.nwater == 1:
            angle_dist(job)
