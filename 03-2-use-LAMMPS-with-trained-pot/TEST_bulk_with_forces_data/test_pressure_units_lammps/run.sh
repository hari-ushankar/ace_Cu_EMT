#!/bin/bash
export LD_LIBRARY_PATH=:$LD_LIBRARY_PATH:/home/hari/lammps/src
export PYTHONPATH="${PYTHONPATH}:/home/hari/lammps/python"
python3 trivial.py in
#python3 extract_data.py
