## Checking lattice constant of Cu in EMT calculator

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

a = 3.6  # approximate lattice constant
b = a / 2
cu = Atoms(
    "Cu", cell=[(0, b, b), (b, 0, b), (b, b, 0)], pbc=1, calculator=EMT()
)  # use EMT potential
cell = cu.get_cell()
traj = Trajectory("Cu.traj", "w")
for x in np.linspace(0.95, 1.05, 5):
    cu.set_cell(cell * x, scale_atoms=True)
    cu.get_potential_energy()
    traj.write(cu)


configs = read("Cu.traj@0:5")  # read 5 configurations
# Extract volumes and energies:
volumes = [ag.get_volume() for ag in configs]
energies = [ag.get_potential_energy() for ag in configs]
eos = EquationOfState(volumes, energies)
v0, e0, B = eos.fit()
print(B / kJ * 1.0e24, "GPa")
a_lat_Cu_EMT = (4 * 11.567) ** (1 / 3)
# (169 + 2*122) / 3 ## (c11 + 2*c12) /3; data from Mishin EAM @ NIST

## Create NEB images and find MEP for vacancy migration

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
## Isolated Cu atom
one_atom = bulk("Cu", "fcc", a=3.59)
one_atom.calc = EMT()
one_atom.cell[0][1] += 15
one_atom.cell[0][2] += 15
one_atom.cell[1][0] += 15
one_atom.cell[1][2] += 15
one_atom.cell[2][0] += 15
one_atom.cell[2][1] += 15
print(one_atom.get_potential_energy())

## create extxyz with additional tag: config_type

from ase.io.extxyz import write_extxyz

for img in images:
    img.info = {"config_type": "bulk_vac_images"}
write_extxyz(fileobj="images.xyz", images=images)
initial_struct.info = {"config_type": "bulk_vac"}
write_extxyz(fileobj="initial.xyz", images=initial_struct)
bulkCu.info = {"config_type": "bulk_Cu"}
write_extxyz(fileobj="bulk.xyz", images=bulkCu)
one_atom.info = {"config_type": "isolated_atom"}
write_extxyz(fileobj="one_atom.xyz", images=one_atom)
# collect all train data into one file!
filenames = ["images.xyz", "initial.xyz", "bulk.xyz", "one_atom.xyz"]
with open("master.xyz", "w") as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
## add in fcc111 surfaces of different sizes in training data
from ase.build import fcc111

slab = fcc111('Cu', size=(3,3,3), vacuum=10.0)
sname = "fcc11_3_3_3_vac10"

slab.calc = EMT()
optimizer = MDMin(slab)
optimizer.run()
slab.info = {"config_type": sname}
write_extxyz(fileobj="{}.xyz".format(sname), images=slab)
filenames = ["{}.xyz".format(sname)]
with open("master.xyz", "a") as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())

slab = fcc111('Cu', size=(2,2,2), vacuum=10.0)
sname = "fcc11_2_2_2_vac10"
slab.calc = EMT()
optimizer = MDMin(slab)
optimizer.run()
slab.info = {"config_type": sname}
write_extxyz(fileobj="{}.xyz".format(sname), images=slab)
filenames = ["{}.xyz".format(sname)]
with open("master.xyz", "a") as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())

slab = fcc111('Cu', size=(4,4,4), vacuum=10.0)
sname = "fcc11_4_4_4_vac10"
slab.calc = EMT()
optimizer = MDMin(slab)
optimizer.run()
slab.info = {"config_type": sname}
write_extxyz(fileobj="{}.xyz".format(sname), images=slab)
filenames = ["{}.xyz".format(sname)]
with open("master.xyz", "a") as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
slab = fcc111('Cu', size=(5,5,5), vacuum=10.0)
sname = "fcc11_5_5_5_vac10"
slab.calc = EMT()
optimizer = MDMin(slab)
optimizer.run()
slab.info = {"config_type": sname}
write_extxyz(fileobj="{}.xyz".format(sname), images=slab)
filenames = ["{}.xyz".format(sname)]
with open("master.xyz", "a") as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())