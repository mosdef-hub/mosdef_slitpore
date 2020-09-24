import signac
import mbuild
import mdtraj as md
import numpy as np
import pandas as pd

from mosdef_slitpore.utils.cassandra import spce_water
from mosdef_slitpore.analysis import compute_density
from mosdef_slitpore.analysis import compute_s


def main():

    project = signac.get_project("../")

    empty_pore = mbuild.recipes.GraphenePore(
        pore_width=2.0,
        pore_length=3.0,
        pore_depth=3.0,
        n_sheets=3,
        slit_pore_dim=2,
    )

    empty_pore.translate(-empty_pore.center)
    empty_pore.periodicity[2] = 6.0
    empty_pore.name = 'RES'

    # Create a water molecule with the spce geometry
    single_water = spce_water()
    single_water.name = 'SOL'

    for nwater, group in project.groupby("nwater"):
        # New dataframe to save the results
        df = pd.DataFrame()

        # Create a topology for the given system
        water_box = mbuild.Box([3.0, 3.0, 1.8]) #nm
        water = mbuild.fill_box(single_water, n_compounds=nwater, box=water_box)
        water.translate(-water.center)
        filled_pore = mbuild.Compound()
        empty_pore.parent = None
        filled_pore.add(empty_pore, inherit_periodicity=True)
        filled_pore.add(water, inherit_periodicity=False)
        xy_area = filled_pore.periodicity[0] * filled_pore.periodicity[1]
        top = filled_pore.to_trajectory(residues=["RES", "SOL"])

        # Load all trajectories and combine
        for job in group:
            run = job.sp.run
            # Load in full trajectory
            full_traj = md.load(job.fn("prod.nvt.out.xyz"), top=top)
            # Add unit cell information
            full_traj = md.Trajectory(
                full_traj.xyz,
                full_traj.top,
                unitcell_lengths = np.tile(filled_pore.periodicity, (full_traj.n_frames,1)),
                unitcell_angles = np.tile([90.,90.,90.], (full_traj.n_frames,1)),
            )
            # Keep only water
            slice_water = full_traj.top.select("water and name O H")
            traj = full_traj.atom_slice(slice_water)
            slice_ow = traj.top.select("name O")
            slice_hw = traj.top.select("name H")
            traj_ow = traj.atom_slice(slice_ow)
            traj_hw = traj.atom_slice(slice_hw)

            # Compute the density
            bin_centers_ow, density_ow = compute_density(traj_ow, xy_area, bin_width=0.005)
            bin_centers_hw, density_hw = compute_density(traj_hw, xy_area, bin_width=0.005)

            # Compute the s order parameter
            bin_centers_s, s_results = compute_s(traj, bin_width=0.005)

            assert np.allclose(bin_centers_ow, bin_centers_hw)
            assert np.allclose(bin_centers_ow, bin_centers_s)

            # Save results
            tmp_df = pd.DataFrame()
            tmp_df[f"run"] = run
            tmp_df[f"z-loc_nm"] = bin_centers_ow
            tmp_df[f"density-ow_nm^-3"] = density_ow
            tmp_df[f"density-hw_nm^-3"] = density_hw
            tmp_df[f"s_value"] = s_results
            df = df.append(tmp_df)

        # Compute mean/stdev and save to file
        means = df.groupby("z-loc_nm").mean().drop(columns=["run"]).add_suffix("_mean")
        stds = df.groupby("z-loc_nm").std().drop(columns=["run"]).add_suffix("_std")
        combined = means.merge(stds, on="z-loc_nm")
        combined.to_csv(f"results_nd_{nwater}-water.csv")


if __name__ == "__main__":
    main()
