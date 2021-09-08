import mdtraj as md
import numpy as np

topfile='Struct1.psf'
dcdfile='Struct1_prod.dcd'

traj = md.load(dcdfile, top=topfile)
top = traj.topology                                         # topology object for future use

nframes = traj.n_frames                                     # get numframes. no use per se

masses = np.array([ a.element.mass for a in top.atoms ])    # masses go as an input.
                                                            # Convinient if we dont want to include atoms in the rg comp
rg = md.compute_rg(traj,masses=masses)

index1 = top.select('resid 0 and name CA')             # idea is to make a 2D array of pairs of atoms of interest
index2 = top.select('resid 15 and name NT')            # we just have [atom1 atom2] (just one pair)

end2end_pair = np.transpose([index1, index2])
e2e = md.compute_distances(traj, end2end_pair)[:,0]  # just to make it from 2D array to 1D array for printing

outdata = np.zeros((nframes,3),dtype=np.float32)
outdata[:,0] = traj.time/1000                   # to picosecond
outdata[:,1] = rg*10                            # units are in nm by default, so converting to angstroms
outdata[:,2] = e2e*10       

np.savetxt('rg_e2e.txt',outdata,fmt='%8.3f\t%8.5f\t%8.5f')

