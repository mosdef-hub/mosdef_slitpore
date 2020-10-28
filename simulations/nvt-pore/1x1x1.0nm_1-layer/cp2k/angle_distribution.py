import os
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import signac
import shutil
from mosdef_slitpore.analysis import compute_density, compute_s, compute_angle
from scipy import stats

project = signac.get_project()


def create_data_folder():
    data_path = "distribution_data"
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.makedirs(data_path)


def create_individual_data_folder(job):
    os.chdir("distribution_data")
    os.makedirs(str(job.sp.nwater) + "water_data")
    os.chdir("..")


def angle_dist(job):
    dim = 1
    box_range = [0.5, 1.5]
    pore_center = (box_range[1] - box_range[0]) / 2 + box_range[0]
    fig, ax = plt.subplots()
    cos_angle_list = list()
    all_cos_angle_list = list()
    trj = md.load(os.path.join(job.ws, "carbon_water-pos-1.pdb"))
    trj.save(os.path.join(job.ws, "carbon_water-pos-1.xyz"), force_overwrite=True)
    results_string = ""
    for trj in md.iterload(
        os.path.join(job.ws, "carbon_water-pos-1.xyz"),
        top=os.path.join(job.ws, "init.mol2"),
        chunk=5000,
        skip=6000,
    ):
        trj = md.Trajectory(
            trj.xyz,
            trj.top,
            unitcell_lengths=np.tile([0.9824, 2.0000, 1.0635], (trj.n_frames, 1)),
            unitcell_angles=np.tile([90.0, 90.0, 90.0], (trj.n_frames, 1)),
        )

        bins, cos_angle_values, all_cos_angles = compute_angle(
            trj, dim, pore_center=pore_center
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
            + "/distribution_data/{}/angle_profile.pdf".format(
                str(job.sp.nwater) + "water_data"
            )
        )

        np.savetxt(
            project.root_directory()
            + "/distribution_data/{}/angle_profile.txt".format(
                str(job.sp.nwater) + "water_data"
            ),
            np.transpose(np.vstack([bins, cos_angle_mean, cos_angle_std])),
            header="Bins\tcos_angle_mean\tcos_angle_std",
        )

    plt.figure()
    all_cos_angle_list = np.asarray(all_cos_angle_list)
    all_angle_list = (180 / np.pi) * np.arccos(all_cos_angle_list)
    counts, cos_angle_bins, bars = plt.hist(
        all_cos_angle_list, bins=100, alpha=0.5, density=True
    )
    results_string += (
        "The mean of the cos(angle) is {}".format(np.mean(all_cos_angle_list)) + "\n"
    )
    results_string += (
        "The stdev of the cos(angle) is {}".format(np.std(all_cos_angle_list)) + "\n"
    )
    cos_angle_bins_center = (cos_angle_bins[:-1] + cos_angle_bins[1:]) / 2
    plt.xlabel("cos(angle)")
    plt.ylabel("Relative frequency")
    with job:
        plt.savefig(
            project.root_directory()
            + "/distribution_data/{}/cos_angle_dist.pdf".format(
                str(job.sp.nwater) + "water_data"
            )
        )

        np.savetxt(
            project.root_directory()
            + "/distribution_data/{}/cos_angle_dist.txt".format(
                str(job.sp.nwater) + "water_data"
            ),
            np.transpose(np.vstack([cos_angle_bins_center, counts])),
            header="cos_Angle_bins\tRelativeFreq",
        )
    plt.figure()
    counts, angle_bins, bars = plt.hist(
        all_angle_list, bins=100, alpha=0.5, density=True
    )
    plt.xlabel("Angle (degress)")
    plt.ylabel("Relative frequency")
    plt.title("Unnormalized distribution")
    angle_bins_center = (angle_bins[:-1] + angle_bins[1:]) / 2
    with job:
        plt.savefig(
            project.root_directory()
            + "/distribution_data/{}/angle_dist_unnormalized.pdf".format(
                str(job.sp.nwater) + "water_data"
            )
        )

        np.savetxt(
            project.root_directory()
            + "/distribution_data/{}/angle_dist_unnormalized.txt".format(
                str(job.sp.nwater) + "water_data"
            ),
            np.transpose(np.vstack([angle_bins_center, counts])),
            header="Angle_bins\tRelativeFreq",
        )

    results_string += (
        "The mean of the angle is {}".format(np.mean(all_angle_list)) + "\n"
    )
    results_string += (
        "The stdev of the angle is {}".format(np.std(all_angle_list)) + "\n"
    )
    plt.figure()
    normalized_counts = np.divide(
        counts, abs(np.sin((np.pi / 180) * angle_bins_center))
    )
    arr = plt.hist(angle_bins_center, weights=normalized_counts, bins=100, density=True)
    # plt.bar(angle_bins_center,normalized_counts)
    plt.xlabel("Angle (degress)")
    plt.ylabel("Relative frequency")
    plt.title("Normalized distribution")
    with job:
        plt.savefig(
            project.root_directory()
            + "/distribution_data/{}/angle_dist_normalized.pdf".format(
                str(job.sp.nwater) + "water_data"
            )
        )

        np.savetxt(
            project.root_directory()
            + "/distribution_data/{}/angle_dist_normalized.txt".format(
                str(job.sp.nwater) + "water_data"
            ),
            np.transpose(np.vstack([angle_bins_center, normalized_counts])),
            header="Angle_bins\tRelativeFreq",
        )
        text_file = open(
            project.root_directory()
            + "/distribution_data/{}/result.txt".format(
                str(job.sp.nwater) + "water_data"
            ),
            "w",
        )
        n = text_file.write(results_string)
        text_file.close()


if __name__ == "__main__":
    create_data_folder()
    for job in project.find_jobs():
        if job.sp.nwater == 1:
            create_individual_data_folder(job)
            angle_dist(job)
