#!/bin/bash

DATAPATH=$(dirname $IMPIPATH)/samoa-data

# Number of processes to start
startprocs=2
# The name of the executable
execname=$(dirname $IMPIPATH)/gh_esamoa/bin/swe_impi_release
# iMPI adapt frequency (every N steps)
nimpiadapt='-nimpiadapt 100'
# iMPI host file (effective only if impi nodes output is enabled)
fimpihosts='-fimpihosts '$PWD/unique_hosts
# Grid minimum depth
dmin='-dmin 8'
# Grid maximum depth
dmax='-dmax 22'
# Simulation time in seconds
# (default 10800 for 3 hrs, 14400 for 4 hrs, 18000 for 5 hrs)
tmax='-tmax 10800'
# VTK output frequency (every N seconds)
tout='-tout 120'
# Enable/disable VTK output
xmlout='-xmloutput .true.'
# Number of sections
sections='-sections 1'
# Allow splitting sections during load balancing
split='-lbsplit'
# Number of threads
threads='-threads 1'
# The Courant number (keep it 0.95)
courant='-courant 0.95'
# Data file for displacement
fdispl='-fdispl '$DATAPATH'/tohoku_static/displ.nc'
# Data file for bathymetry
fbath='-fbath '$DATAPATH'/tohoku_static/bath_2014.nc'
# What is stestpoints
stestpoints='-stestpoints "545735.266126 62716.4740303,935356.566012 -817289.628677,1058466.21575 765077.767857"' 
# Ouput directory
mkdir -p $PWD/output
output_dir='-output_dir '$PWD/output
# Put all options together
all=$execname' '$nimpiadapt' '$fimpihosts' '$dmin' '$dmax' '$tmax' '$tout' '$xmlout' '$sections' '$split' '$threads' '$courant' '$fdispl' '$fbath' '$stestpoints' '$output_dir


srun -n $startprocs -o swe.out $all
