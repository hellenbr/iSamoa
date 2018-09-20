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
impi_dir='.' # will read from $IMPIPATH
impinodes=True
#Asagi setting
asagi=True
asagi_dir='.' # will check for $IMPIPATH
#Executable name
exe=scenario
if (impi):
    exe+='_impi_'
else:
    exe+='_mpi_'
exe+=target
