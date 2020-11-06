import numpy as np
import matplotlib.pyplot as plt
import MDAnalysis as mda
from MDAnalysis import transformations
from scipy.ndimage.measurements import center_of_mass
from scipy import stats
import MDAnalysis.transformations.rotate as w
#from __future__ import absolute_import

from MDAnalysis.lib._cutil import make_whole

#*****************************
# note : wrap and unwrap pasted in from MDAnalysis.transformations.wrap as didnt want to import (start)
#*****************************
def wrap(ag, compound='atoms'):
    """
    Shift the contents of a given AtomGroup back into the unit cell. ::

       +-----------+          +-----------+
       |           |          |           |
       |         3 | 6        | 6       3 |
       |         ! | !        | !       ! |
       |       1-2-|-5-8  ->  |-5-8   1-2-|
       |         ! | !        | !       ! |
       |         4 | 7        | 7       4 |
       |           |          |           |
       +-----------+          +-----------+

    Example
    -------

    .. code-block:: python

        ag = u.atoms
        transform = mda.transformations.wrap(ag)
        u.trajectory.add_transformations(transform)

    Parameters
    ----------

    ag: Atomgroup
        Atomgroup to be wrapped in the unit cell
    compound : {'atoms', 'group', 'residues', 'segments', 'fragments'}, optional
        The group which will be kept together through the shifting process.

    Notes
    -----
    When specifying a `compound`, the translation is calculated based on
    each compound. The same translation is applied to all atoms
    within this compound, meaning it will not be broken by the shift.
    This might however mean that not all atoms from the compound are
    inside the unit cell, but rather the center of the compound is.

    Returns
    -------
    MDAnalysis.coordinates.base.Timestep

    """

    def wrapped(ts):
        ag.wrap(compound=compound)

        return ts

    return wrapped


def unwrap(ag):
    """
    Move all atoms in an AtomGroup so that bonds don't split over images

    Atom positions are modified in place.

    This function is most useful when atoms have been packed into the primary
    unit cell, causing breaks mid molecule, with the molecule then appearing
    on either side of the unit cell. This is problematic for operations
    such as calculating the center of mass of the molecule. ::

       +-----------+     +-----------+
       |           |     |           |
       | 6       3 |     |         3 | 6
       | !       ! |     |         ! | !
       |-5-8   1-2-| ->  |       1-2-|-5-8
       | !       ! |     |         ! | !
       | 7       4 |     |         4 | 7
       |           |     |           |
       +-----------+     +-----------+

    Example
    -------

    .. code-block:: python

        ag = u.atoms
        transform = mda.transformations.unwrap(ag)
        u.trajectory.add_transformations(transform)

    Parameters
    ----------
    atomgroup : AtomGroup
        The :class:`MDAnalysis.core.groups.AtomGroup` to work with.
        The positions of this are modified in place.

    Returns
    -------
    MDAnalysis.coordinates.base.Timestep

    """

    try:
        ag.fragments
    except AttributeError:
        raise AttributeError("{} has no fragments".format(ag))

    def wrapped(ts):
        for frag in ag.fragments:
            make_whole(frag)

        return ts

    return wrapped
#*****************************
# note : wrap and unwrap pasted in from MDAnalysis.transformations.wrap as didnt want to import (end)
#*****************************

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    theta = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

    return theta


def s_order_parameter(angles):
    """ Calculate angle order parameter

    Parameters
    ----------
    angles : list
        Angle between water and surface in radians
    """
    angle_average = np.mean(np.cos(angles) ** 2)
    s = (3 * angle_average - 1) / 2

    return s


def calc_water_angle(trj_file, gro_file, cutoff, dim=2, filepath=''):
    """ Calculate angle distribution between a water molecule vector and normal of
    a surface
    Water vector:
        ^
        |
        |
        O
       / \
      H   H
    Parameters
    ----------
    trj_file : trajectory file
        MD trajectory to load
    gro_file : Coordinate file
        MD coordinates to load.  MOL2 file is preferred as it contains bond information.
    cutoff : float
        Cutoff to analyze molecules in z-direction (angstroms)
    dim : int
        Dimension of surface vector
    """
    if dim == 0:
        normal_vector = [1, 0, 0]
    elif dim == 1:
        normal_vector = [0, 1, 0]
    else:
        normal_vector = [0, 0, 1]

    trj_str = f'{filepath}/{trj_file}'
    gro_str = f'{filepath}/{gro_file}'

    universe = mda.Universe(gro_str, trj_str)

    water_groups = universe.select_atoms('resname H2O h2o')
    print("Unwrapping water molecules")
    #transform = transformations.unwrap(water_groups)
    transform = unwrap(water_groups)
    universe.trajectory.add_transformations(transform)
    print("Finished unwrapping water molecules")
    coordinates = [water_groups.positions for ts in universe.trajectory]
    angles = list()
    radians = list()
    print("Starting to analyze vectors ... ")
    for frame_num, frame in enumerate(coordinates):
        for idx in np.arange(3, len(frame) + 3, 3):
            xyz = frame[idx - 3:idx]

            if xyz[0][dim] > cutoff:
                continue
            # Get midpoint of hydrogens
            fit = [(xyz[1][i] + xyz[2][i]) / 2 for i in range(3)]
            # Draw vector of oxygen going through hydrogen midpoint
            vector = [xyz[0][i] - fit[i] for i in range(3)]

            angle = angle_between(np.array([vector[0], vector[1], vector[2]]),
                                  np.array(normal_vector)) * (180 / np.pi)

            angle_in_radians = angle * np.pi / 180
            radians.append(angle_in_radians)
            angles.append(angle)

    y, x = np.histogram(angles, bins=180, density=True, range=(0.0, 180.0))
    new_x = list()
    for idx in range(180):
        mid = idx + 0.5
        new_x.append(mid)
    new_x_hist = y / np.sin((np.array(new_x) * np.pi / 180))
    fig, ax = plt.subplots()
    plt.plot(new_x, y)
    plt.xlim((0, 181))
    plt.ylabel('Count')
    plt.xlabel('Angle (Deg)')
    fig, ax = plt.subplots()
    # plt.bar(new_x, new_x_hist)
    plt.bar(new_x, y)
    plt.xlim((0, 181))
    plt.ylabel('Count')
    plt.xlabel('Angle (Deg)')
    plt.savefig(f'{filepath}/water_angles.pdf')


