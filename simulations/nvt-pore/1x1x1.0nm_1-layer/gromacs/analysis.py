import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt
import signac
import os
from mosdef_slitpore.analysis import compute_density, compute_s

project = signac.get_project()

def number_density(job):
    dim = 1
    box_range = [0.167, 1.167]
    pore_center = (box_range[1]-box_range[0])/2 + box_range[0]
    o_densities = list()
    h_densities = list()
    fig, ax = plt.subplots()
    for trj in md.iterload(os.path.join(job.ws, 'nvt.trr'), top=os.path.join(job.ws, 'nvt.gro'), chunk=5000, skip=5001):
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

    plt.plot(bins, o_mean, label='O')
    plt.fill_between(bins, o_mean + o_std, o_mean - o_std, alpha=0.2)
    plt.plot(bins, h_mean, label='H')
    plt.fill_between(bins, h_mean + h_std, h_mean - h_std, alpha=0.2)
    plt.xlabel('z-position (nm)')
    plt.ylabel('Number Density ($nm^-3$)')
    
    plt.legend()
    with job:
       np.savetxt('o_density.txt', np.transpose(np.vstack([bins, o_mean, o_std])),
                  header='Bins\tDensity_mean\tDensity_std')

       np.savetxt('h_density.txt', np.transpose(np.vstack([bins, h_mean, h_std])),
                  header='Bins\tDensity_mean\tDensity_std')
       plt.savefig('numberdensity.pdf')
    np.savetxt(f'data/{job.sp.nwater}_mol_o_density.txt', np.transpose(np.vstack([bins, o_mean, o_std])),
               header='Bins\tDensity_mean\tDensity_std')

    np.savetxt(f'data/{job.sp.nwater}_mol_h_density.txt', np.transpose(np.vstack([bins, h_mean, h_std])),
               header='Bins\tDensity_mean\tDensity_std')

def s_order(job):
    dim = 1
    box_range = [0.167, 1.167]
    pore_center = (box_range[1]-box_range[0])/2 + box_range[0]
    fig, ax = plt.subplots()
    s_list = list()
    for trj in md.iterload(os.path.join(job.ws, 'nvt.trr'), top=os.path.join(job.ws, 'init.mol2'), chunk=5000, skip=5001):
        bins, s_values = compute_s(trj, dim, pore_center=pore_center, bin_width=0.01)
        s_list.append(s_values)

    s_mean = np.mean(s_list, axis=0)
    s_std = np.std(s_list, axis=0)

    plt.plot(bins, s_mean)
    plt.fill_between(bins, s_mean + s_std, s_mean - s_std, alpha=0.2)
    plt.xlabel('z-position (nm)')
    plt.ylabel('S')

    with job:
        plt.savefig('s_order.pdf')

        np.savetxt('s_order.txt', np.transpose(np.vstack([bins, s_mean, s_std])),
                   header='Bins\tS_mean\tS_std')
    np.savetxt(f'data/{job.sp.nwater}_mol_s_order.txt', np.transpose(np.vstack([bins, s_mean, s_std])),
               header='Bins\tS_mean\tS_std')

def area(job):
    """Calculate molecules of water per area on graphene surface"""
    with job:
        trj = md.load('sample.trr', top='sample.gro')[5000:]

    box_range = [0.167, 1.167]
    area = trj.unitcell_lengths[0][0] * trj.unitcell_lengths[0][2]
    dim = 1
    
    n_bins=200
   
    fig, ax = plt.subplots()
    areas, bins = compute_mol_per_area(trj, area, dim, box_range, n_bins, shift=False)

    cutoff_indices = np.where(bins < bins[0] + cutoff)
    area_sum = sum(areas[:cutoff_indices[0][-1]])

    cumsum = np.cumsum(areas)
    new_bins = [bi -box_range[0] for bi in bins]
    plt.plot(new_bins, cumsum)
    plt.scatter(bins[cutoff_indices[0][-1]]-box_range[0], area_sum)
    plt.text(0.5, 5, f'n_molecules = {(area_sum):.3f}')
    plt.xlabel('z-position (nm)')
    plt.ylabel('cumulative sum of molecules')
    with job:
        plt.savefig('cumulative_area.pdf')

if __name__ == '__main__':
    for job in project.find_jobs({"nwater": 24}):
        number_density(job)
        s_order(job)
