#!/bin/bash

BASEPATH=$IMPIPATH/../esamoa
DATAPATH=$IMPIPATH/../samoa-data

# Number of processes to start
startprocs=2
# The name of the executable
execname=$BASEPATH/bin/darcy_mpi_release
# iMPI adapt frequency (every N steps)
nimpiadapt='-nimpiadapt 50'
# Grid maximum depth
dmax='-dmax 14'
# Simulation time in seconds (normally 3 hrs)
tmax='-tmax 172.8e6'
# VTK output frequency (every N seconds)
tout='-tout 86.4e3'
# Enable/disable VTK output
xmlout='-xmloutput .true.'
# Number of sections
sections='-sections 1'
# Number of threads
threads='-threads 1'
# The Courant number
courant='-courant 1.0'
# some threshold?
epsilon='-epsilon 1.0e-4'
# S reference threshold?
srefth='-S_ref_th 1.0e2'
# P reference threshold?
prefth='-p_ref_th 2.0e-8'
# Data file for displacement
fperm='-fperm '$DATAPATH'/darcy_five_spot/spe_perm_renamed.nc'
# Data file for bathymetry
fpor='-fpor '$DATAPATH'/darcy_five_spot/spe_phi_renamed.nc'
# Ouput directory
output_dir='-output_dir '$PWD
# Put all options together
all=$execname' '$nimpiadapt' '$dmax' '$tmax' '$tout' '$xmlout' '$sections' '$threads' '$courant' '$epsilon' '$srefth' '$prefth' '$fperm' '$fpor' '$output_dir


srun -n $startprocs $all > console.out

