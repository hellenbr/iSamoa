# -*- coding: utf-8 -*-
import sys
import os

if len(sys.argv) < 2 or sys.argv[1] in ['-help', '-h', '--help' , '--h']:
	sys.exit("Usage: python3 swe_quickcheck.py <swe console output>")

filename = sys.argv[1]
if not os.path.isfile(filename):
	sys.exit("SWE output file %s does not exist!" % filename)

print("\nChecking SWE output from %s ...\n" % filename)

simtime = []
walltime = []
numcells = []
numranks = []
timestep= []

f = open(filename, 'r')
for i, line in enumerate(f,1):
	if line.startswith("cfg") or line.startswith("CFG"):
		continue
	if "SWE Tsunami:" in line:
		arr = line.split()
		try:
			# Parse time step
			idx = arr.index("time")
			step = int(arr[idx+2])

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
				elif 'ns' in tmp:
					continue #igore nanosec
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
			timestep += [step]
		except ValueError:
			print("Parse error: probably corrupted line. Skipping line...")
			print("%s\n" % arr)
			continue
f.close()

print('{:^10} | {:^15} | {:^15} | {:^15} | {:^15}'.format("Ranks", "Sim Time (sec)", "Wall Time (sec)", "Cells", "Time Steps"))
print('{:^10} | {:^15} | {:^15} | {:^15} | {:^15}'.format("-"*10, "-"*15, "-"*15, "-"*15, "-"*15))
print('{:>10} | {:>15} | {:>15} | {:>15} | {:>15}'.format(numranks[0], round(simtime[0],2), round(walltime[0],2), numcells[0], timestep[0]))
pre_i = 0
for i in range(len(numranks)-1):
	if (numranks[i] != numranks[pre_i]):
		pre_i = i
		print('{:>10} | {:>15} | {:>15} | {:>15} | {:>15}'.format(numranks[i], round(simtime[i],2), round(walltime[i],2), numcells[i], timestep[i]))
print('{:>10} | {:>15} | {:>15} | {:>15} | {:>15}'.format(numranks[-1], round(simtime[-1],2), round(walltime[-1],2), numcells[-1], timestep[-1]))
print('{:^10} | {:^15} | {:^15} | {:^15} | {:^15}'.format("-"*10, "-"*15, "-"*15, "-"*15, "-"*15))
print('')

