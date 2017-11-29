
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
filename = "/media/emily/EMO-64G/yes_vm8n2r_irmperi_tohoku_3hr/console.out"

# Specify the output figure path & name
figname_prefix = '/media/emily/EMO-64G/yes_vm8n2r_irmperi_tohoku_3hr/vis_nodes/res_'
figname_suffix = '.pdf'

# Specify application number (this determines the color used the application)
appid = 1

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
#for i in range(len(node_lists)):
#    print("Step ", output_steps[i], ": ", node_lists[i])


################################
##### Plotting Definitions #####
################################

# define color code
colorcode = [
        'grey',      # CPU is idle or in transition state
        'lightpink', # CPU is assigned to App1
        'skyblue',   # CPU is assigned to App2
        'khaki',     # CPU is assigned to App3
        'lightgreen' # CPU is assigned to App4
]

# Node patch config
node_size_x = 2.0
node_size_y = 2.0
node_patch_size_x = node_size_x * 0.9
node_patch_size_y = node_size_y * 0.9
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
    return colorcode[appid] if (n in node_list) else colorcode[0]

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
    		y + cpu_y*cpu_size_y + cpu_patch_offset_y)

# add cpus patches for a node to...
def add_cpus_patches(cpus, node_id, node_list):
    cpu_color = get_node_color(node_id, node_list)
    # Add list of cpu patches for the node
    for j in range(cy):
        for i in range(cx):      
            cpus[node_id*(cx*cy) + (j*cx+i)] = patches.Rectangle(
                    getxy_cpu(node_id, i,j),
                    cpu_patch_size_x,
                    cpu_patch_size_y,
                    facecolor=cpu_color)

# Function for drawing 1 frame
def draw_frame(frame_id, node_list):
    # Figure setup
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim([0,nx*node_size_x])
    ax.set_ylim([0,ny*node_size_y])
    ax.axis('off')
    ax.set_frame_on(False)
    # Create a list cpu patches (cx*cy patches per node) for drawing
    cpus = dict()
    for n in range(nx*ny):
        add_cpus_patches(cpus, n, node_list)
    # Draw the node patches
    for c in cpus:
        ax.add_artist(cpus[c]) 
    # Write node number to each node (fancy)
    for n in range(nx*ny):
        nodepatch = patches.Rectangle(getxy(n), node_patch_size_x, node_patch_size_y)
        x,y = nodepatch.get_xy()
        center_x = x + nodepatch.get_width()/2.0
        center_y = y + nodepatch.get_height()/2.0
        # Put node number at the center of the patch
        ax.annotate(n, (center_x, center_y), \
        		color='black', weight='normal', fontsize=12, ha='center', va='center')    
    # Save and close figure
    filename = figname_prefix + str(frame_id) + figname_suffix
    plt.savefig(filename)
    plt.close(fig)


# Draw all frames
for i in range(len(node_lists)):
    draw_frame(output_steps[i],node_lists[i])
    



