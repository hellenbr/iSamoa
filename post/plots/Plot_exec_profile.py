
#########################################
##  Plot Execution Profile
#########################################
import numpy as np
import linecache
get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


###################################
##### PROVIDE INPUTS HERE !!! #####
###################################

# Specify the input file to read
readfilename = "/Volumes/DATA/emily/Desktop/tmp/swe25_mpi_sb32n16t_console.out"

# Specify the output figure path & name
figname_prefix = '/Volumes/DATA/emily/Desktop/tmp/'
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
        try:
            init_wall_time += [float(arr[8])]
            init_cells_per_rank += [int(arr[11])]
            init_ranks += [int(arr[14])]
        except:
            continue
        
    elif "SWE Earthquake: dt" in line:
        arr = line.split()
        try:
            eqk_wall_time += [float(arr[12])]
            eqk_time_step += [int(arr[16])]
            eqk_cells_per_rank += [int(arr[19])]
            eqk_ranks += [int(arr[22])]
        except:
            continue
    
    elif "SWE Tsunami: dt" in line:
        arr = line.split()
        try:
            tsu_wall_time += [float(arr[14])]
            tsu_time_step += [int(arr[18])]
            tsu_cells_per_rank += [int(arr[21])]
            tsu_ranks += [int(arr[24])]
        except:
            continue
f.close()

time_in_sec = np.array(tsu_wall_time)
time_in_min = time_in_sec / 60
time_in_hr = time_in_sec / 3600
tsu_total_cells = np.array(tsu_cells_per_rank) * np.array(tsu_ranks)
tsu_rank_cells = np.array(tsu_cells_per_rank)


####################
##### Plotting #####
####################

def plot_all_in_one(time_in_sec, tsu_ranks, tsu_total_cells, tsu_rank_cells):
    # Figure setup
    fig = plt.figure(frameon = True)
    # 9.6 inch x 200 dpi = 1920
    # 5.4 inch x 200 dpi = 1080
    fig.set_size_inches(9.6, 5.4) 
    host = fig.add_subplot(1,1,1)
    par1 = host.twinx()
    par2 = host.twinx()

    colorhost = 'b'
    colorpar1 = 'r'
    colorpar2 = 'g'

    host.set_xlabel("Execution time")
    host.set_ylabel("Number of MPI ranks", color=colorhost)
    par1.set_ylabel("Number of grid cells in total", color=colorpar1)
    par2.set_ylabel("Number of gird cells per rank", color=colorpar2)

    p1, = host.plot(time_in_sec, tsu_ranks, color=colorhost,label="MPI ranks")
    p2, = par1.plot(time_in_sec, tsu_total_cells, color=colorpar1, label="# of grid cells in total")
    p3, = par2.plot(time_in_sec, tsu_rank_cells, color=colorpar2, label="# of grid cells per rank")

    lns = [p1, p2, p3]
    host.legend(handles=lns, loc="upper left", bbox_to_anchor=(-0.05,1.15), fancybox=True, shadow=False, ncol=5)

    #host.set_xlim([0,35])
    #par1.text(35, 0.24, r'$\times 10^6$', fontsize=11, color=colorpar1)
    # right, left, top, bottom
    par2.spines['right'].set_position(('outward', 60))      
    #par2.text(41.3, 0.114, r'$\times 10^6$', fontsize=11, color=colorpar2)

    host.yaxis.label.set_color(colorhost)
    par1.yaxis.label.set_color(colorpar1)
    par2.yaxis.label.set_color(colorpar2)

    for tl in host.get_yticklabels():
        tl.set_color(colorhost)

    for tl in par1.get_yticklabels():
        tl.set_color(colorpar1)

    for tl in par2.get_yticklabels():
        tl.set_color(colorpar2)

    plt.savefig(figname_prefix + "fig_exec_profile_one" + figname_suffix, bbox_inches="tight")
    plt.close(fig)


