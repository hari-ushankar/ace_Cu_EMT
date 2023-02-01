import numpy as np
from ase import Atoms
from ase.build import bulk
from ase.calculators.emt import EMT
from ase.eos import EquationOfState
from ase.io import read
from ase.io.trajectory import Trajectory
from ase.neb import NEB, NEBTools
from ase.optimize import MDMin
from ase.units import kJ
from ase.visualize import view
from matplotlib import pyplot as plt
import numpy as np
## Create NEB images and find MEP for vacancy migration
a_lat_Cu_EMT = (4 * 11.567) ** (1 / 3)
a1 = bulk("Cu", "fcc", a=a_lat_Cu_EMT)
bulkCu = a1.repeat(6)
bulkCu.calc = EMT()
imgs = 5
# create initial and final structures for vac migration
initial_struct = bulkCu.copy()
final_struct = bulkCu.copy()
initial_struct.pop(129)  # we went from 0 to 129 to pick from the center
final_struct.pop(130)

# relax initial and final structures using a calculator
initial_struct.calc = EMT()
optimizer = MDMin(initial_struct)
optimizer.run()
final_struct.calc = EMT()
optimizer = MDMin(final_struct)
optimizer.run()

# create images using in-built NEB inside ASE

images = [initial_struct]
images += [initial_struct.copy() for i in range(imgs)]
images += [final_struct]
neb = NEB(images)
# Interpolate linearly the potisions of the three middle images:
neb.interpolate()
# set calculator for each image!
for image in images[1 : imgs + 1]:
    image.calc = EMT()
# Optimize:
optimizer = MDMin(neb, trajectory="A2B.traj")
optimizer.run(fmax=0.01)
q = NEBTools(images)
e_m_vac = q.get_barrier()
vac_e = initial_struct.get_potential_energy()
bulk_e = bulkCu.get_potential_energy()
e_vac_f = vac_e - 215 / 216 * bulk_e
print("Vacancy formation energy in bulk Cu: {} eV".format(round(e_vac_f, 2)))
print("Vacancy migration energy in bulk Cu: {} eV".format(round(e_m_vac[0], 2)))
