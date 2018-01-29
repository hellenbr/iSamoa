#Scenario settings
scenario='darcy'
target='release'
flux_solver='upwind'
layers=85
perm_averaging='geometric'
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
    exe+='_impi_'
else:
    exe+='_mpi_'
exe+=target
