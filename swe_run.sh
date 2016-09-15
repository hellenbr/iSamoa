#!/bin/bash

# The name of the executable
execname="$1"

# Number of sections
sections=''
sections+='-sections 1'

# Allow splitting sections during load balancing
split=''
split+='-lbsplit'

# The Courant number (keep it 0.95)
courant=''
courant+='-courant 0.95'

# Number of threads
threads=''
threads+='-threads 1'

# VTK output frequency (every N sections)
tout=''
tout+='-tout 120'

# Grid minimum depth
dmin=''
dmin+='-dmin 0'

# Grid maximum depth
dmax=''
dmax+='-dmax 20'

# Simulation time in seconds (normally 3 hrs)
tmax=''
tmax+='-tmax 10800'

# Data file for displacement
fdispl=''
fdispl+='-fdispl /home/emily/nfs/workspace/samoa-data/tohoku_static/displ.nc'

# Data file for bathymetry
fbath=''
fbath+='-fbath /home/emily/nfs/workspace/samoa-data/tohoku_static/bath_2014.nc'

# Enable VTK output
xmlout=''
xmlout+='-xmloutput .true.'

# What is stestpoints (for Tohoku only)??
stestpoints=''
stestpoints+='-stestpoints "545735.266126 62716.4740303,935356.566012 -817289.628677,1058466.21575 765077.767857"' 

# Ouput directory
outdir='/home/emily/nfs/workspace/isamoa/output/swe_impi'
rm -rf $outdir
mkdir $outdir
output_dir='-output_dir '$outdir

# Put all options together
all=$sections' '$split' '$courant' '$threads' '$tout' '$dmin' '$dmax' '$tmax' '$fdispl' '$fbash' '$xmlout' '$stestpoints' '$output_dir


#mpiexec -n 4 $execname $all >> console.out
srun -n 2 $execname $all > console.out

