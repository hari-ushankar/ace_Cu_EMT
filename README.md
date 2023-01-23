# ace_Cu_EMT_vacancy

Repo contains codes for three essential steps
1- create training data; 
2- fit a ACE model to that data; 
3- Evaluate  ACE pot using LAMMPS (needs work)

- (01 step) Using ASE's EMT calculator; vacancy migration path is calculated using NEB and the final structures are outputted to .extxyz file
- (02 step)Use ACE1pack to fit a ACE model to `vacancy, bulk, surfaces` and `isolated atom` data
- (03-1 step) Check if your local LAMMPS installation has ML-PACE package[https://docs.lammps.org/Packages_details.html#pkg-ml-pace] installed properly.
- use the .yace file generated from step 2 to run a simple LAMMPS minimization of monovacancy in Cu [need to use the latest version of LAMMPS and install 2023 version of ML-PACE library]; this is a simple test that should yield the energy that is already in the training data.

TODO: Need to think about now adding more structures in here. Maybe GBs and dislocations?

Each folder has a `bash` script that allows one to run python or Julia codes. 
