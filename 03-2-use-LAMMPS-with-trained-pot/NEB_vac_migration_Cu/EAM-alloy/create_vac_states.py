import numpy as np
from ase.build import bulk
from ase.calculators.emt import EMT
from ase.eos import EquationOfState
from ase.io import read
from ase.io.trajectory import Trajectory
from ase.neb import NEB, NEBTools
from ase.units import kJ
from ase.visualize import view
from matplotlib import pyplot as plt
from ase.io import write

a_lat_Cu_EMT = 3.615
a1=bulk("Cu", "fcc", a=a_lat_Cu_EMT)
bulkCu = a1.repeat(6)
initial_struct = bulkCu.copy()
final_struct = bulkCu.copy()
initial_struct.pop(129)
final_struct.pop(130)
write('initial_new.lmp', initial_struct, format='lammps-data')
write('final.lmp', final_struct, format='lammps-data')


