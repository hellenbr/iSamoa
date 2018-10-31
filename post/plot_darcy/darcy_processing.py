'''
This function returns data (simulation time, wall time, number of cells) in 3 equal-sized arrays
This is for plotting grid cell growth profile during the simulation
'''
def get_data(filename):
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
def get_data_by_day(filename):
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
