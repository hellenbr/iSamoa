target='release'
assertions=True
scenario='swe'
flux_solver='aug_riemann'
compiler='gnu'
#if enable iMPI, OpenMP must be disabled
openmp='noomp'
mpi='default'
impi='no'
#asagi on/off switch: accept True or False
asagi=True
#use this asagi directory when using iMPI
asagi_dir='/home/emily/nfs/workspace/libasagi'
#use this asagi directory when using normal MPI
#asagi_dir='/media/DATA/install/libasagi'
