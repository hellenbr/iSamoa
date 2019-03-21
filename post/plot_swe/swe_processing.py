import matplotlib.pyplot as plt
import linecache
import sys


'''
This function returns data (simulation time, wall time, number of cells) in 3 equal-sized arrays
This is for plotting grid cell growth profile during the simulation
'''
def getdata_sim(filename):
	# Define output arrays
	simtime = []
	walltime = []
	numcells = []
	numranks = []

	f = open(filename, 'r')
	for i, line in enumerate(f,1):
		if "Darcy Simulation:" in line:
			arr = line.split()
			
			# Parse simulation time
			idx = arr.index("sim.time")
			tsim = 0.0
			for i in range(idx+1, idx+4):
				# remove comma if any
				tmp = arr[i].replace(',','')
				if 'd' in tmp:
					tsim += int(tmp.replace('d','')) * 3600 * 24
				elif 'h' in tmp:
					tsim += int(tmp.replace('h','')) * 3600
				elif 'min' in tmp:
					tsim += int(tmp.replace('min','')) * 60
				elif 'ms' in tmp:
					tsim += int(tmp.replace('ms','')) * 1e-3
				elif 'µs' in tmp:
					continue #igore microsec 
				elif 's' in tmp:
					tsim += int(tmp.replace('s',''))

			# Parse wall time
			idx = arr.index("elap.time(sec)")
			twall = float(arr[idx+1])

			# Parse cells and ranks
			idx = arr.index("cells")
			ncells = int(arr[idx+1])
			idx = arr.index("ranks")
			nranks = int(arr[idx+1])

			# Put data in output arrays
			simtime += [tsim]
			walltime += [twall]
			numcells += [ncells * nranks]
			numranks += [nranks]
	f.close()
	return (simtime, walltime, numcells, numranks)


'''
This function samples data (simulation time, wall time, number of cells) at the beginning of each simulation day.
It will produce less much less data points.
'''
def getdata_sim_by_day(filename):
	# Define output arrays
	simtime = []
	walltime = []
	numcells = []
	numranks = []

	f = open(filename, 'r')
	sampleline = False
	iday = 0
	for i, line in enumerate(f,1):
		if "Darcy Simulation:" in line:
			arr = line.split()
			# Determine if this line will be sample or not
			if (arr[6] == '1,'):
				sampleline = True
			elif (arr[9] == str(iday)+'d'):
				sampleline = True
			
			if (sampleline):
				# Reset for next line
				sampleline = False
				iday += 1
				
				# Parse simulation time
				idx = arr.index("sim.time")
				tsim = 0.0
				for i in range(idx+1, idx+4):
					# remove comma if any
					tmp = arr[i].replace(',','')
					if 'd' in tmp:
						tsim += int(tmp.replace('d','')) * 3600 * 24
					elif 'h' in tmp:
						tsim += int(tmp.replace('h','')) * 3600
					elif 'min' in tmp:
						tsim += int(tmp.replace('min','')) * 60
					elif 'ms' in tmp:
						tsim += int(tmp.replace('ms','')) * 1e-3
					elif 'µs' in tmp:
						continue #igore microsec 
					elif 's' in tmp:
						tsim += int(tmp.replace('s',''))

				# Parse wall time
				idx = arr.index("elap.time(sec)")
				twall = float(arr[idx+1])

				# Parse cells and ranks
				idx = arr.index("cells")
				ncells = int(arr[idx+1])
				idx = arr.index("ranks")
				nranks = int(arr[idx+1])

				# Put data in output arrays
				simtime += [tsim]
				walltime += [twall]
				numcells += [ncells * nranks]
				numranks += [nranks]
	f.close()
	return (simtime, walltime, numcells, numranks)


