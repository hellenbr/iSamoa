# iMPI Installation on Virtual Machine Cluster

This is a step-by-step guide for setting up a VM cluster with iMPI installed on it. We use [Oracle VirtualBox](https://www.virtualbox.org/).

The cluster consists of 1 controller node (which runs the SLURM controller daemon) and N worker nodes (which do the actual computation work). N can be any number the user desires or the host machine can handle.

In this guide, we use the following node configuration -- [Host name] : [IP Assignment]

* node0 : 10.0.0.1
* node1 : 10.0.0.2
* node2 : 10.0.0.3
* node3 : 10.0.0.4
* node4 : 10.0.0.5
* node5 : 10.0.0.6
* node6 : 10.0.0.7
* node7 : 10.0.0.8
* controller : 10.0.0.9
* login : 10.0.0.99


##### Table of Contents  
1. [Host Preparation](#host_prep)
	1. [**apt-install** packages](#host_prep_1)
	2. [Setup a host-only network in VirtualBox](#host_prep_2)
    3. [**/etc/exports** specify NFS shared directory](#host_prep_3)
    4. [**/etc/hosts** specify VM cluster node layout](#host_prep_4)
2. [VM Node Creation & Preparation](#node_prep)
	1. [Create a new VM](#node_prep_1)
	2. [Install OS and packages](#node_prep_2)
3. [VM Node Network and NFS Setup](#network)
	1. [**/etc/hosts** specify VM cluster node layout](#network_1)
	2. [**/etc/hostname** specify node name](#network_2)
	3. [**/etc/network/interfaces** specify node IP](#network_3)
	4. [**/etc/fstab** specify NFS shared dir location](#network_4)
4. [VM Node iMPI Installation](#impi_inst)
5. [Duplicate VM Node](#dup_node)

<a name="host_prep"/>
## 1. Host Preparation (admin rights required)

On host machine, do the following...

<a name="host_prep_1"/>
#### 1.1 apt-install packages
* virtualbox
* nfs-common
* nfs-kernel-server
* tmux

<a name="host_prep_2"/>
#### 1.2 Setup a host-only network in VirtualBox

* **Command line version**
```bash
vboxmanage hostonlyif create
```
```bash
vboxmanage list hostonlyifs
```
```bash
vboxmanage hostonlyif ipconfig vboxnet0 --ip 10.0.0.100 --netmask 255.255.255.0
```
```bash
vboxmanage hostonlyif ipconfig vboxnet1 --ipv6 '' --netmasklengthv6 0
```
```bash
vboxmanage list hostonlyifs
```
<span style="color:red">Note: make sure **DHCP** is disabled.</span>


* **GUI version**
```
Start VirtualBox
go to "File" -> "Preferences" -> "Network" -> "Host-only Networks"
```
```
Add a new host-only network. "vboxnet0" will be created.
```
```
Choose "vboxnet0" and edit "Adapter" tab:
	- IPv4 Address: 10.0.0.100
	- IPv4 Network Mask: 255.255.255.0
	- IPv6 Address: (leave blank)
	- IPv6 Network Mask Length: 0
```
```
In "DHCP Server" tab, uncheck "Enable server" option.
```

<a name="host_prep_3"/>
#### 1.3 /etc/exports specify NFS shared directory

Insert the following line into **/etc/exports**.

On Linux OS
```
/path/to/nfs 10.0.0.0/24(rw,fsid=0,insecure,no_subtree_check,async,no_root_squash)
```

On OSX
```
/path/to/nfs -maproot=root:wheel -network 10.0.0.0 -mask 255.255.255.0
```

Then execute this so that the above change take effect.
```bash
sudo exportfs -ra
```

<a name="host_prep_4"/>
#### 1.4 /etc/hosts specify VM cluster node layout

Insert following lines to **/etc/hosts**
```no-highlight
10.0.0.1   node0
10.0.0.2   node1
10.0.0.3   node2
10.0.0.4   node3
10.0.0.5   node4
10.0.0.6   node5
10.0.0.7   node6
10.0.0.8   node7
10.0.0.9   controller
10.0.0.99  login
10.0.0.100 IMPIHOST
```
Then restart network service (Linux only)
```bash
sudo service networking restart
```

<a name="node_prep"/>
## 2. VM Node Creation & Preparation

<a name="node_prep_1"/>
#### 2.1 Create a new VM

##### Download an Ubuntu desktop ISO image. We use 16.04 LTS.

##### Start VirtualBox, create a new virtual machine with:
* Name: node0
* Type: Linux
* Version: Ubuntu (64-bit)
* Memory size: 2048 MB (recommend at least 2GB)
* Create a hard disk:
	* file type: VDI
	* dynamically allocated (this allows disk file to shrink/grow)
	* choose a file location
	* disk size limit: 10GB

##### When VM created, do NOT start it right away. Adjust its settings first!

* **Command line version**
```bash
vboxmanage modifyvm node0 --memory 2048 --cpus 2 --cpuexecutioncap 70 --accelerate3d off --accelerate2dvideo off --audio none --usb off --clipboard hosttoguest --nic1 nat --cableconnected1 on --nic2 hostonly --cableconnected2 on --hostonlyadapter2 vboxnet0
```

* **GUI version**
```
Right click VM, choose "Settings..."
	- In "System" tab, "Base memory" set to 2048 MB
	- In "System" tab, "Processors" to 2 CPUs  <--- Very important!
      and "Execution Cap" set to 70%
	- In "Display" tab, disable 3D and 2D acceleration
	- In "Audio" tab, disable audio
	- In "Network" tab, set adapter 1 to **NAT**, adapter 2 to **Host-Only**       with the **vboxnet0**.
```

<a name="node_prep_2"/>
#### 2.2 Install OS and Packages on VM

##### 1. Start the VM, finish the OS installation with the Ubuntu ISO image. Reboot.
<span style="color:red">Note: Create the same user name as the one on host machine from which you will be launching the iMPI applications.</span>

##### 2. Install necessary packages and update/upgrade system
```bash
sudo apt update
```
```bash
sudo apt install build-essential openssh-server nfs-common htop vim libssl-dev scons gfortran cmake libnetcdf-dev libpthread-stubs0-dev libnuma-dev
```
```bash
sudo apt upgrade
```
```bash
sudo apt autoremove
```
```bash
sudo apt autoclean
```
```bash
sudo apt clean
```
```bash
sudo reboot
```
Package explanation:
* build-essential
* openssh-server		<--needed for ssh login
* nfs-common			<--needed for NFS shared dir
* htop					<--monitoring utility
* vim
* libssl-dev			<--needed by **munge**
* scons					<--needed by **samoa**
* gfortran				<--needed by **samoa**
* cmake 				<--needed by **asagi**
* libnetcdf-dev			<--needed by **asagi**
* libpthread-stubs0-dev	<--needed by **asagi**
* libnuma-dev			<--needed by **asagi**


<a name="network"/>
## 3. VM Node Network and NFS Setup

On the VM node, modify the following 4 files
* /etc/hosts
* /etc/hostname
* /etc/network/interfaces
* /etc/fstab

<a name="network_1"/>
#### 3.1 /etc/hosts specify VM cluster node layout

**Note: Node layout must be consistent on Host and all VMs.**

Comment out line "127.0.1.1 node0" if it exists.
```no-highlight
#127.0.1.1  node0
```
Append these lines
```no-highlight
# iMPI VM cluster
10.0.0.1   node0
10.0.0.2   node1
10.0.0.3   node2
10.0.0.4   node3
10.0.0.5   node4
10.0.0.6   node5
10.0.0.7   node6
10.0.0.8   node7
10.0.0.9   controller
10.0.0.99  login
10.0.0.100 IMPIHOST
```

<a name="network_2"/>
#### 3.2 /etc/hostname specify node name, e.g.,
```no-highlight
node0
```


<a name="network_3"/>
#### 3.3 /etc/network/interfaces specify node IP

<span style="color:red">**Note**: host name and IP address must match according to node layout, e.g. _node0_ address must be 10.0.0.1 ; _node1_ address must be 10.0.0.2 ; etc.</span>

Insert these lines to **/etc/network/interfaces**
```bash
# Adapter 1 (enp0s3) for NAT Internet access, use dhcp
# gateway will be set by dhcp (do not manually set gateway)
auto enp0s3
iface enp0s3 inet dhcp

# Adapter 2 (enp0s8) for Host-Only network, use static
auto enp0s8
iface enp0s8 inet static
	address   10.0.0.1
    netmask   255.255.255.0
    network   10.0.0.0
    broadcast 10.0.0.255
```


<a name="network_4"/>
#### 3.4 /etc/fstab specify NFS shared dir location

<span style="color:red">**Note**: the NFS path on VM must be EXACTLY the same as on host! It won't work otherwise.</span>

- Create the exact same path on VM if it doesn't exist.
```bash
sudo mkdir -p /path/to/nfs
```
- Insert this line to **/etc/fstab**
```bash
10.0.0.100:/path/to/nfs  /path/to/nfs   nfs   auto    0   0
```


#### 3.5 Setup SSH authorized keys and bashrc

- Restart VM, now check if the NFS shared folder is working.

- Setup root account password.
```bash
sudo passwd
```

- Add the host's pubic key to both the root account, and current user account.
```bash
mkdir -p ~/.ssh
```
```bash
touch ~/.ssh/authorized_keys
```
```bash
cat path/to/hosts/id_rsa.pub >> ~/.ssh/authorized_keys
```

- Add paths to **.bashrc** for both **current user** and **root**.

```bash
##############################
#        MY SETTING
##############################

#enable 256-color support
export TERM="xterm-256color"

# set ls color
alias ls='ls --color=auto'

# convenient stuff
alias lss='ls -1'
alias ll='ls -alhF'
alias la='ls -A'
alias laa='ls -A1'
alias l='ls -CF'
alias du1='du -h -d 1'
alias tlf="tail -f"
alias cdnfs='cd $NFSPATH'
alias cdimpi='cd $IMPIPATH'
alias cdesa='cd $NFSPATH/esamoa'

# Java compiler path point to JDK instead of JRE
#export JAVA_HOME=$(dirname $(dirname $(readlink $(which javac))))

# VM functions
function vm_irm_node {
        pkill -f munge -9
        munged -f
        pkill -f slurm -9
        slurmd -Dc
}
function vm_irm_ctrl {
        pkill -f munge -9
        munged -f
        pkill -f slurm -9
        pkill -f irtsched -9
        irtsched -Dc
}

# define NFSPATH (for iMPI VM cluster)
export NFSPATH=/work_fast/hellenbr/workspace
export IMPIPATH=$NFSPATH/ihpcins
# iMPI paths
export PATH=$IMPIPATH/sbin:$PATH
export PATH=$IMPIPATH/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$IMPIPATH/lib:$LD_LIBRARY_PATH
export CPATH=$IMPIPATH/include:$CPATH
export CPPPATH=$IMPIPATH/include:$CPPPATH
export SLURM_MPI_TYPE=pmi2
# start from work dir
cdesa
```

<a name="impi_ins"/>
## 4. VM Node iMPI Installation

<a name="impi_ins_1"/>
#### 4.1 Install dependencies & munge
```
Install dependencies in order:
1) m4		---> install to $IMPIPATH
2) autoconf	---> install to $IMPIPATH
3) automake	---> install to $IMPIPATH
4) libtool	---> install to $IMPIPATH
5) munge	---> install to /usr/local (munge must be one instance per VM)
```

- For **m4**, **autoconf**, **automake**, **libtool** do this:
```bash
tar xvzf <package_tar.gz_ball>
```
```bash
cd <package_dir>
```
```bash
./configure --prefix=$IMPIPATH
```
```bash
make install
```

- For **munge**, do this
```bash
tar xvjf <package_tar.bz2_ball>
```
```bash
cd <package_dir>
```
```bash
./configure --prefix=/usr/local
```
```bash
sudo make install
```

- Create a **munge.key** file
```bash
sudo mkdir -p /usr/local/etc/munge
```
```bash
sudo touch /usr/local/etc/munge/munge.key
```
```bash
echo 'somenumberalphabetonlytextnospecialcharacters' | sudo tee -a /usr/local/etc/munge/munge.key
```

- Test **munged**
```bash
munged -Ff
```


<a name="impi_ins_2"/>
#### 4.2 Install iRM

- Run autogen
```bash
cd /path/to/irm
```
```bash
./autogen.sh
```

- Build and install **iRM**
```bash
cd /path/to/irm_build
```
```bash
../irm/configure --prefix=$IMPIPATH --with-munge=/usr/local
```
```bash
make install
```

- Install **PMI**
```bash
cd ./contribs/pmi2
```
```bash
make install
```

- Copy **slurm.conf** file into **$IMPIPATH/etc**
```bash
cp /path/to/sample/slurm.conf $IMPIPATH/etc
```
<span style="color:red">Note 1: Add **root** as slurm user in **slurm.conf** (also remove unnecessary users)</span>
```no-highlight
SlurmUser=root
SlurmdUser=root
```
<span style="color:red">Note 2: Check the end of file, node layout should be consistent!! </span>
```no-hightlight
# COMPUTE NODES
#PartitionName=local Nodes=NODES Default=YES MaxTime=INFINITE State=UP
NodeName=10.0.0.1 NodeHostname=node0 CPUs=2 State=UNKNOWN
NodeName=10.0.0.2 NodeHostname=node1 CPUs=2 State=UNKNOWN
NodeName=10.0.0.3 NodeHostname=node2 CPUs=2 State=UNKNOWN
NodeName=10.0.0.4 NodeHostname=node3 CPUs=2 State=UNKNOWN
NodeName=10.0.0.5 NodeHostname=node4 CPUs=2 State=UNKNOWN
NodeName=10.0.0.6 NodeHostname=node5 CPUs=2 State=UNKNOWN
NodeName=10.0.0.7 NodeHostname=node6 CPUs=2 State=UNKNOWN
NodeName=10.0.0.8 NodeHostname=node7 CPUs=2 State=UNKNOWN
PartitionName=vbox Nodes=10.0.0.[1-8] Default=YES MaxTime=INFINITE State=UP
#PartitionName=local Nodes=node0,node1,node2,node3 Default=YES MaxTime=INFINITE State=UP
ControlAddr=10.0.0.9
ControlMachine=controller
```

- Test **slurmd**
```bash
slurmd -Dvvvv
```


<a name="impi_ins_3"/>
#### 4.3 Install iMPI

- Run autogen
```bash
cd /path/to/impi
```
```bash
./autogen.sh
```

- Build and install **iMPI**
```bash
cd /path/to/impi_build
```
```bash
../impi/configure --prefix=$IMPIPATH --with-slurm=$IMPIPATH --with-pmi=pmi2 --with-pm=no
```
```bash
make install
```


<a name="impi_ins_4"/>
#### 4.4 Install iMPI Tests

- Run autogen
```bash
cd /path/to/impitests
```
```bash
./autogen.sh
```

- Build and install **iMPI tests**
```bash
cd /path/to/impitests_build
```
```bash
./impitests/configure --prefix=$IMPIPATH/tests LDFLAGS="-L"$IMPIPATH"/lib"
```
```bash
make install
```

<a name="impi_ins_5"/>
#### 4.5 Install ASAGI

- Get **ASAGI** repo and its submodules
```bash
git clone https://github.com/TUM-I5/ASAGI.git asagi
```
```bash
cd asagi
```
```bash
git submodule update --init --recursive
```

- Build and install **ASAGI**
<span style="color:red">Note:For iMPI to work, ASAGI must be compiled with no MPI </span>
```bash
cd /path/to/asagi_build
```
```bash
cmake -DCMAKE_INSTALL_PREFIX=$IMPIPATH -DCMAKE_PREFIX_PATH=$IMPIPATH -DNOMPI=ON ../asagi
```
```bash
make install
```


<a name="impi_ins_6"/>
#### 4.6 Install eSamoa



<a name="dup_node"/>
## 5. Duplicate VM Node

```bash
vboxmanage clonevm node0 --name node1 --basefolder /path/to/vms --register
```
