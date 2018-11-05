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
		if "Darcy Simulation" in line:
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
		if "Darcy Simulation" in line:
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
Plot cells profile
'''
def plot_cells_vs_simday(xarr, yarr, figout):
	import matplotlib.pyplot as plt
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)

	xx = [x/3600/24 for x in xarr]
	yy = yarr
	host.plot(xx, yy, color='k')

	host.set_xlabel("Simulation time (days)")
	host.set_ylabel("Number of grid cells")
	#host.set_xlim(0,150)
	#host.set_ylim(4000,6000)
	plt.show()
	plt.savefig(figout, bbox_inches="tight")
	plt.close(fig)


def plot_cells_vs_wallhr(xarr, yarr, figout):
	import matplotlib.pyplot as plt
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)

	xx = [x/3600 for x in xarr]
	yy = yarr
	host.plot(xx, yy, color='k')

	host.set_xlabel("Elapsed time (hours)")
	host.set_ylabel("Number of grid cells")
	#host.set_xlim(0,2.7)
	#host.set_ylim(4000,6000)
	plt.show()
	plt.savefig(figout, bbox_inches="tight")
	plt.close(fig)



'''
Plot MPI ranks profile
'''
def plot_ranks_vs_simday(xarr, yarr, figout):
	import matplotlib.pyplot as plt
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)

	xx = [x/3600/24 for x in xarr]
	yy = yarr
	host.plot(xx, yy, color='k')

	host.set_xlabel("Simulation time (days)")
	host.set_ylabel("Number of MPI ranks")
	#host.set_xlim(0,150)
	host.set_ylim(0,17)
	plt.show()
	plt.savefig(figout, bbox_inches="tight")
	plt.close(fig)

def plot_ranks_vs_wallhr(xarr, yarr, figout):
	import matplotlib.pyplot as plt
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)

	xx = [x/3600 for x in xarr]
	yy = yarr
	host.plot(xx, yy, color='k')

	host.set_xlabel("Elapsed time (hours)")
	host.set_ylabel("Number of MPI ranks")
	#host.set_xlim(0,2.7)
	host.set_ylim(0,17)
	plt.show()
	plt.savefig(figout, bbox_inches="tight")
	plt.close(fig)



'''
Compute CPU-hours
'''
def compute_cpuhours(time_in_sec, num_cpus):
	import numpy
	return numpy.trapz(num_cpus, time_in_sec) / 3600