'''
This function returns "Phase Statistics" in 8 equal-sized arrays
This is for plotting component exec. times
'''
def getdata_stat(filename):
	##########
	# t_phase = (t_compute + t_refine + t_conformity + t_lb + t_others) / ranks + t_impi
	##########

	# Define outputs
	numranks = []
	t_phase = []
	t_compute = []
	t_refine = [] 
	t_conformity = []
	t_lb = []
	t_others = []
	t_impi = []
	sum_impi_init = 0.0
	sum_impi_probe = 0.0

	f = open(filename, 'r')
	for i, line in enumerate(f,1):
		if "init_adapt" in line:
			arr = line.split()
			idx = arr.index("init_adapt")
			sum_impi_init += float(arr[idx+1])

		if "probe_adapt" in line:
			arr = line.split()
			idx = arr.index("probe_adapt")
			sum_impi_probe += float(arr[idx+1])

		if "Phase statistics:" in line:
			j = 1
			while (True):
				line = linecache.getline(filename, i+j)
				j = j+1
				
				# Loop breaker
				if 

			# Number of ranks
			if "Num ranks:" in line: #Line starts with "Num ranks:"
				larr = line.split()
				nranks = int(larr[-1])
				numranks += [nranks]
			
			# t_phase (Total phase time)
			line = linecache.getline(filename, i+13) #Line starts with "Phase time:"
			if "Phase time:" in line:
				larr = line.split()
				idx = larr.index("time:")
				phase_time = float(larr[idx+1]) #wall time, not summed
				t_phase += [phase_time]
			else:
				sys.exit("Line Phase time not found. Program abort!")
			
			# t_refine (grid refinement time)
			# t_conformity (conformity check time)
			# t_lb (load balancing time)
			line = linecache.getline(filename, i+6) #Line starts with "Adaptions:"
			if "Adaptions:" in line:
				larr = line.split()
				idx = larr.index("time:")
				refine_time = float(larr[idx+1])/float(nranks)
				t_refine += [refine_time]
				
				idx = larr.index("integrity:")
				conformity_time = float(larr[idx+1])/float(nranks)
				t_conformity += [conformity_time]
				
				idx = larr.index("balancing:")
				lb_time = float(larr[idx+1])/float(nranks)
				t_lb += [lb_time]
			else:
				sys.exit("Line Adaptions not found. Program abort!")
		 
			# t_compute (computation time)
			line = linecache.getline(filename, i+5) #Line starts with "Time steps:"
			if "Time steps:" in line:
				larr = line.split()
				idx = larr.index("time:")
				compute_time += float(larr[idx+1])/float(nranks)
				t_compute += [compute_time]
			else:
				sys.exit("Line Time steps not found. Program abort!")
			
			# t_impi
			line = linecache.getline(filename, i+33) #Line starts with "iMPI: total adapt time"
			if "iMPI: total adapt time" in line:
				larr = line.split()
				idx = larr.index("time")
				impi_time = float(larr[idx+1])  #wall time, not summed
			else: #iMPI line may not exist (for init and the last phase)
				impi_time = 0.0
			t_impi += [impi_time]
			
			# t_others
			time_others = phase_time - compute_time - refine_time - conformity_time - lb_time - impi_time
			t_others += [time_others]

	f.close()
	return (numranks, t_phase, t_compute, t_refine, t_conformity, t_lb, t_others, t_impi, sum_impi_init, sum_impi_probe)


'''
This function returns "#ranks and T_timestep" in 2 equal-sized arrays
This is for plotting T_timestep vs. # ranks
'''
def getdata_tstep(filename, maxranks, rankspernode):
	# Define output arrays
	numranks = []
	numcellsperrank = []
	tstep = []

	# Get data from file
	f = open(filename, 'r')
	for i, line in enumerate(f,1):
		if "Darcy Simulation:" in line:
			arr = line.split()
			
			# Parse timestep time
			idx = arr.index("time(sec)")
			tstep += [float(arr[idx+1])]

			# Parse cells and ranks
			idx = arr.index("cells")
			numcellsperrank += [int(arr[idx+1])]
			idx = arr.index("ranks")
			numranks += [int(arr[idx+1])]
	f.close()

	# Process data
	# Find the average time spent on each time step for each #ranks
	nranks = [x for x in range(rankspernode,maxranks+1,rankspernode)]
	freq = [0.0] * len(nranks)
	tavg = [0.0] * len(nranks)

	for i in range(0,len(tstep)):
		k = nranks.index(numranks[i])
		freq[k] = freq[k] + 1
		tavg[k] = tavg[k] + tstep[i]
		
	for i in range(0, len(tavg)):
		if (freq[i] > 0.0):
			tavg[i] = tavg[i] / freq[i]
			
	# Remove entries with 0 frequency
	out_ranks = []
	out_tavg = []
	for i in range(0, len(freq)):
		if (freq[i] > 0.0):
			out_ranks += [nranks[i]]
			out_tavg += [tavg[i]]
			
	return (out_ranks, out_tavg)