def plot_two_figs(time_in_sec, tsu_ranks, tsu_total_cells, tsu_rank_cells):

    ######### Setup this #########
    ##############################
    # Full labels
    x_label       = "Execution time"
    upper_y1_label = "Number of MPI ranks"
    upper_y2_label = "Number of grid cells in total"
    lower_y1_label = "Number of MPI ranks"
    lower_y2_label = "Number of grid cells per rank"

    # Short labels (for legend)
    x_label2      = "Time"
    upper_y1_label2 = "MPI ranks"
    upper_y2_label2 = "# cells in total"
    lower_y1_label2 = "MPI ranks"
    lower_y2_label2 = "# cells per rank"

    # leave range empty if range be auto
    x_range = [0, 530]
    upper_y1_range = [0, 600]
    upper_y2_range = []
    lower_y1_range = upper_y1_range
    lower_y2_range = []
    ##############################

    # Figure setup
    fig = plt.figure(figsize=(5,8), frameon=True)
    # Subplot grid config
    gs = gridspec.GridSpec(2,1)
    gs.update(wspace=0.025, hspace=0.025)
    # Axis of subplots
    f1p1 = plt.subplot(gs[0])
    f1p2 = f1p1.twinx()
    f2p1 = plt.subplot(gs[1])
    f2p2 = f2p1.twinx()

    # Define axis colors
    colorf1p1 = 'b'
    colorf1p2 = 'r'
    colorf2p1 = 'b'
    colorf2p2 = 'g'

    # Plotting
    p1, = f1p1.plot(time_in_sec, tsu_ranks, color=colorf1p1,label=upper_y1_label2)
    p2, = f1p2.plot(time_in_sec, tsu_total_cells/1000000, color=colorf1p2, label=upper_y2_label2)
    p3, = f2p1.plot(time_in_sec, tsu_ranks, color=colorf2p1,label=lower_y1_label2)
    p4, = f2p2.plot(time_in_sec, tsu_rank_cells, color=colorf2p2, label=lower_y2_label2)

    # Need a special "x10" label for f1p2 (number of Million cells)
    [x1,x2] = f1p2.get_xlim()
    [y1,y2] = f1p2.get_ylim()
    f1p2.text(x2*1.01, y2*0.98, r'$\times 10^6$', fontsize=9, color=colorf1p2)    

    # Set range
    if (len(x_range) > 0):
        f1p1.set_xlim(x_range)
        f2p1.set_xlim(x_range)
    if (len(upper_y1_range) > 0):
        f1p1.set_ylim(upper_y1_range)
    if (len(upper_y2_range) > 0):
        f1p2.set_ylim(upper_y2_range)
    if (len(lower_y1_range) > 0):
        f2p1.set_ylim(lower_y1_range)
    if (len(lower_y2_range) > 0):
        f2p2.set_ylim(lower_y2_range)   

    # Axis labels
    f1p1.axes.xaxis.set_ticklabels([])  # Hide x-axis in the upper subplot
    f1p1.set_ylabel(upper_y1_label, color=colorf1p1)
    f1p2.set_ylabel(upper_y2_label, color=colorf1p2)
    f2p1.set_xlabel(x_label)
    f2p1.set_ylabel(lower_y1_label, color=colorf2p1)
    f2p2.set_ylabel(lower_y2_label, color=colorf2p2)

    # Turn on grid line only for x-axis
    f1p1.axes.xaxis.grid(True)
    f2p1.axes.xaxis.grid(True)

    # Add legend
    lns = [p1, p2, p4]
    f1p1.legend(handles=lns, loc="upper left", bbox_to_anchor=(-0.1,1.18), fancybox=True, shadow=False, ncol=5)

    # Color for labels and ticks
    f1p1.yaxis.label.set_color(colorf1p1)
    f1p2.yaxis.label.set_color(colorf1p2)
    f2p1.yaxis.label.set_color(colorf2p1)
    f2p2.yaxis.label.set_color(colorf2p2)
    for tl in f1p1.get_yticklabels():
        tl.set_color(colorf1p1)
    for tl in f1p2.get_yticklabels():
        tl.set_color(colorf1p2)
    for tl in f2p1.get_yticklabels():
        tl.set_color(colorf2p1)        
    for tl in f2p2.get_yticklabels():
        tl.set_color(colorf2p2)

    # Save and close
    plt.savefig(figname_prefix + "fig_exec_profile_two" + figname_suffix, bbox_inches="tight")
    plt.close(fig)


plot_two_figs(time_in_sec, tsu_ranks, tsu_total_cells, tsu_rank_cells)



