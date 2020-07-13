import numpy as np
import mbuild as mb

from foyer import Forcefield
from mosdef_slitpore.pores import graphene_surface
from mosdef_slitpore.utils.cassandra import spce_water
from mosdef_slitpore.utils.utils import get_ff
from mosdef_slitpore.utils.gromacs import write_ndx, add_settles

surface = graphene_surface()
x_length = np.max(surface.xyz[:, 0])
y_length = np.max(surface.xyz[:, 1])
z_length = np.max(surface.xyz[:, 2])

water = spce_water()
water.name = 'SOL'

water_region = mb.Box(
        mins=[0, 0, z_length+0.2],
        maxs=[x_length, y_length, z_length+2]
        )

water_box = mb.fill_box(water, box=water_region, density=1000)



ff = Forcefield(get_ff('pore-spce.xml'))

graphenePM = ff.apply(surface, residues='RES')
waterPM = ff.apply(water_box, residues='SOL')

system = graphenePM + waterPM

system.save('init.gro', combine='all', overwrite=True)
system.save('init.top', combine='all', overwrite=True)
system.save('init.mol2', overwrite=True)

add_settles('init.top')
write_ndx()