def calc_water_order_parameter(trj_file, gro_file, cutoffs, dim=2, filepath=''):
    """ Calculate the order parameter between a water molecule vector and normal of
    a surface
    DOI: 10.1021/la0347354
    Water vector:
        ^
        |
        |
        O
       / \
      H   H
    Parameters
    ----------
    trj_file : trajectory file
        MD trajectory to load
    gro_file : Coordinate file
        MD coordinates to load.  MOL2 file is preferred as it contains bond information.
    cutoff : list or tuple
        Dimensions of slitpore to consider (angstroms)
    dim : int
        Dimension of surface vector
    """
    if dim == 0:
        normal_vector = [1, 0, 0]
    elif dim == 1:
        normal_vector = [0, 1, 0]
    else:
        normal_vector = [0, 0, 1]

    trj_str = f'{filepath}/{trj_file}'
    gro_str = f'{filepath}/{gro_file}'

    universe = mda.Universe(gro_str, trj_str)

    water_groups = universe.select_atoms('resname H2O h2o')
    print(' water_groups = '+str( water_groups))
    print("Unwrapping water molecules")
    transform = unwrap(water_groups)
    print(' transform = '+str( transform))
    universe.trajectory.add_transformations(transform)
    print("Finished unwrapping water molecules")
    #coordinates = [water_groups.positions for ts in universe.trajectory[9000:]]
    coordinates = [water_groups.positions for ts in universe.trajectory[0:]]
    print("Starting to analyze vectors ... ")
    angle_position = dict()
    for frame_num, frame in enumerate(coordinates):
        for idx in np.arange(3, len(frame) + 3, 3):
            xyz = frame[idx - 3:idx]

            if xyz[0][dim] < cutoffs[0] and xyz[0][dim] > cutoffs[1]:
                continue
            # Get midpoint of hydrogens
            fit = [(xyz[1][i] + xyz[2][i]) / 2 for i in range(3)]
            # Draw vector of oxygen going through hydrogen midpoint
            vector = [xyz[0][i] - fit[i] for i in range(3)]

            angle = angle_between(np.array([vector[0], vector[1], vector[2]]),
                                  np.array(normal_vector)) * (180 / np.pi)

            angle_in_radians = angle * np.pi / 180
            angle_position[xyz[0][dim]] = angle_in_radians

    distance_dict = dict()

    for dis in np.arange(cutoffs[0], cutoffs[1], step=0.1):
        distance_dict[dis] = list()
        for pos, angle in angle_position.items():
            if pos > dis and pos < (dis + 1):
                distance_dict[dis].append(angle)

    s_order_dict = dict()
    for dis, angles in distance_dict.items():
        s_order_dict[dis] = s_order_parameter(angles)

    print('s_order_dict.keys() = '+str(s_order_dict.keys()))
    print('s_order_dict.values() = ' + str(s_order_dict.values()))

    fig, ax = plt.subplots()
    plt.plot(s_order_dict.keys(), s_order_dict.values())
    plt.xlabel('Distance')
    plt.ylabel('S')
    plt.savefig(f'{filepath}/s_order.pdf')


#mda.Universe('../set1/1r4/SPCE_PORE_NVT_20_merged.psf','../set1/1r4/SPCE_PORE_NVT_20_BOX_0.xyz', all_coordinates = True)


psf_filename = 'SPCE_PORE_NVT_20_BOX_0.mol2'
pdb_filename = 'SPCE_PORE_NVT_20_BOX_0.mol2'
#calc_water_order_parameter( pdb_filename,psf_filename , [29.472,   29.777,   36.750 ], dim=2, filepath='../set1/1r4/')
calc_water_order_parameter( pdb_filename,psf_filename , [16.75,   36.750 ], dim=2, filepath='../set1/1r4/')