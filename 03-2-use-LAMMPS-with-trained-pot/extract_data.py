#!/home/hari/miniconda3/envs/ase_env/bin/python
from ase.io import read
import numpy as np
from ase.io.extxyz import write_extxyz
#from ase.io.xyz import read_xyz
import lammps_logfile
from lammps import lammps

## run a lammps calculation
# infile = "in"
# lmp = lammps()
# print(lmp.version())
# lmp.file(infile)
# lmp.close()
# load the last frame of the dump file
dump = read("dump.out", format="lammps-dump-text", index=-1)

# get the pressures from log.lammps
lmp = lammps_logfile.File("log.lammps")
pxx = lmp.get("Pxx")[-1]
pyy = lmp.get("Pyy")[-1]
pzz = lmp.get("Pzz")[-1]
pyz = lmp.get("Pyz")[-1]
pxz = lmp.get("Pxz")[-1]
pxy = lmp.get("Pxy")[-1]
energy = lmp.get("PotEng")[-1]
energy = np.array(energy)
print(energy)
## need to check on the units! I guess LAMMPS deals with atomic style units; but what does ASE use?
stress = np.array([pxx, pyy, pzz, pyz, pxz, pxy])
## virial's array ordering based on Voigt notation:
## https://gitlab.com/ase/ase/-/blob/3.22.1/ase/io/extxyz.py#L519
## assign config_type and virial to the atoms
dump.info = {"config_type": "bulkCu", "virial": stress, "free_energy": energy}
write_extxyz(fileobj="dump_new.xyz", images=dump)
