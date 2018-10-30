def getdata_cells(filename):
	# Define output arrays
	simtime = []
	walltime = []
	numcells = []

	f = open(filename, 'r')
	for i, line in enumerate(f,1):
		'''
		if "Darcy Initialzation" in line:
			arr = line.split()
			# Elapsed time at arr[15] 
			t_wall = float(arr[15].replace(',',''))
			# Single rank #cells at arr[17]
			ncells_per_rank = int(arr[17].replace(',',''))
			# #ranks at arr[19] 
			nranks = int(arr[19].replace(',',''))
			# Put data in output arrays
			simtime += [float(0)]
			walltime += [t_wall]
			numcells += [ncells_per_rank * nranks]
		'''
		if "Darcy Simulation" in line:
			arr = line.split()

			# Parse simulation time
			idx = arr.index("time:")
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
					continue
				elif 's' in tmp:
					tsim += int(tmp.replace('s',''))

			# Parse wall time
			idx = arr.index("(sec):")
			twall = float(arr[idx+1].replace(',',''))

			# Parse cells and ranks
			idx = arr.index("cells:")
			ncells = int(arr[idx+1].replace(',',''))
			idx = arr.index("ranks:")
			nranks = int(arr[idx+1])

			# Put data in output arrays
			simtime += [tsim]
			walltime += [twall]
			numcells += [ncells * nranks]
	f.close()
	return (simtime, walltime, numcells)

def getdata_cells_by_day(filename):
	# Define output arrays
	simtime = []
	walltime = []
	numcells = []

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
				idx = arr.index("time:")
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
						continue
					elif 's' in tmp:
						tsim += int(tmp.replace('s',''))
				# Parse wall time
				idx = arr.index("(sec):")
				twall = float(arr[idx+1].replace(',',''))
				# Parse cells and ranks
				idx = arr.index("cells:")
				ncells = int(arr[idx+1].replace(',',''))
				idx = arr.index("ranks:")
				nranks = int(arr[idx+1])
				# Put data in output arrays
				simtime += [tsim]
				walltime += [twall]
				numcells += [ncells * nranks]   
	f.close()
	return (simtime, walltime, numcells)


def plot_cells_vs_simtime(simtime, numcells, figout):
	import matplotlib.pyplot as plt
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)
	host.set_xlabel("Simulation time (sec)")
	host.set_ylabel("Number of cells")
	host.plot(simtime, numcells, color='k')
	plt.savefig(figout, bbox_inches="tight")
	plt.close(fig)


def plot_cells_vs_walltime(walltime, numcells, figout):
	import matplotlib.pyplot as plt
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)
	host.set_xlabel("Elapsed time (sec)")
	host.set_ylabel("Number of cells")
	host.plot(walltime, numcells, color='k')
	plt.savefig(figout, bbox_inches="tight")
	plt.close(fig)


def plot_cells_vs_simday(simtime, numcells, figout):
	import matplotlib.pyplot as plt
	# Figure setup
	fig = plt.figure(frameon = True)
	# 9.6 inch x 200 dpi = 1920
	# 5.4 inch x 200 dpi = 1080
	fig.set_size_inches(9.6, 5.4) 
	host = fig.add_subplot(1,1,1)
	host.set_xlabel("Simulation time (days)")
	host.set_ylabel("Number of cells")

	#host.set_ylim(10,15)
	#host.set_xlim(0,200)

	simday = [int(x / 3600 / 24) for x in simtime]
	ncells = [float(x / 1000) for x in numcells]

	host.plot(simday, ncells, color='k')
	plt.savefig(figout, bbox_inches="tight")
	plt.close(fig)
