#!/bin/bash
export PATH=/home/hari/lammps/src/:$PATH
export PATH=/usr/bin/:$PATH
export LD_LIBRARY_PATH=:$LD_LIBRARY_PATH:/home/hari/lammps/src
export PYTHONPATH="${PYTHONPATH}:/home/hari/lammps/python"
#lmp_mpi -h
#python3 trivial.py in
mpirun -np 7 lmp_mpi -partition 7x1 -in in.neb
