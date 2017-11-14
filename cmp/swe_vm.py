target='release'
assertions=True
scenario='swe'
flux_solver='aug_riemann'
compiler='gnu'
#If enable iMPI, OpenMP must be disabled
openmp='noomp'
mpi='default'
impi=True
#Asagi on/off switch: accept True or False
asagi=True
#Use this asagi directory when using iMPI
asagi_dir='/media/data/emily/workspace/ihpcins'
#To run with normal MPI, must provide an asagi lib dir compiled with normal MPI
