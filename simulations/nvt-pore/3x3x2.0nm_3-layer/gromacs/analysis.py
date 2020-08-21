import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
from mosdef_slitpore.analysis import compute_density, compute_s

def number_density(nmols):
    dim = 1
    box_range = [0.837, 2.837]
    pore_center = (box_range[1]-box_range[0])/2 + box_range[0]
    o_densities = list()
    h_densities = list()
    fig, ax = plt.subplots()
    for trj in md.iterload(f'{nmols}_mols/sample.trr', top=f'{nmols}_mols/sample.gro', chunk=5000, skip=10001):
        print(trj)
        water_o = trj.atom_slice(trj.topology.select('name O'))
        water_h = trj.atom_slice(trj.topology.select('name H'))
        area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]
          
        for water_trj in (water_o, water_h):
            bins, density = compute_density(water_trj, area, dim, pore_center=pore_center, bin_width=0.01)
            label_name = list(set([i.name for i in water_trj.topology.atoms]))
            if label_name[0] == 'O':
                o_densities.append(density)
            else:
                h_densities.append(density)

    o_mean = np.mean(o_densities, axis=0)
    h_mean = np.mean(h_densities, axis=0)
    o_std = np.std(o_densities, axis=0)
    h_std = np.std(h_densities, axis=0)

    np.savetxt(f'{nmols}_mols/o_density.txt', np.transpose(np.vstack([bins, o_mean, o_std])),
               header='Bins\tDensity_mean\tDensity_std')

    np.savetxt(f'{nmols}_mols/h_density.txt', np.transpose(np.vstack([bins, h_mean, h_std])),
               header='Bins\tDensity_mean\tDensity_std')

    plt.plot(bins, o_mean, label='O')
    plt.fill_between(bins, o_mean + o_std, o_mean - o_std, alpha=0.2)
    plt.plot(bins, h_mean, label='H')
    plt.fill_between(bins, h_mean + h_std, h_mean - h_std, alpha=0.2)
    plt.xlabel('z-position (nm)')
    plt.ylabel('Number Density ($nm^-3$)')
    
    plt.legend()
    plt.savefig(f'{nmols}_mols/numberdensity.pdf')

def s_order(nmols):
    dim = 1
    box_range = [0.837, 2.837]
    pore_center = (box_range[1]-box_range[0])/2 + box_range[0]
    fig, ax = plt.subplots()
    s_list = list()
    for trj in md.iterload(f'{nmols}_mols/sample.trr', top=f'{nmols}_mols/init.mol2', chunk=5000, skip=10001):
        bins, s_values = compute_s(trj, dim, pore_center=pore_center)
        s_list.append(s_values)

    s_mean = np.mean(s_list, axis=0)
    s_std = np.std(s_list, axis=0)

    np.savetxt(f'{nmols}_mols/s_order.txt', np.transpose(np.vstack([bins, s_mean, s_std])),
               header='Bins\tS_mean\tS_std')
    plt.plot(bins, s_mean)
    plt.fill_between(bins, s_mean + s_std, s_mean - s_std, alpha=0.2)
    plt.xlabel('z-position (nm)')
    plt.ylabel('S')
    plt.savefig(f'{nmols}_mols/s_order.pdf')

for i in [485, 490, 495, 500]:
    s_order(i)
    number_density(i)
