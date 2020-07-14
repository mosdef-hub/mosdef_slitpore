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
    
    fig, ax = plt.subplots()
    ax.plot(bins-gph_max, rho[0])
    plt.xlabel('z-position (nm)')
    plt.ylabel('Number Density (1/nm^3)')
    plt.xlim((0, 1.5))

    plt.savefig('numberdensity.pdf')

number_density()
