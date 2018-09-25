#Scenario settings
scenario='swe'
target='release'
flux_solver='aug_riemann'
assertions=True
#For iMPI: use GNU, no OpenMP
compiler='gnu'
openmp='noomp'
mpi='impi' # to use the iMPI library
impi_on=True
impi_dir='.' # will read from $IMPIPATH
impi_nodeinfo=True
#Asagi setting
asagi=True
asagi_dir='.' # will check for $IMPIPATH
#Executable name
exe=scenario
if (impi_on):
    exe+='_impi_'
else:
    exe+='_mpi_'
exe+=target
