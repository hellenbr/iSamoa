#!/bin/bash

# The name of the executable
execname="$1"

# Number of starting ranks (=num_cores_per_node)
numranks="$2"

# Batch job ID
jobid="$3"

# Number of sections
sections='-sections 1'

# Allow splitting sections during load balancing
split='-lbsplit'

# The Courant number (keep it 0.95)
courant='-courant 0.95'

# Number of threads
threads='-threads 1'

# Enable VTK output
xmlout='-xmloutput .true.'

# VTK output frequency (every N seconds)
tout='-tout 120'

# iMPI adapt frequency (every N steps)
nimpiadapt='-nimpiadapt 50'

# Grid minimum depth
dmin='-dmin 8'

# Grid maximum depth
dmax='-dmax 28'

# Simulation time in seconds (normally 3 hrs)
tmax='-tmax 10800'

# Data file for displacement
fdispl='-fdispl /home/hpc/h039w/di29zaf2/ihpc_workspace/samoa-data/tohoku_static/displ.nc'

# Data file for bathymetry
fbath='-fbath /home/hpc/h039w/di29zaf2/ihpc_workspace/samoa-data/tohoku_static/bath_2014.nc'

# What is stestpoints (for Tohoku only)??
stestpoints='-stestpoints "545735.266126 62716.4740303,935356.566012 -817289.628677,1058466.21575 765077.767857"' 

# Ouput directory
outdir='/home/hpc/h039w/di29zaf2/ihpc_output/'$jobid
if [[ $execname == *"impi"* ]]; then
	outdir+='_swe_impi'
else
	outdir+='_swe_mpi'
fi
rm -rf $outdir
mkdir $outdir
output_dir='-output_dir '$outdir

# Put all options together
all=$sections' '$split' '$courant' '$threads' '$tout' '$nimpiadapt' '$dmin' '$dmax' '$tmax' '$fdispl' '$fbath' '$xmlout' '$stestpoints' '$output_dir

#mpiexec -n 4 $execname $all >> console.out
srun -n $numranks $execname $all > ${jobid}_console.log