'''
Compute CPU-hour of the run
'''
def compute_cpuhours(time_in_sec, num_cpus):
	import numpy
	return numpy.trapz(num_cpus, time_in_sec) / 3600


'''
Create fixed-sized figure/axis objects
'''
def create_figure():
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	ax = fig.add_subplot(1,1,1)
	return (fig, ax)


'''
A generic 1D plot interface
'''
def plot_1d(xvec, yvec, xrange, yrange, xtitle, ytitle, outfig, printdots=False):
	(fig, ax) = create_figure()
	if printdots:
		ax.plot(xvec, yvec, '-ok')
	else:
		ax.plot(xvec, yvec, color='k')
	if (xrange != [0,0]):
		ax.set_xlim(xrange)
	if (yrange != [0,0]):
		ax.set_ylim(yrange)
	ax.set_xlabel(xtitle, fontsize=18)
	ax.set_ylabel(ytitle, fontsize=18)
	plt.grid(True)
	plt.savefig(outfig, bbox_inches="tight")
	plt.show()
	plt.close(fig)

'''
A generic 1D plot interface for 2 datasets (2 y-axes)
'''
def plot_1d_2scales(xvec, yvec1, yvec2, xrange, yrange1, yrange2, xtitle, ytitle1, ytitle2, outfig):
	(fig, ax1) = create_figure()

	# First plot ax1
	ax1.plot(xvec, yvec1, 'b-')
	ax1.set_xlabel(xtitle, color='k', fontsize=18)
	ax1.set_ylabel(ytitle1, color='b', fontsize=18)
	ax1.tick_params('y', colors='b')
	if (xrange != [0,0]):
		ax1.set_xlim(xrange)    
	if (yrange1 != [0,0]):
		ax1.set_ylim(yrange1)

	# Second plot ax2
	ax2 = ax1.twinx()
	ax2.plot(xvec, yvec2, 'r-')
	ax2.set_ylabel(ytitle2, color='r', fontsize=18)
	ax2.tick_params('y', colors='r')
	if (xrange != [0,0]):
		ax2.set_xlim(xrange)   
	if (yrange2 != [0,0]):
		ax2.set_ylim(yrange2)

	plt.savefig(outfig, bbox_inches="tight")
	plt.show()
	plt.close(fig)

'''
Generate component % table
'''
def generate_component_table(filename):
	(numranks, t_phase, t_compute, t_refine, t_conformity, t_lb, t_others, t_impi, sum_impi_init, sum_impi_probe) = getdata_stat(filename)

	total_sim_time = sum(t_phase)
	compute_time = sum(t_compute)
	refine_time = sum(t_refine)
	comform_time = sum(t_conformity)
	lb_time = sum(t_lb)
	others_time = sum(t_others)
	impi_time = sum(t_impi) + sum_impi_init + sum_impi_probe

	print("")
	print("{0:22s} {1:20s} {2:10s}".format("Component", "Exec. time (sec)", "Percent (%)"))
	print("{0:22s} {1:20s} {2:10s}".format("----------------", "----------------", "-----------"))
	print("{0:22s} {1:16.4f} {2:10.2f}".format("Total simulation", total_sim_time, 100.0))
	print("{0:22s} {1:16.4f} {2:10.2f}".format("Computation", compute_time, compute_time/total_sim_time*100))
	print("{0:22s} {1:16.4f} {2:10.2f}".format("Grid refinement", refine_time, refine_time/total_sim_time*100))
	print("{0:22s} {1:16.4f} {2:10.2f}".format("Conformity check", comform_time, comform_time/total_sim_time*100))
	print("{0:22s} {1:16.4f} {2:10.2f}".format("Load balancing", lb_time, lb_time/total_sim_time*100))
	print("{0:22s} {1:16.4f} {2:10.2f}".format("Resource adaptation", impi_time, impi_time/total_sim_time*100))
	print("{0:22s} {1:16.4f} {2:10.2f}".format("Others", others_time, others_time/total_sim_time*100))
	print("")

