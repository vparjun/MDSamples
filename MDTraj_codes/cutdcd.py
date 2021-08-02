import mdtraj as md

t = md.load('traj.dcd', top='psffiles.psf')
reqframes = int(4200)
t[0:reqframes].save_dcd('firstframes.dcd')
