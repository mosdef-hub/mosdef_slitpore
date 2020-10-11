import numpy as np

def compute_density(
    traj,
    area,
    surface_normal_dim=2,
    pore_center=0.0,
    max_distance = 1.0,
    bin_width = 0.01
    ):
    """Compute the density of traj in atoms/nm^3

    Parameters
    ----------
    traj : mdtraj.Trajectory,
        trajectory to analyze
    area : float
        area of the surface in nm^2
    surface_normal_dim : enum (0,1,2), optional, default = 2
        direction normal to the surface (x:0, y:1, z:2)
    pore_center : float, optional, default = 0.0
        coordinate of the pore center along surface_normal_dim
    max_distance : float, optional, default = 1.0
        max distance to consider from the center of the pore
    bin_width : float, optional, default = 0.01
        width of the bin for computing s

    Returns
    -------
    bin_centers : np.ndarray
        the bin centers, shifted so that pore_center is at 0.0
    density : np.ndarray
        the density (atoms / nm^3) in each bin
    """
    distances = traj.xyz[:,:,surface_normal_dim] - pore_center
    bin_centers = []
    density = []
    for bin_center in np.arange(-max_distance, max_distance, bin_width):
        mask = np.logical_and(
            distances > bin_center - 0.5 * bin_width,
            distances < bin_center + 0.5 * bin_width
        )
        bin_centers.append(bin_center)
        density.append(mask.sum() / (area * bin_width * traj.n_frames))

    return bin_centers, density

