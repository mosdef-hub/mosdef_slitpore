import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
from mosdef_slitpore.analysis import compute_density, compute_s

def number_density(nmols):
    trj = md.load(f'{nmols}_mols/sample.trr', top=f'{nmols}_mols/sample.gro')
    
    water_o = trj.atom_slice(trj.topology.select('name O'))
    water_h = trj.atom_slice(trj.topology.select('name H'))
    area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]
    dim = 1
    box_range = [0.837, 2.837]
    pore_center = (box_range[1]-box_range[0])/2 + box_range[0]
    
    fig, ax = plt.subplots()
    for water_trj in (water_o, water_h):
        bins, density = compute_density(water_trj, area, dim, pore_center=pore_center)
        label_name = list(set([i.name for i in water_trj.topology.atoms]))
        plt.plot(bins, density, label=label_name[0])
    
    plt.xlabel('z-position (nm)')
    plt.ylabel('Number Density ($nm^-3$)')
    
    plt.legend()
    plt.savefig(f'{nmols}_mols/numberdensity.pdf')

def s_order(nmols):
    trj = md.load(f'{nmols}_mols/sample.trr', top=f'{nmols}_mols/init.mol2')
    dim = 1
    box_range = [0.837, 2.837]
    pore_center = (box_range[1]-box_range[0])/2 + box_range[0]

    fig, ax = plt.subplots()
    bins, s_values = compute_s(trj, dim, pore_center=pore_center)
    plt.plot(bins, s_values)

    plt.xlabel('z-position (nm)')
    plt.ylabel('S')
    plt.savefig(f'{nmols}_mols/s_order.pdf')

for i in [485, 490, 495, 500]:
    s_order(i)
    number_density(i)
