import mdtraj as md
t = md.load('positions.dcd', top='water_Na.psf')
t[0:4200].save_dcd('firstframes.dcd')