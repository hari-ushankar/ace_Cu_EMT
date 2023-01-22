# ace_Cu_EMT_vacancy
Repo contains codes for three essential steps
1- create training data; 
2- fit a ACE model to that data; 
3-Evaluate  ACE pot using LAMMPS (needs work)

- Using ASE's EMT calculator; vacancy migration path is calculated using NEB and the final structures are outputted to .extxyz file
- Use ACE1pack to fit a ACE model to `vacancy, bulk and isolated atom` data
- (this does not work for now..) use the .yace file to run a simple LAMMPS minimization of monovacancy in Cu
