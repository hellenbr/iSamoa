#########################################
##  Plot Execution Profile
#########################################
import numpy as np
import linecache
get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt

###################################
##### PROVIDE INPUTS HERE !!! #####
###################################

# Specify the input file to read
readfilename = "/media/emily/EMO-64G/yes_vm8n2r_irmperi_tohoku_3hr/console.out"

# Specify the output figure path & name
figname_prefix = '/media/emily/EMO-64G/yes_vm8n2r_irmperi_tohoku_3hr/'
figname_suffix = '.pdf'

###########################
##### Data Processing #####
###########################

# There are 3 phases: "initialization", "earthquake displacement data", "tsunami simulation"
# Create 3 sets of lists

# sim time not available in init phase
init_wall_time = []
init_cells_per_rank = []
init_ranks = []

eqk_wall_time = []
eqk_time_step = []
eqk_cells_per_rank = []
eqk_ranks = []

tsu_wall_time = []
tsu_time_step = []
tsu_cells_per_rank = []
tsu_ranks = []

f = open(readfilename, 'r')
for i, line in enumerate(f,1):
    if "SWE Init: adaption" in line:
        arr = line.split()
        init_wall_time += [float(arr[8])]
        init_cells_per_rank += [int(arr[11])]
        init_ranks += [int(arr[14])]
        
    elif "SWE Earthquake: dt" in line:
        arr = line.split()    
        eqk_wall_time += [float(arr[12])]
        eqk_time_step += [int(arr[16])]
        eqk_cells_per_rank += [int(arr[19])]
        eqk_ranks += [int(arr[22])]
    
    elif "SWE Tsunami: dt" in line:
        arr = line.split()    
        tsu_wall_time += [float(arr[14])]
        tsu_time_step += [int(arr[18])]
        tsu_cells_per_rank += [int(arr[21])]
        tsu_ranks += [int(arr[24])]
f.close()

####################
##### Plotting #####
####################
time_in_min = np.array(tsu_wall_time) / 60
tsu_cells = np.array(tsu_cells_per_rank) * np.array(tsu_ranks) / 1000000
tsu_rank_cells = np.array(tsu_cells_per_rank) / 1000000

fig = plt.figure()
host = fig.add_subplot(111)
par1 = host.twinx()
par2 = host.twinx()

colorhost = 'b'
colorpar1 = 'r'
colorpar2 = 'g'

host.set_xlabel("Execution time in minutes")
host.set_ylabel("Number of MPI ranks", color=colorhost)
par1.set_ylabel("Number of grid cells in total", color=colorpar1)
par2.set_ylabel("Number of gird cells per rank", color=colorpar2)

p1, = host.plot(time_in_min, tsu_ranks, color=colorhost,label="MPI ranks")
p2, = par1.plot(time_in_min, tsu_cells, color=colorpar1, label="# of grid cells in total")
p3, = par2.plot(time_in_min, tsu_rank_cells, color=colorpar2, label="# of grid cells per rank")

lns = [p1, p2, p3]
host.legend(handles=lns, loc="upper left", bbox_to_anchor=(-0.05,1.15), \
		fancybox=True, shadow=False, ncol=5)
host.set_xlim([0,35])
par1.text(35, 0.24, r'$\times 10^6$', fontsize=11, color=colorpar1)
# right, left, top, bottom
par2.spines['right'].set_position(('outward', 60))      
par2.text(41.3, 0.114, r'$\times 10^6$', fontsize=11, color=colorpar2)

host.yaxis.label.set_color(colorhost)
par1.yaxis.label.set_color(colorpar1)
par2.yaxis.label.set_color(colorpar2)

for tl in host.get_yticklabels():
    tl.set_color(colorhost)

for tl in par1.get_yticklabels():
    tl.set_color(colorpar1)
    
for tl in par2.get_yticklabels():
    tl.set_color(colorpar2)

plt.savefig(figname_prefix + "fig_exec_profile" + figname_suffix, bbox_inches="tight")
plt.close(fig)





