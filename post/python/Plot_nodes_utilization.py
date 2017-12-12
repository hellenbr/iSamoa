
#############################################
##  Node-level Resource Untilization Plot
##     (for every VTK ouput step)
#############################################
import numpy as np
import linecache
#%matplotlib inline # suppress interactive display by default
import matplotlib.pyplot as plt
import matplotlib.patches as patches


###################################
##### PROVIDE INPUTS HERE !!! #####
###################################
# Specify the input file to read
filename = "/media/emily/EMO-64G/yes_swe_irmperi_vm8n2t/console.out"

# Specify the output figure path & name
figname_prefix = '/media/data/emily/Desktop/vis_nodes/res_'
figname_suffix = '.png'

# Specify application number (this determines the color used the application)
appid = 0
app2 = 1

# Setup the Nodes visual grid size: nx-by-ny
nx,ny = (8,4)
# Specify CPUs per node: cx-by-cy
cx,cy = (4,4)


###########################
##### Data Processing #####
###########################
# Function for removing duplicate nodes
# Return a list containing only unique nodes
def get_unique(node_list):
    unique_nodes = []
    for n in node_list:
        if n not in unique_nodes:
            unique_nodes += [n]
    return unique_nodes

# Get unique node lists for every OUTPUT step from file
# The output line looks like:
# "iMPI NODES OUTPUT 21 : 0 0 1 1 2 2"
node_lists = []
output_steps = []

f = open(filename, 'r')
for i, line in enumerate(f,1):
    if "iMPI NODES OUTPUT" in line:
        arr = line.split()
        # Output step number is in arr[3]
        output_steps += [int(arr[3])]
        # Starting from arr[5], convert them into a integer array
        nodes = []
        for i in range(5, len(arr)):
            nodes += [int(arr[i])]
        # Reduce to unique nodes
        unique_nodes = get_unique(nodes)
        # append to node lists
        node_lists += [unique_nodes]
f.close()

### For testing only
# for i in range(len(node_lists)):
#     print("Step ", output_steps[i], ": ", node_lists[i])


################################
##### Plotting Definitions #####
################################
# define color code
# colorcode = [
#         'grey',      # CPU is idle or in transition state
#         'lightpink', # CPU is assigned to App1
#         'skyblue',   # CPU is assigned to App2
#         'khaki',     # CPU is assigned to App3
#         'lightgreen' # CPU is assigned to App4
# ]
colorcode = [
        'skyblue',   # CPU is assigned to App1
        'lightpink', # CPU is assigned to App2
]

# Node patch config
node_size_x = 10.0
node_size_y = 10.0
node_patch_size_x = node_size_x * 0.96
node_patch_size_y = node_size_y * 0.96
node_patch_offset_x = (node_size_x - node_patch_size_x) * 0.5
node_patch_offset_y = (node_size_y - node_patch_size_y) * 0.5

# CPU patch config
cpu_size_x = node_patch_size_x / float(cx)
cpu_size_y = node_patch_size_y / float(cy)
cpu_patch_size_x = cpu_size_x * 0.9
cpu_patch_size_y = cpu_size_y * 0.9
cpu_patch_offset_x = (cpu_size_x - cpu_patch_size_x) * 0.5
cpu_patch_offset_y = (cpu_size_y - cpu_patch_size_y) * 0.5

# Function to get node color
def get_node_color(n, node_list):
    return colorcode[appid] if (n in node_list) else colorcode[app2]

# Get the node patch position (x,y)
def getxy(node_id):
    y = ny - 1 - int(node_id / nx)
    x = int(node_id % nx)
    return (x * node_size_x + node_patch_offset_x, \
            y * node_size_y + node_patch_offset_y)

# Get the cpu patch position
def getxy_cpu(node_id, cpu_x, cpu_y):
    (x,y) = getxy(node_id)
    return (x + cpu_x*cpu_size_x + cpu_patch_offset_x, \
            y + (cy-1-cpu_y)*cpu_size_y + cpu_patch_offset_y)


# Function for drawing 1 frame (CPU-based)
def draw_frame(frame_id, node_list):
    # Figure setup
    fig = plt.figure(frameon = False)
    # 9.6 inch x 200 dpi = 1920
    # 5.4 inch x 200 dpi = 1080
    fig.set_size_inches(9.6, 5.4) 
    ax = plt.Axes(fig, [0., 0., 1., 1.], )
    ax.set_xlim([0,nx*node_size_x])
    ax.set_ylim([0,ny*node_size_y])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Create a list cpu patches (cx*cy patches per node) for drawing
    cpus = dict()
    for n in range(nx*ny):
        cpu_color = get_node_color(n, node_list)
        for j in range(cy):
            for i in range(cx):
                cpu_id = n*(cx*cy) + (j*cx+i)
                cpus[cpu_id] = patches.Rectangle(
                        getxy_cpu(n, i,j),
                        cpu_patch_size_x,
                        cpu_patch_size_y,
                        facecolor=cpu_color)
    # Draw the cpu patches
    for c in cpus:
        ax.add_artist(cpus[c])
        # add a rank number to the center of patch
        x,y = cpus[c].get_xy()
        center_x = x + cpus[c].get_width()/2.0
        center_y = y + cpus[c].get_height()/2.0
        ax.annotate(c, (center_x, center_y), \
                color='black', weight='normal', fontsize=6, ha='center', va='center')
    # Add legend
    app_tsu = patches.Patch(color=colorcode[appid], label='Tsunami Simulation')
    app_inv = patches.Patch(color=colorcode[app2], label='Inverse Problem')
    leg = plt.legend(handles=[app_tsu, app_inv])
    leg.get_frame().set_alpha(0.65)  # set legend opacity

    # Save and close figure
    filename = figname_prefix + str(frame_id).zfill(3) + figname_suffix
    plt.savefig(filename, dpi=200)
    plt.close(fig)


# Test plotting for 1 frame
#frame_id = 0
#l = node_lists[frame_id]
#print(l)
#draw_frame(frame_id, l)


# Draw all frames
for i in range(len(node_lists)):
    draw_frame(output_steps[i],node_lists[i])


# Make video from png frames (ffmpeg)
#------------------------------------
# -f: input format
# -r: fps (frame rate per second)
# -s: resolution in pixel
# -i: input files
# -vcodec: video format
# -crf: quality, number between 15-25 is really good
# -pix_fmt: pixel format

cmd='ffmpeg -f image2 -r 4 -s 1920x1080 -i res_%03d.png -vcodec libx264 -crf 20 -pix_fmt yuv420p demo.mp4'
print(cmd)