def compute_s(
    traj,
    surface_normal_dim=2,
    pore_center = 0.0,
    max_distance = 1.0,
    bin_width=0.01
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

    Returns
    -------
    bin_centers : np.ndarray
        the bin centers, shifted so that pore_center is at 0.0
    s_values : np.ndarray
        the value of s for each bin
    """
    # Make molecules whole first
    traj.make_molecules_whole(inplace=True)
    # Select ow and hw
    water_o = traj.top.select("water and name O")
    water_h = traj.top.select("water and name H")
    traj_ow = traj.atom_slice(water_o)
    traj_hw = traj.atom_slice(water_h)

    # Compute angles between surface normal ([0,0,1]) and h-o-h bisector
    hw_midpoints = traj_hw.xyz.reshape(traj_hw.n_frames,-1,2,3).mean(axis=2)
    vectors = (traj_ow.xyz - hw_midpoints)
    vectors /= np.linalg.norm(vectors, axis=-1, keepdims=True)
    cos_angles = vectors[:,:,surface_normal_dim]

    # Compute distances -- center of pore already @ 0,0; use OW position
    distances = traj_ow.xyz[:,:,surface_normal_dim] - pore_center
    bin_centers = []
    s_values = []
    for bin_center in np.arange(-max_distance, max_distance, bin_width):
        mask = np.logical_and(
            distances > bin_center - 0.5 * bin_width,
            distances < bin_center + 0.5 * bin_width
        )
        s = (3.0 * np.mean(cos_angles[mask]**2) - 1.0) / 2.0
        bin_centers.append(bin_center)
        s_values.append(s)

    return bin_centers, s_values

def compute_mol_per_area(traj, area,
        dim, box_range, n_bins, shift=True, frame_range=None):
    """
    Calculate molecules per area
    Parameters
    ----------
    traj : mdtraj.trajectory
        Trajectory
    area : int or float
        Area of box in dimensions where number density isn't calculated
    dim : int
        Dimension to calculate number density profile (x: 0, y: 1, z: 2)
    box_range : array
        Range of coordinates in 'dim' to evaluate
    n_bins : int
        Number of bins in histogram
    shift : boolean, default=True
        Shift center to zero if True
    frame_range : Python range() (optional)
        Range of frames to calculate number density function over
    
    Returns
    -------
    areas : list
        A list containing number density for each bin
    new_bins : list
        A list of bins
    """
    water_o = traj.atom_slice(traj.topology.select('name O'))
    resnames = np.unique([x.name for x in
               water_o.topology.residues])
    
    if frame_range:
        water_o = water_o[frame_range]
    for i,frame in enumerate(water_o):
        indices = [[atom.index for atom in compound.atoms]
                  for compound in
                  list(frame.topology.residues)]

        if frame_range:
            if i == 0:
                x = np.histogram(frame.xyz[0,indices,dim].flatten(), 
                    bins=n_bins, range=(box_range[0], box_range[1]))
                areas = x[0]
                bins = x[1]
            else:
                areas += np.histogram(frame.xyz[0, indices, dim].
                        flatten(),bins=n_bins, range=(box_range[0],
                            box_range[1]))[0]
        else:
            if i == 0:
                x = np.histogram(frame.xyz[0,indices,dim].flatten(), 
                    bins=n_bins, range=(box_range[0], box_range[1]))
                areas = x[0]
                bins = x[1]
            else:
                areas += np.histogram(frame.xyz[0, indices, dim].
                        flatten(),bins=n_bins, range=(box_range[0],
                            box_range[1]))[0]

    areas = np.divide(areas, water_o.n_frames)

    new_bins = list()
    for idx, bi in enumerate(bins):
        if (idx+1) >= len(bins):
            continue
        mid = (bins[idx] + bins[idx+1])/2
        new_bins.append(mid)

    if shift:
        middle = float(n_bins / 2)
        if middle % 2 != 0:
            shift_value = new_bins[int(middle - 0.5)]
        else:
            shift_value = new_bins[int(middle)]
        new_bins = [(bi-shift_value) for bi in new_bins]
    
    return (areas, new_bins)

def compute_angles(
    traj,
    surface_normal_dim=2,
    pore_center = 0.0,
    max_distance = 1.0,
    bin_width=0.01,
    distance_criteria=0.05
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

    Returns
    -------
    bin_centers : np.ndarray
        the bin centers, shifted so that pore_center is at 0.0
    s_values : np.ndarray
        the value of s for each bin
    """
    # Make molecules whole first
    traj.make_molecules_whole(inplace=True)
    # Select ow and hw
    water_o = traj.top.select("water and name O")
    water_h = traj.top.select("water and name H")
    traj_ow = traj.atom_slice(water_o)
    traj_hw = traj.atom_slice(water_h)

    # Discard molecules not within 0.1 nm of center of pore
    distance_mask = np.logical_and(
        traj_ow.xyz[:,:,surface_normal_dim] > pore_center - distance_criteria,
        traj_ow.xyz[:,:,surface_normal_dim] < pore_center + distance_criteria
    )

    # Compute angles between surface normal ([0,0,1]) and h-o-h bisector
    hw_midpoints = traj_hw.xyz.reshape(traj_hw.n_frames,-1,2,3).mean(axis=2)
    vectors = (traj_ow.xyz - hw_midpoints)
    normal = np.full(np.shape(traj_ow.xyz), [0, 1, 0])
    # Use distance mask
    vectors = vectors[distance_mask]
    normal = normal[distance_mask]
    vectors = np.array([v1 / np.linalg.norm(v1) for v1 in vectors])
    normal = np.array([v1 / np.linalg.norm(v1) for v1 in normal])
    cos_angles = list()
    for i in range(len(vectors)):
        angle = np.arccos(np.dot(vectors[i], normal[i])) * (180/np.pi)
        cos_angles.append(angle)

    # Compute distances -- center of pore already @ 0,0; use OW position
    bin_centers = []
    angles = []
    for bin_center in np.arange(0, 180, bin_width):
        mask = np.logical_and(
            cos_angles > bin_center - 0.5 * bin_width,
            cos_angles < bin_center + 0.5 * bin_width
        )
        bin_centers.append(bin_center)
        angles.append(mask.sum()/len(cos_angles))

    return bin_centers, angles
