[![Logo](https://raw.githubusercontent.com/meistero/Samoa/master/logo_small.png)]( https://raw.githubusercontent.com/meistero/Samoa/master/logo.png)

eSam(oa)²
=========

Elastic Space-Filling Curves and Adaptive Meshes for Oceanic And Other Applications. <br>
Github repository: [https://github.com/mohellen/eSamoa.git](https://github.com/mohellen/eSamoa.git)

## Contents

1. [Prerequisite iRM-iMPI infrastructure](#impi)
2. [Prerequisite ASAGI](#asagi)
3. [eSamoa](#esamoa)


<a name="impi"/>
### 1. Prerequisite iRM-iMPI infrastructure

<a name="asagi"/>
### 2. Prerequisite ASAGI

- **ASAGI** dependencies
```bash
sudo apt install libnetcdf-dev libpthread-stubs0-dev libnuma-dev
```

- Get **ASAGI** and its submodules
```bash
git clone https://github.com/TUM-I5/ASAGI.git asagi
```
```bash
cd asagi
```
```bash
git submodule update --init --recursive
```

- Build and install
```bash
cd /path/to/asagi_build
```
```bash
cmake -DCMAKE_INSTALL_PREFIX=$IMPIPATH -DCMAKE_PREFIX_PATH=$IMPIPATH -DNOMPI=ON ../asagi
```
```bash
make install
```
<span style="color:red">**Note**: For iMPI to work, ASAGI must be compiled with no MPI</span>

<a name="esamoa"/>
### 3. eSamoa

- **eSamoa** dependencies
```bash
sudo apt install scons gfortran
```

- Get **eSamoa**
```bash
git@github.com:mohellen/eSamoa.git esamoa
```

- Compile **eSamoa**
```bash
cd esamoa
```
```bash
scons config=cmp/swe.py asagi_dir=<asagi lib install location>
```
<span style="color:red">**Note**: parameters in config script can be overridden by passing the parameters directly like above. For more compile usage, do `cat cmp/README`.</span>

- Run **eSamoa**
```bash
cd <output_dir>
```
```bash
cp esamoa/run/tohoku.sh .
```
<span style="color:red">**Note**: set BASEPATH (esamoa) and DATAPATH (samoa-data) in the script.</span>
-
```bash
bash tohoku.sh
```
