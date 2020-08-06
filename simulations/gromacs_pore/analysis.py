import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
from ramtools.structure.calc_number_density import calc_number_density
from ramtools.structure.calc_angle_distribution import calc_water_angle, calc_water_order_parameter

def number_density(nmols):
    """Calculate number density function of water on graphene surface"""
    trj = md.load(f'{nmols}_mols/nvt.trr', top=f'{nmols}_mols/nvt.gro')[5000:]

    gph_trj = trj.atom_slice(trj.topology.select('resname RES'))
    area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]
    dim = 1
    box_range = [0.837, 2.837]
    
    n_bins=200
    water_o = trj.atom_slice(trj.topology.select('name O'))
    water_h = trj.atom_slice(trj.topology.select('name H'))
   
    fig, ax = plt.subplots()
    for water_trj in [water_o, water_h]: 
        rho, bins, res = calc_number_density(water_trj, area, dim, box_range, n_bins)
       
        label_name = list(set([i.name for i in water_trj.topology.atoms]))
        ax.plot(bins, rho[0], label=label_name[0])

    plt.xlabel('z-position (nm)')
    plt.ylabel('Number Density ($nm^-3$)')
 
    plt.legend()
    plt.savefig(f'{nmols}_mols/numberdensity.pdf')

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
for i in [485, 490, 495, 500]:
    #number_density(i)
    #calc_water_angle('nvt_chunk.trr', 'init.mol2', cutoff=(1.5+0.75)*10, dim=1, filepath=f'{i}_mols')
    calc_water_order_parameter('nvt.trr', 'init.mol2', cutoffs=[8.37+3, 28.37-3], dim=1, filepath=f'{i}_mols')
