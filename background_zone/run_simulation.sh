#!/bin/bash

# Go to background_zone directory and set up the background mesh
cd ../background_zone
./Allclean
blockMesh
#topoSet -dict system/topoSetDictR2 | tee log.topoSet
topoSet -dict system/topoSetDict | tee log.topoSet
mv log.topoSet log.topoSet1
#refineMesh -dict system/refineMeshDict2 -overwrite
checkMesh
cp -r 0.orig/. 0/
touch mesh_background.foam

# Go to component_zone and set up the component mesh
cd ../component_zone
./Allclean
blockMesh
surfaceFeatureExtract 
#sed -i "/numberOfSubdomains/s/[0-9]\+/$1/g" system/decomposeParDict
decomposePar
mpirun -np 32 snappyHexMesh -parallel -overwrite
#srun -n"$1" snappyHexMesh -parallel -overwrite
reconstructParMesh -constant
topoSet
checkMesh
touch mesh_component.foam

# Merge component and background meshes and finalize setup
cd ../background_zone
mergeMeshes . ../component_zone -overwrite
topoSet -dict system/topoSetDict | tee log.topoSet
mv log.topoSet log.topoSet2
setFields
checkMesh
touch mesh_assembled.foam

# Decompose domain and run simulation
#sed -i "/numberOfSubdomains/s/[0-9]\+/$1/g" system/decomposeParDict
decomposePar
mpirun -np 32 overPimpleDyMFoam -parallel | tee log.simulation
#srun -n"$1" overPimpleDyMFoam -parallel | tee $WORK/LOLLI/log.seed_6dof"$1"

# Reconstruct final mesh and open ParaView for visualization
# reconstructPar
# paraFoam
