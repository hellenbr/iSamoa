#!/bin/bash
#@ wall_clock_limit = 24:00:00
#@ job_name = ebayes_irmfit_sb16n2t
#@ job_type = MPICH
#@ class = test
#@ output = $(jobid).log
#@ error = $(jobid).err
#@ node = 16
##Sandy Bridge nodes: 16 cores per node
#@ tasks_per_node = 2
#@ node_usage = not_shared
#@ energy_policy_tag = impi_tests
#@ minimize_time_to_solution = yes
#@ island_count = 1
#@ notification = always
#@ notify_user = hellenbr@in.tum.de
#@ queue

. /etc/profile
. /etc/profile.d/modules.sh
. $HOME/.bashrc  #This loads all iMPI related paths

#########################
# SET THIS CORRECTLY
#########################
BATCH_USER=di29zaf2
# Must be consistent with "node" and "tasks_per_node"
NUM_NODES=16
CORES_PER_NODE=2
# Make sure these paths are correct
DATAPATH=$SAMOADATADIR
execname=$IMPIPATH/darcy/darcy_impi_release

#########################
# Runtime Options
#########################
all=$execname
# iMPI adapt frequency (every N steps)
all=$all' -nimpiadapt 300'
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

#########################
# iMPI Processing for SB
#########################
# Rank range
MIN_RANKS=$CORES_PER_NODE
MAX_RANKS=$(($NUM_NODES * $CORES_PER_NODE))
# Extract the jobid
JOBID=$(echo $LOADL_STEP_ID| cut -d'.' -f 2)

# processing load-leveler host-file
cat $LOADL_HOSTFILE > host_file
echo "processing the Load Leveler provided hostfile "
echo "getting unique entries..."
awk '!a[$0]++' host_file > unique_hosts
cat unique_hosts > $LOADL_HOSTFILE
echo "new ll file:"
cat $LOADL_HOSTFILE 
echo "trimming the -ib part endings..."
rm -rf trimmed_unique_hosts
while read h; do
	echo $h | rev | cut -c 4- | rev >> trimmed_unique_hosts
done <unique_hosts

# generating slurm.conf dynamically
echo "copying initial slurm.conf work file"
cp -a $IMPIPATH/etc/slurm.conf.in slurm.conf.initial
cp -a $IMPIPATH/etc/slurm.conf.in slurm.conf.work
echo "setting up NodeName and PartitionName entries in slurm.conf ..."
while read h; do
	echo "NodeName=$h CPUs=${CORES_PER_NODE} State=UNKNOWN" >> slurm.conf.work
done <trimmed_unique_hosts
Nodes=`sed "N;s/\n/,/" trimmed_unique_hosts`
Nodes=`cat trimmed_unique_hosts | paste -sd "," -`
echo "PartitionName=local Nodes=${Nodes} Default=YES MaxTime=INFINITE State=UP" >> slurm.conf.work
FirstNode=`head -n 1 trimmed_unique_hosts`
echo "ControlMachine=${FirstNode}" >> slurm.conf.work
cp -a slurm.conf.work $IMPIPATH/etc/slurm.conf

# starting the resource manager (slurm)
echo "starting daemons on each given node..."
n=`wc -l <unique_hosts`
autonomous_master.ksh -n $n -c "$IMPIPATH/sbin/munged -Ff > munge_remote_daemon_out 2>&1" &
autonomous_master.ksh -n $n -c "$IMPIPATH/sbin/slurmd -Dc > slurm_remote_daemon_out 2>&1" &
echo "starting the controller..."
irtsched -Dcvvvv > slurm_controller_out 2>&1 &
sleep 5

echo "exporting recommended variable..."
export SLURM_PMI_KVS_NO_DUP_KEYS
export MXM_LOG_LEVEL=error
export SLURM_MPI_TYPE=pmi2

echo "--------------------------------------------------------------------------------"
echo " Starnig the application with srun:"
date

srun -n $MIN_RANKS $all > darcy.out

date
echo "--------------------------------------------------------------------------------"
