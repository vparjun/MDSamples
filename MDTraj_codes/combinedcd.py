import mdtraj as md
import numpy as np

fileid = np.array([1, 3, 18, 50])
nstates = len(bubbles)

trajarr = []
for i in range(nstates):
    traj = md.load('traj_' + '{:2.0f}'.format(fileid[i]) + '.dcd', top='psffile.psf')
    trajarr.append(traj)
    print(traj.n_frames)

fulltraj = md.join(trajarr)
fulltraj.save_dcd('allframes.dcd')
