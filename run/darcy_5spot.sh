#!/bin/bash

#===============
# Set these
#===============
DATAPATH=$SAMOADATADIR
execname=$IMPIPATH/darcy/darcy_impi_release
# Number of processes to start
startprocs=2


#==================
# Runtime Options
#==================
all=$execname
# iMPI adapt frequency (every N steps)
all=$all' -nimpiadapt 500'
# iMPI host file (effective only if impi nodes output is enabled)
all=$all' -fimpihosts '$PWD/unique_hosts
# Grid maximum depth (set 16 ~= 5000 cells)
all=$all' -dmax 16'
# Simulation time in sec (default 172,800,000 for 2000 days)
all=$all' -tmax 63.072e6' # for 730 days (2 yrs)
# VTK output frequency in sec (default 86400 for every 1 day)
all=$all' -tout 86.4e3'
# Enable/disable VTK output
all=$all' -xmloutput .true.'
# Number of sections per thread/rank
all=$all' -sections 1'
# Allow splitting sections during load balancing (if not, load won't distribute)
all=$all' -lbsplit'
# Number of threads per rank
all=$all' -threads 1'
# The Courant number
all=$all' -courant 1.0'
# some threshold?
all=$all' -epsilon 1.0e-4'
# S reference threshold?
all=$all' -S_ref_th 1.0e2'
# P reference threshold?
all=$all' -p_ref_th 2.0e-8'
# Data file for displacement
all=$all' -fperm '$DATAPATH'/darcy_five_spot/spe_perm_renamed.nc'
# Data file for bathymetry
all=$all' -fpor '$DATAPATH'/darcy_five_spot/spe_phi_renamed.nc'
# Ouput directory
mkdir -p $PWD/output
all=$all' -output_dir '$PWD/output


#==================
# Launch
#==================
srun -n $startprocs -o darcy.out $all

