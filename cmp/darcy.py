#Executable name
exe='darcy_mpi_release'
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
impi=False
#Asagi setting
asagi=True
asagi_dir='/media/data/emily/workspace/ihpcins'

