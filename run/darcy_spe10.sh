#!/bin/bash

DATAPATH=$SAMOADATADIR
execname=$IMPIPATH/darcy/darcy_impi_release

# Number of processes to start
startprocs=2
# iMPI adapt frequency (every N steps)
nimpiadapt='-nimpiadapt 10'
# iMPI host file (effective only if impi nodes output is enabled)
fimpihosts='-fimpihosts '$PWD/unique_host
# Grid maximum depth (14)
dmax='-dmax 11'
# Simulation time in sec (default 172,800,000 for 2000 days)
tmax='-tmax 172.8e6'
# VTK output frequency in sec (default 86400 for every 1 day)
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
mkdir -p $PWD/output
output_dir='-output_dir '$PWD/output
# Put all options together
all=$execname' '$nimpiadapt' '$fimpihosts' '$dmax' '$tmax' '$tout' '$xmlout' '$sections' '$threads' '$courant' '$epsilon' '$srefth' '$prefth' '$fperm' '$fpor' '$output_dir


srun -n $startprocs -o darcy.out $all

