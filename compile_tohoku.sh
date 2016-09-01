compiler='gnu'
max_depths='20'
fdispl="data/tohoku_static/displ.nc"
fbath="data/tohoku_static/bath_2014.nc"
#flux_solvers='aug_riemann'
flux_solvers='fwave'
vtk='.true.'
asagi_dir='/media/DATA/nfs/workspace/asagi'

virtual_cores=$(lscpu | grep "^CPU(s)" | grep -oE "[0-9]+" | tr "\n" " ")
threads_per_core=$(lscpu | grep "^Thread(s) per core" | grep -oE "[0-9]+" | tr "\n" " ")
cores=$(( $virtual_cores / $threads_per_core ))

echo "Tsunami scenario execution script."
echo ""
echo "compiler          : "$compiler
echo "max depths        : "$max_depths
echo "flux solvers      : "$flux_solvers
echo "bathymetry file   : "$fdispl
echo "displacement file : "$fbath
echo ""

echo ""
echo "Compiling (skip with Ctrl-C)..."
echo ""

for flux_solver in $flux_solvers
do
	exe="samoa_swe_"$compiler"_"$flux_solver
	    scons compiler=$compiler asagi_dir=$asagi_dir scenario=swe flux_solver=$flux_solver exe=$exe -j4
done

echo ""
echo "Compile successful."
echo ""
