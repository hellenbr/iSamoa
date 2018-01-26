#Scenario settings
scenario='swe'
target='release'
flux_solver='aug_riemann'
assertions=True
#For iMPI: use GNU, no OpenMP, and MPI must set to default (MPICH)
compiler='gnu'
openmp='noomp'
mpi='default'
impi=True
impinodes=True
#Asagi setting
asagi=True
asagi_dir='/media/data/emily/workspace/ihpcins'
#Executable name
exe=scenario
if (impi):
    exe+='_impi'
else:
    exe+='_mpi'
exe+='_target'
