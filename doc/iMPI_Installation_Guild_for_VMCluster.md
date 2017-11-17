# iMPI Installation on Virtual Machine Cluster

This is a step-by-step guide for setting up a VM cluster with iMPI installed on it. We use [Oracle VirtualBox](https://www.virtualbox.org/).

The cluster consists of 1 controller node (which runs the SLURM controller daemon) and N worker nodes (which do the actual computation work). N can be any number the user desires or the host machine can handle.

In this guide, we use the following node configuration -- [Host name] : [IP Assignment]

* node0 : 10.0.0.1
* node1 : 10.0.0.2
* node2 : 10.0.0.3
* node3 : 10.0.0.4
* controller : 10.0.0.5

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

VirtualBox can also be installed manually from [Oracle VirtualBox](https://www.virtualbox.org/).

<a name="host_prep_2"/>
#### 1.2 Setup a host-only network in VirtualBox

Start VirtualBox, go to **File** -> **Preferences** -> **Network** -> **Host-only Networks**.

Add a new host-only network. **vboxnet0** will be created.

Choose **vboxnet0** and edit:
* In **Adapter** tab
	* IPv4 Address: 10.0.0.100 
	* IPv4 Network Mask: 255.255.255.0
	* IPv6 Address: (leave blank)
	* IPv6 Network Mask Length: 0
* In **DHCP Server** tab, uncheck "Enable server" option.

<a name="host_prep_3"/>
#### 1.3 /etc/exports specify NFS shared directory

Let **/path/to/nfs** be the desired location you want to create the shared directory between host and VMs.

Insert the following line into **/etc/exports**.
```no-highlight
/path/to/nfs  10.0.0.0/24(rw,fsid=0,insecure,no_subtree_check,async,no_root_squash)
```
Then execute this so that the above change take effect.
```bash
sudo exportfs -ra
```
<a name="host_prep_4"/>
#### 1.4 /etc/hosts specify VM cluster node layout

Insert following lines to **/etc/hosts**
```no-highlight
10.0.0.1     node0
10.0.0.2     node1
10.0.0.3     node2
10.0.0.4     node3
10.0.0.5     controller
10.0.0.100   IMPIHOST
```
Then restart network service so that the above change take effect
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

##### When VM created, do NOT start it right away. Adjust its settings via command line:
```bash
vboxmanage modifyvm node0 --memory 2048 --cpus 2 --cpuexecutioncap 70 --accelerate3d off --accelerate2dvideo off --audio none --usb off --clipboard hosttoguest --hostonlyadapter1 vboxnet0 --cableconnected1 on --nic1 nat
```
Alternatively, one can also change the setting via GUI:

* In **System** tab, set
	* <span style="color:red">Processors: 2 CPUs</span> -----Very important!
	* Execution Cap: 70%
* In **Display** tab, disable 3D and 2D acceleration
* In **Audio** tab, disable audio
* In **Network** tab, use **NAT** network adapter for now (because we need Internet access to install some packages).



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
sudo apt autoremove
sudo apt autoclean
sudo apt clean
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

<span style="color:red">Note: Node layout must be consistent on Host and all VMs.</span>
```no-highlight
10.0.0.1     node0
10.0.0.2     node1
10.0.0.3     node2
10.0.0.4     node3
10.0.0.5     controller
10.0.0.100   IMPIHOST
```

<a name="network_2"/>
#### 3.2 /etc/hostname specify node name
e.g.
> node0


<a name="network_3"/>
#### 3.3 /etc/network/interfaces specify node IP
 
<span style="color:red">Note: host name and IP address must match according to node layout, e.g. _node0_ address must be 10.0.0.1 ; _node1_ address must be 10.0.0.2 ; etc.</span>

<span style="color:green">Note 2: to access internet, must uncomment the dhcp line, and comment out the static lines.</span>

Insert these lines to **/etc/network/interfaces**
```no-highlight
# Primary interface
auto enp0s3
# For Internet access, use dhcp
#iface enp0s3 inet dhcp
# For Host-VM network (no Internet access), use static
iface enp0s3 inet static
	address 10.0.0.1
    netmask 255.255.255.0
    gateway 10.0.0.254
```

<a name="network_4"/>
#### 3.4 /etc/fstab specify NFS shared dir location

<span style="color:red">Note: the path on VM must be EXACTLY the same as on host!! (It won't work otherwise.)</span>

Create the exact same path on VM if it doesn't exist.
```bash
sudo mkdir -p /path/to/nfs
```
Insert this line to **/etc/fstab**
```bash
10.0.0.100:/path/to/nfs  /path/to/nfs   nfs   auto    0   0
```

#### 3.5 Switch VM to host-only network
Shut down VM, and run the following command to switch to host-only network
```bash
vboxmanage modifyvm node0 --nic1 hostonly
```

#### 3.6 Setup SSH authorized keys and bashrc

1. Start VM, now check if the NFS shared folder is working. 

2. Setup root account password.
```bash
sudo passwd
```
After entering sudo password for currently user, you will be prompt to enter password for root.

3. Add the host's pubic key to both the root account, and current user account.
```bash
mkdir -p ~/.ssh
touch ~/.ssh/authorized_keys
cat path/to/hosts/id_rsa.pub >> ~/.ssh/authorized_keys
```

4. Add paths to **.bashrc** in both accounts (root and current user)
```bash
export NFSPATH=/path/to/nfs
export IMPIPATH=$NFSPATH/ihpcins

export PATH=$IMPIPATH/sbin:$PATH
export PATH=$IMPIPATH/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$IMPIPATH/lib:$LD_LIBRARY_PATH
export CPPPATH=$IMPIPATH/include:$CPPPAT
export SLURM_MPI_TYPE=pmi2
```

<a name="impi_ins"/>
## 4. VM Node iMPI Installation

<a name="impi_ins_1"/>
#### 4.1 Install dependencies & munge

Install dependencies in order:
1) autoconf	---> install to $IMPIPATH
2) automake	---> install to $IMPIPATH
3) libtool	---> install to $IMPIPATH
4) m4		---> install to $IMPIPATH
5) munge	---> install to /usr/local (munge must be one instance per VM)

