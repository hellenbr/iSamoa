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

	f = open(filename, 'r')
	for i, line in enumerate(f,1):
		if "Phase statistics:" in line:
			# Number of ranks
			line = linecache.getline(filename, i+2) #Line starts with "Num ranks:"
			if "Num ranks:" in line:
				larr = line.split()
				nranks = int(larr[-1])
				numranks += [nranks]
			else:
				sys.exit("Line Num ranks not found. Program abort!")
			
			# t_phase (Total phase time)
			line = linecache.getline(filename, i+14) #Line starts with "Phase time:"
			if "Phase time:" in line:
				larr = line.split()
				idx = larr.index("time:")
				phase_time = float(larr[idx+1]) #wall time, not summed
				t_phase += [phase_time]
			else:
				sys.exit("Line Num ranks not found. Program abort!")
			
			# t_refine (grid refinement time)
			line = linecache.getline(filename, i+8) #Line starts with "Adaptions:"
			if "Adaptions:" in line:
				larr = line.split()
				idx = larr.index("time:")
				refine_time = float(larr[idx+1])/float(nranks)
				t_refine += [refine_time]
				
				# t_conformity (conformity check time)
				idx = larr.index("integrity:")
				conformity_time = float(larr[idx+1])/float(nranks)
				t_conformity += [conformity_time]
				
				# t_lb (load balancing time)
				idx = larr.index("balancing:")
				lb_time = float(larr[idx+1])/float(nranks)
				t_lb += [lb_time]
			else:
				sys.exit("Line Adaptions not found. Program abort!")
		 
			# t_compute (computation time) := t_transport + t_gradient + t_perm + t_err + t_pressure
			compute_time = 0.0
			# t_transport
			line = linecache.getline(filename, i+4) #Line starts with "Transport:"
			if "Transport:" in line:
				larr = line.split()
				idx = larr.index("time:")
				compute_time += float(larr[idx+1])/float(nranks)
			else:
				sys.exit("Line Transport not found. Program abort!")
			# t_gradient
			line = linecache.getline(filename, i+5) #Line starts with "Gradient:"
			if "Gradient:" in line:
				larr = line.split()
				idx = larr.index("time:")
				compute_time += float(larr[idx+1])/float(nranks)
			else:
				sys.exit("Line Gradient not found. Program abort!")
			# t_perm
			line = linecache.getline(filename, i+6) #Line starts with "Permeability:"
			if "Permeability:" in line:
				larr = line.split()
				idx = larr.index("time:")
				compute_time += float(larr[idx+1])/float(nranks)
			else:
				sys.exit("Line Permeability not found. Program abort!")
			# t_err
			line = linecache.getline(filename, i+7) #Line starts with "Error Estimate:"
			if "Error Estimate:" in line:
				larr = line.split()
				idx = larr.index("time:")
				compute_time += float(larr[idx+1])/float(nranks)
			else:
				sys.exit("Line Error Estimate not found. Program abort!")
			# t_pressure
			line = linecache.getline(filename, i+9) #Line starts with "Pressure Solver:"
			if "Pressure Solver:" in line:
				larr = line.split()
				idx = larr.index("time:")
				compute_time += float(larr[idx+1])/float(nranks)
			else:
				sys.exit("Line Pressure Solver not found. Program abort!")
			t_compute += [compute_time]
			
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
	return (numranks, t_phase, t_compute, t_refine, t_conformity, t_lb, t_others, t_impi)

'''
Compute CPU-hour of the run
'''
def compute_cpuhours(time_in_sec, num_cpus):
	import numpy
	return numpy.trapz(num_cpus, time_in_sec) / 3600

'''
A generic 1D plot interface
'''
def plot_1d(xvec, yvec, xrange, yrange, xtitle, ytitle, outfig):
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)
	host.plot(xvec, yvec, color='k')
	if (xrange != [0,0]):
		host.set_xlim(xrange)
	if (yrange != [0,0]):
		host.set_ylim(yrange)
	host.set_xlabel(xtitle)
	host.set_ylabel(ytitle)
	plt.savefig(outfig, bbox_inches="tight")
	plt.show()
	plt.close(fig)

'''
A generic 1D plot interface for 2 datasets (2 y-axes)
'''
def plot_1d_2scales(xvec, yvec1, yvec2, xrange, yrange1, yrange2, xtitle, ytitle1, ytitle2, outfig):
	# Figure setup
	fig = plt.figure(frameon = True)
	#fig, ax1 = plt.subplots()
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4)

	# First plot ax1
	ax1 = fig.add_subplot(1,1,1)
	ax1.plot(xvec, yvec1, 'b-')
	ax1.set_xlabel(xtitle, color='k')
	ax1.set_ylabel(ytitle1, color='b')
	ax1.tick_params('y', colors='b')
	if (xrange != [0,0]):
		ax1.set_xlim(xrange)    
	if (yrange1 != [0,0]):
		ax1.set_ylim(yrange1)

	# Second plot ax2
	ax2 = ax1.twinx()
	ax2.plot(xvec, yvec2, 'r-')
	ax2.set_ylabel(ytitle2, color='r')
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
	(numranks, t_phase, t_compute, t_refine, t_conformity, t_lb, t_others, t_impi) = getdata_stat(filename)

	total_sim_time = sum(t_phase)
	compute_time = sum(t_compute)
	refine_time = sum(t_refine)
	comform_time = sum(t_conformity)
	lb_time = sum(t_lb)
	others_time = sum(t_others)
	impi_time = sum(t_impi)

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
	total_time = 0.0
	init_adapt = 0.0
	probe_adapt = 0.0
	adapt_begin = 0.0
	adapt_commit = 0.0

	f = open(filename, 'r')
	for i, line in enumerate(f,1):
		if "init_adapt" in line:
			arr = line.split()
			idx = arr.index("init_adapt")
			init_adapt += float(arr[idx+1])
		elif "probe_adapt" in line:
			arr = line.split()
			idx = arr.index("probe_adapt")
			probe_adapt += float(arr[idx+1])
		elif "adapt_begin" in line:
			arr = line.split()
			idx = arr.index("adapt_begin")
			adapt_begin += float(arr[idx+1])
		elif "adapt_commit" in line:
			arr = line.split()
			idx = arr.index("adapt_commit")
			adapt_commit += float(arr[idx+1])
		elif "total adapt time" in line:
			arr = line.split()
			idx = arr.index("time")
			total_time += float(arr[idx+1])
	f.close()

	print("")
	print("{0:22s} {1:18s} {2:10s}".format("Function", "Acc. time (sec)", "Percent (%)"))
	print("{0:22s} {1:18s} {2:10s}".format("----------------", "----------------", "-----------"))
	print("{0:22s} {1:14.4f} {2:10.2f}".format("Total adaptation", total_time, 100.0))
	print("{0:22s} {1:14.4f} {2:10.2f}".format("MPI_init_adapt", init_adapt, init_adapt/total_time*100))
	print("{0:22s} {1:14.4f} {2:10.2f}".format("MPI_Comm_probe_adapt", probe_adapt, probe_adapt/total_time*100))
	print("{0:22s} {1:14.4f} {2:10.2f}".format("MPI_Comm_adapt_begin", adapt_begin, adapt_begin/total_time*100))
	print("{0:22s} {1:14.4f} {2:10.2f}".format("MPI_Comm_adapt_commit", init_adapt, adapt_commit/total_time*100))
	print("")
