#Scenario settings
scenario='swe'
target='release'
flux_solver='aug_riemann'
assertions=True
#For iMPI: use GNU, no OpenMP
compiler='gnu'
openmp='noomp'
# Which MPI library to use
# (setting it to impi will use the MPI library install at $IMPIPATH)
mpi='impi'
impi_on=True    # Enable iMPI
#impi_on=False   # Disable iMPI
impi_dir='.' # will read from $IMPIPATH
impi_nodeinfo=True
#Asagi setting
asagi=True
asagi_dir='.' # will check for $IMPIPATH
#Executable name
exename=scenario
if (impi_on):
    exename+='_impi_'
else:
    exename+='_mpi_'
exename+=target
