#!/bin/bash

export NFSPATH=$HOME/workspace


# The name of the executable
execname=$NFSPATH/esamoa/bin/swe_noomp_impi_gnu_release
# Number of starting ranks (=num_procs_per_node)
numranks=2

# Number of sections
sections='-sections 1'
# Allow splitting sections during load balancing
split='-lbsplit'
# The Courant number (keep it 0.95)
courant='-courant 0.95'
# Number of threads
threads='-threads 1'
# VTK output frequency (every N seconds)
tout='-tout 120'
# iMPI adapt frequency (every N steps)
nimpiadapt='-nimpiadapt 50'
# Grid minimum depth
dmin='-dmin 8'
# Grid maximum depth
dmax='-dmax 22'
# Simulation time in seconds (normally 3 hrs)
tmax='-tmax 3600'
# Data file for displacement
fdispl='-fdispl '$NFSPATH'/samoa-data/tohoku_static/displ.nc'
# Data file for bathymetry
fbath='-fbath '$NFSPATH'/samoa-data/tohoku_static/bath_2014.nc'
# Enable/disable VTK output
xmlout='-xmloutput .false.'
# What is stestpoints
stestpoints='-stestpoints "545735.266126 62716.4740303,935356.566012 -817289.628677,1058466.21575 765077.767857"' 
# Ouput directory
outdir=$NFSPATH'/esamoa'
if [[ $execname == *"impi"* ]]; then
	outdir+='/out_swe_impi'
else
	outdir+='/out_swe_mpi'
fi
mkdir -p $outdir
rm -rf $outdir/*
output_dir='-output_dir '$outdir
# Put all options together
all=$sections' '$split' '$courant' '$threads' '$tout' '$nimpiadapt' '$dmin' '$dmax' '$tmax' '$fdispl' '$fbath' '$xmlout' '$stestpoints' '$output_dir

#mpiexec -n 4 $execname $all >> console.out
srun -n $numranks $execname $all > $outdir/console.out
