import numpy as np


def compute_angle(
    traj,
    surface_normal_dim=2,
    pore_center=0.0,
    max_distance=1.0,
    bin_width=0.01,
    symmetrize=False,
):
    """Compute the "s" order parameter

    Parameters
    ----------
    traj : mdtraj.Trajectory,
        trajectory to analyze
    surface_normal_dim : enum (0,1,2), optional, default = 2
        direction normal to the surface (x:0, y:1, z:2)
    pore_center : float, optional, default = 0.0
        coordinate of the pore center along surface_normal_dim
    max_distance : float, optional, default = 1.0
        max distance to consider from the center of the pore
    bin_width : float, optional, default = 0.01
        width of the bin for computing s
    symmetrize : bool, optional, default = False
        if binning should be done in abs(z) instead of z
    Returns
    -------
    bin_centers : np.ndarray
        the bin centers, shifted so that pore_center is at 0.0
    angle_values : np.ndarray
        the value of average angle for each bin
    """
    # Make molecules whole first
    traj.make_molecules_whole(inplace=True)
    # Select ow and hw
    water_o = traj.top.select("water and name O")
    water_h = traj.top.select("water and name H")
    traj_ow = traj.atom_slice(water_o)
    traj_hw = traj.atom_slice(water_h)

    # Compute angles between surface normal ([0,0,1]/[0,0,-1]) and h-o-h bisector
    hw_midpoints = traj_hw.xyz.reshape(traj_hw.n_frames, -1, 2, 3).mean(axis=2)

    vectors = traj_ow.xyz - hw_midpoints
    vectors /= np.linalg.norm(vectors, axis=-1, keepdims=True)
    cos_angles = vectors[:, :, surface_normal_dim]
    side_of_pore = np.sign(-traj_ow.xyz[:, :, surface_normal_dim] + pore_center)
    cos_angles = np.multiply(cos_angles, side_of_pore)
    angles = (180 / np.pi) * np.arccos(cos_angles)
    # Compute distances -- center of pore already @ 0,0; use OW position
    if symmetrize:
        distances = abs(traj_ow.xyz[:, :, surface_normal_dim] - pore_center)
    else:
        distances = traj_ow.xyz[:, :, surface_normal_dim] - pore_center
    bin_centers = []
    angle_values = []
    for bin_center in np.arange(-max_distance, max_distance, bin_width):
        mask = np.logical_and(
            distances > bin_center - 0.5 * bin_width,
            distances < bin_center + 0.5 * bin_width,
        )
        angle = np.mean(angles[mask])
        bin_centers.append(bin_center)
        angle_values.append(angle)

    return bin_centers, angle_values