For **autoconf**, **automake**, **libtool** and **m4**, do this:
```bash
tar xvzf \<package tar.gz ball\>
cd \<package_dir\>
./configure --prefix=$IMPIPATH
make install
```
For **munge**, do this
```bash
tar xvjf \<package tar.bz2 ball\>
cd \<package_dir\>
./configure --prefix=/usr/local
sudo make install
```
Create a **munge.key** file
```bash
sudo mkdir -p /usr/local/etc/munge
sudo touch /usr/local/etc/munge/munge.key
echo 'somenumberalphabetonlytextnospecialcharacters' | sudo tee -a /usr/local/etc/munge/munge.key
```
Test **munged**
```bash
munged -Ff
```

<a name="impi_ins_2"/>
#### 4.2 Install iRM

```bash
cd /path/to/irm
./autogen.sh

cd /path/to/irm_build
../irm/configure --prefix=$IMPIPATH --with-munge=/usr/local
make install

cd ./contribs/pmi2
make install
```

Now copy **slurm.conf** file into **$IMPIPATH/etc**
```bash
cp /path/to/sample/slurm.conf $IMPIPATH/etc
```
<span style="color:red">Note1: Add boths root and current user to **slurm.conf** (also remove unnecessary users)</span>
```no-highlight
SlurmUser=\<current user\>
SlurmUser=root
SlurmdUser=\<current user\>
SlurmdUser=root
```
<span style="color:red">Note2: Check the end of file, node layout should be consistent!! </span>


Test **slurmd**
```bash
slurmd -Dvvvv
```

<a name="impi_ins_3"/>
#### 4.3 Install iMPI

```bash
cd /path/to/impi
./autogen.sh

cd /path/to/impi_build
../impi/configure --prefix=$IMPIPATH --with-slurm=$IMPIPATH --with-pmi=pmi2 --with-pm=no
make install
```

<a name="impi_ins_4"/>
#### 4.4 Install iMPI Tests

```bash
cd /path/to/impitests
./autogen.sh

cd /path/to/impitests_build
../impitests/configure --prefix=$IMPIPATH/tests
make install
```
Note: if run into make error, open **config.status** and add the correct -I/path to **CPPFLAG** and -L/path to **LDFLAG**.


<a name="impi_ins_5"/>
#### 4.5 Install ASAGI

```bash
cd /path/to/asagi_build
cmake -DCMAKE_INSTALL_PREFIX=$IMPIPATH -DCMAKE_PREFIX_PATH=$IMPIPATH -DNOMPI=ON ../asagi
make install
```
Note: For iMPI to work, ASAGI must be compiled with no MPI

<a name="impi_ins_6"/>
#### 4.6 Install eSamoa



<a name="dup_node"/>
## 5. Duplicate VM Node

```bash
vboxmanage clonevm node0 --name node1 --basefolder /work_fast/hellenbr/vms --register
```
