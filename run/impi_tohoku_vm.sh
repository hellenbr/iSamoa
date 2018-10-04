#!/bin/bash

#===============
# Set these
#===============
DATAPATH=$SAMOADATADIR
execname=$IMPIPATH/swe/swe_impi_release
# Number of processes to start
startprocs=2


#==================
# Runtime Options
#==================
all=$execname
# iMPI adapt frequency (every N steps)
all=$all' -nimpiadapt 100'
# iMPI host file (effective only if impi nodes output is enabled)
all=$all' -fimpihosts '$PWD/unique_hosts
# Grid maximum depth (14)
all=$all' -dmin 8'
# Grid maximum depth (14)
all=$all' -dmax 22'
# Simulation time in sec (default 10800 for 3 hrs, 14400 for 4 hrs, 18000 for 5 hrs)
all=$all' -tmax 10800'
# VTK output frequency in sec (every N seconds)
all=$all' -tout 120'
# Enable/disable VTK output
all=$all' -xmloutput .true.'
# Number of sections per thread/rank
all=$all' -sections 1'
# Allow splitting sections during load balancing (if not, load won't distribute)
all=$all' -lbsplit'
# Number of threads per rank
all=$all' -threads 1'
# The Courant number (keep it 0.95 for SWE)
all=$all' -courant 0.95'
# Data file for displacement
all=$all' -fdispl '$DATAPATH'/tohoku_static/displ.nc'
# Data file for bathymetry
all=$all' -fbath '$DATAPATH'/tohoku_static/bath_2014.nc'
# Points for the point output (must enable point output, otherwise iMPI won't work)
all=$all' -stestpoints "545735.266126 62716.4740303,935356.566012 -817289.628677,1058466.21575 765077.767857"'
# Ouput directory
mkdir -p $PWD/output
all=$all' -output_dir '$PWD/output


#==================
# Launch
#==================
srun -n $startprocs -o swe.out $all
