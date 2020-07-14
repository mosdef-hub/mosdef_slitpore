import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
from ramtools.structure.calc_number_density import calc_number_density

def number_density():
    """Calculate number density function of water on graphene surface"""
    trj = md.load('nvt.trr', top='nvt.gro')[5000:]

    gph_trj = trj.atom_slice(trj.topology.select('resname RES'))
    gph_max = np.max(gph_trj.xyz[:,:,2])
    area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][1]
    dim = 2
    box_range = [0.67, 3]
    
    n_bins=150
    
    rho, bins, res = calc_number_density(trj, area, dim, box_range, n_bins)
    r_min, rho_min = find_local_minima(bins, rho[0], 0.5)
    
    fig, ax = plt.subplots()
    ax.plot(bins-gph_max, rho[0])
    ax.scatter(r_min-gph_max, rho_min, color='k', marker='o')
    plt.text(0.5, 10, f'r_min = {(r_min-gph_max):.3f}')
    plt.xlabel('z-position (nm)')
    plt.ylabel('Number Density (1/nm^3)')
    plt.xlim((0, 1.5))

    plt.savefig('numberdensity.pdf')

def find_local_minima(r, y, r_guess):
    """Find the local minima nearest a guess value of r
    Grabbed from: https://github.com/mattwthompson/scattering
    """
    all_minima = find_all_minima(y)
    nearest_minima, _ = find_nearest(r[all_minima], r_guess)
    return r[all_minima[nearest_minima]], y[all_minima[nearest_minima]]

def find_all_minima(arr):
    """
    Find all local minima in a 1-D array, defined as value in which each
    neighbor is greater. See https://stackoverflow.com/a/4625132/4248961
    Grabbed from: https://github.com/mattwthompson/scattering
    Parameters
    ----------
    arr : np.ndarray
        1-D array of values
    Returns
    -------
    minima : np.ndarray
        indices of local minima
    """

    checks = np.r_[True, arr[1:] < arr[:-1]] & np.r_[arr[:-1] < arr[1:], True]
    minima = np.where(checks)[0]
    return minima

def find_nearest(arr, val):
    """
    Find index in an array nearest some value.
    See https://stackoverflow.com/a/2566508/4248961
    Grabbed from: https://github.com/mattwthompson/scattering
    """

    arr = np.asarray(arr)
    idx = (np.abs(arr - val)).argmin()
    return idx, arr[idx]

number_density()
