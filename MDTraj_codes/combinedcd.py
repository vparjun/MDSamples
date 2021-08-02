import matplotlib.pyplot as plt
import itertools
import mdtraj as md
import numpy as np
#from mywallfunction import mylj126wall

#traj = md.load('firstframes.dcd', top='water_Na.psf')
bubbles = np.array([2.0254, 2.1292, 2.2971, 2.5000, 2.7029, 2.8708, 2.9746])
nstates = len(bubbles)

trajarr = []
for i in range(nstates):
    traj = md.load('wbigbox_' + '{:.4f}'.format(bubbles[i]) + '.dcd', top='wbigbox.psf')
    trajarr.append(traj)
    print(traj.n_frames)
    #
    #topology = traj.topology
    #print(topology)

fulltraj = md.join(trajarr)
fulltraj.save_dcd('allframes.dcd')