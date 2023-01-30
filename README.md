# ace_Cu_EMT_dataset_training

Repo contains codes for three essential steps
1- create training data; 
2- fit a ACE model to that data; 
3- Evaluate  ACE pot using LAMMPS (needs work)

- (01 step) Using ASE's EMT calculator; vacancy migration path is calculated using NEB and the final structures are outputted to .extxyz file
- (02 step)Use ACE1pack to fit a ACE model to the following structures:
  ```
  vacancy( 5 images + initial state), 
  bulk (4x4x4 reps of unit cell), 
  surfaces: fcc111 of reps of 2, 3, 4, 5 ,  
  isolated atom,
  clusters: icosahedron, octahedron
  twist sigma17 (001) GB
  tilt sigma17(014), sigma5(013) GB
  
  ```

 
 
- (03-1 step) Check if your local LAMMPS installation has ML-PACE package[https://docs.lammps.org/Packages_details.html#pkg-ml-pace] installed properly.
- (03-2 step) use the .yace file generated from step 02 to run a simple LAMMPS minimization of:
  -- monovacancy in Cu (minimization was ok) 
  -- sigma5(012) GB (minimization was ok)
  
  Note: need to use the latest version of LAMMPS and install 2023 version of ML-PACE library;
  TODO: 
- Need to think about now adding more structures in here. Maybe GBs and dislocations?
- ~~Use LAMMPS-python interface to run minimizations and output the final structures to .extxyz format~~

Each folder has a `bash` script that allows one to run python or Julia codes. 
