# ace_Cu_EMT_vacancy
Repo contains codes for three essential steps
1- create training data; 
2- fit a ACE model to that data; 
3- Evaluate  ACE pot using LAMMPS (needs work)

- Using ASE's EMT calculator; vacancy migration path is calculated using NEB and the final structures are outputted to .extxyz file
- Use ACE1pack to fit a ACE model to `vacancy, bulk and isolated atom` data
- (03-1 step) Check if your local LAMMPS installation has ML-PACE package[https://docs.lammps.org/Packages_details.html#pkg-ml-pace] installed properly.
- use the .yace file generated from step 2 to run a simple LAMMPS minimization of monovacancy in Cu [need to use the latest version of LAMMPS and install 2023 version of ML-PACE library]; this is a simple test that should yield the energy that is already in the training data.

 Although, the simulation using ACE potential itself throws out some weird behaviour! 

Each folder has a `bash` script that allows one to run each step. 
