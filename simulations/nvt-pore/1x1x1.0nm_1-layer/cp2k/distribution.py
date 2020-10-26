import os
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import signac
import shutil
from mosdef_slitpore.analysis import compute_density, compute_s
from scipy import stats
from mosdef_slitpore.analysis_angle import compute_angle

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
    angle_list = list()
    trj = md.load(os.path.join(job.ws, "carbon_water-pos-1.pdb"))
    trj.save(os.path.join(job.ws, "carbon_water-pos-1.xyz"), force_overwrite=True)

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

        bins, angle_values = compute_angle(trj, dim, pore_center=pore_center)
        angle_list.append(angle_values)
    angle_mean = np.mean(angle_list, axis=0)
    angle_std = np.std(angle_list, axis=0)

    plt.plot(bins, angle_mean)
    plt.fill_between(bins, angle_mean + angle_std, angle_mean - angle_std, alpha=0.2)
    plt.xlabel("z-position (nm)")
    plt.ylabel("angle")

    with job:
        plt.savefig(
            project.root_directory()
            + "/distribution_data/{}/angle.pdf".format(
                str(job.sp.nwater) + "water_data"
            )
        )

        np.savetxt(
            project.root_directory()
            + "/distribution_data/{}/angle.txt".format(
                str(job.sp.nwater) + "water_data"
            ),
            np.transpose(np.vstack([bins, angle_mean, angle_std])),
            header="Bins\tangle_mean\tangle_std",
        )


if __name__ == "__main__":
    create_data_folder()
    for job in project.find_jobs():
        create_individual_data_folder(job)
        angle_dist(job)