'''
Generate iMPI function call table
'''
def generate_impi_table(filename):
	# Define output arrays
	total_time = []
	init_adapt = []
	probe_adapt = []
	adapt_begin = []
	adapt_commit = []

	f = open(filename, 'r')
	for i, line in enumerate(f,1):
		if "init_adapt" in line:
			arr = line.split()
			idx = arr.index("init_adapt")
			init_adapt += [float(arr[idx+1])]
		elif "probe_adapt" in line:
			arr = line.split()
			idx = arr.index("probe_adapt")
			probe_adapt += [float(arr[idx+1])]
		elif "adapt_begin" in line:
			arr = line.split()
			idx = arr.index("adapt_begin")
			adapt_begin += [float(arr[idx+1])]
		elif "adapt_commit" in line:
			arr = line.split()
			idx = arr.index("adapt_commit")
			adapt_commit += [float(arr[idx+1])]
		elif "total adapt time" in line:
			arr = line.split()
			idx = arr.index("time")
			total_time += [float(arr[idx+1])]
	f.close()

	sum_init = sum(init_adapt)
	sum_probe = sum(probe_adapt)
	sum_begin = sum(adapt_begin)
	sum_commit = sum(adapt_commit)
	# the total time array did not include init time and most of the probe time
	# So the true total time must include these two items
	sum_total = sum(total_time) + sum_init + sum_probe
	sum_data_migration = sum_total - sum_begin - sum_commit - sum_init - sum_probe

	if (sum_total > 0.0):
		print("")
		print("{0:22s} {1:18s} {2:18s} {3:10s}".format("Function", "Avg. time (sec)", "Acc. time (sec)", "Percent (%)"))
		print("{0:22s} {1:18s} {2:18s} {3:10s}".format("----------------", "----------------", "----------------", "-----------"))
		if len(total_time) == 0:
			avg = 0.0
		else:
			avg = sum_total/len(total_time)
		print("{0:22s} {1:14.4f} {2:16.4f} {3:14.2f}".format("Total adaptation",      avg,  sum_total,  100.0))

		if len(init_adapt) == 0:
			avg = 0.0
		else:
			avg = sum_init/len(init_adapt)
		print("{0:22s} {1:14.4f} {2:16.4f} {3:14.2f}".format("MPI_init_adapt",        avg,  sum_init,   sum_init/sum_total*100))

		if len(probe_adapt) == 0:
			avg = 0.0
		else:
			avg = sum_probe/len(probe_adapt)
		print("{0:22s} {1:14.4f} {2:16.4f} {3:14.2f}".format("MPI_Comm_probe_adapt",  avg,  sum_probe,  sum_probe/sum_total*100))

		if len(adapt_begin) == 0:
			avg = 0.0
		else:
			avg = sum_begin/len(adapt_begin)
		print("{0:22s} {1:14.4f} {2:16.4f} {3:14.2f}".format("MPI_Comm_adapt_begin",  avg,  sum_begin,  sum_begin/sum_total*100))

		if len(adapt_commit) == 0:
			avg = 0.0
		else:
			avg = sum_commit/len(adapt_commit)
		print("{0:22s} {1:14.4f} {2:16.4f} {3:14.2f}".format("MPI_Comm_adapt_commit", avg,  sum_commit, sum_commit/sum_total*100))

		if len(adapt_commit) == 0:
			avg = 0.0
		else:
			avg = sum_data_migration/len(adapt_commit)
		print("{0:22s} {1:14.4f} {2:16.4f} {3:14.2f}".format("Data migration",        avg,  sum_data_migration, sum_data_migration/sum_total*100))
		print("")
	else:
		print("No iMPI calls. This is probably a normal MPI run.")
