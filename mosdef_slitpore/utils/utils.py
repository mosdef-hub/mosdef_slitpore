import os
import numpy as np
from pkg_resources import resource_filename
from mdtraj.core.residue_names import _WATER_RESIDUES

def get_ff(filename):
    """Get path to a file in ffxml directory
    """
    file_path = resource_filename('mosdef_slitpore',
            os.path.join('ffxml', filename))

    return file_path

def get_bond_array(trj):
    """Get indices of water bonds from an MDTraj.trajectory

    Parameters
    ----------
    trj : MDTraj.trajectory
        Trajectory in which to get bond indices

    Returns
    -------
    bond_array : np.array(dtype=np.int32) of shape (n_bonds, 2)
        Array of bond indices
    """
    bond_array = list()
    water_res = [i for i in trj[0].topology.residues if i.name in _WATER_RESIDUES]
    # Assuming that O index is always 0, H is 1 and 2
    for res in water_res:
        atoms = [atom for atom in res.atoms]
        b1 = (atoms[0].index, atoms[1].index)
        b2 = (atoms[0].index, atoms[2].index)
        bond_array.append(b1)
        bond_array.append(b2)
    bond_array = np.asarray(bond_array, dtype=np.int32)

    return bond_array
