import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
from mosdef_slitpore.analysis import compute_density, compute_s, compute_mol_per_area

def number_density(nmols, box_range):
    trj = md.load(f'{nmols}_mols/sample.trr', top=f'{nmols}_mols/sample.gro')
    
    water_o = trj.atom_slice(trj.topology.select('name O'))
    water_h = trj.atom_slice(trj.topology.select('name H'))
    area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]
    dim = 1
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

def s_order(nmols, box_range):
    trj = md.load(f'{nmols}_mols/sample.trr', top=f'{nmols}_mols/init.mol2')
    dim = 1
    pore_center = (box_range[1]-box_range[0])/2 + box_range[0]

    fig, ax = plt.subplots()
    bins, s_values = compute_s(trj, dim, pore_center=pore_center)
    plt.plot(bins, s_values)

    plt.xlabel('z-position (nm)')
    plt.ylabel('S')
    plt.savefig(f'{nmols}_mols/s_order.pdf')

def area(nmols, cutoff, box_range):
    """Calculate molecules of water per area on graphene surface"""
    trj = md.load(f'{nmols}_mols/sample.trr', top=f'{nmols}_mols/sample.gro')[5000:]

    area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]
    dim = 1
    
    n_bins=200
   
    fig, ax = plt.subplots()
    areas, bins, res = compute_mol_per_area(trj, area, dim, box_range, n_bins, shift=False)

    cutoff_indices = np.where(bins < bins[0] + cutoff)
    area_sum = sum(areas[0][:cutoff_indices[0][-1]])

    cumsum = np.cumsum(areas[0])
    new_bins = [bi -box_range[0] for bi in bins]
    plt.plot(new_bins, cumsum)
    plt.scatter(bins[cutoff_indices[0][-1]]-box_range[0], area_sum)
    plt.text(1.2, 5, f'n_molecules = {(area_sum):.3f}')
    plt.xlabel('z-position (nm)')
    plt.ylabel('cumulative sum of molecules')
    plt.savefig(f'{nmols}_mols/cumsum.pdf')

number_density(23, box_range = [0.167, 1.167])
