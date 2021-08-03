from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout
import numpy as np
import datetime

system_time = datetime.datetime.now()

print("\nSystem Time is:", system_time)

platform = Platform.getPlatformByName('CUDA')
properties = {'Precision':'double'}

# input topology, psf, and force field files 
print('Parsing system topology')

topology = CharmmPsfFile('water.psf')
parameters = CharmmParameterSet('top_spce_ions.rtf',\
            'par_spce_ions.prm' )

print('Parsing system coordinates')
coord = PDBFile('water.pdb')

# for using PBC in OpenMM, we need to make sure that
# the origin of the sytem is at (0,0,0)
# and that the extremum of the system is at (Lx, Ly, Lz)
# Boxl here is 3.9224 nm

xyz = np.array(coord.positions/nanometer)
xyz[:,0] += 3.9224/2
xyz[:,1] += 3.9224/2
xyz[:,2] += 3.9224/2
coord.positions = xyz*nanometer

topology.setBox(3.9224*nanometer,3.9224*nanometer, 3.9224*nanometer)

#build a simulation system from topology and force field

system = topology.createSystem(parameters,
    nonbondedMethod=PME,
    nonbondedCutoff=1.2*nanometer,
    ewaldErrorTolerance=1e-5,
    constraints=HBonds,
    rigidWater=True,
    removeCMMotion=True
)

# set the integrator. We want an NPT simulation, hence Langevin Integrator and Monte Carlo Barostat
integrator = LangevinIntegrator(298.15*kelvin, 10/picoseconds, 1.0*femtoseconds)
barostat = MonteCarloBarostat(1*bar,298.15*kelvin,50)
system.addForce(barostat)

nsteps = 1000000
# Create simulation object
simulation = Simulation(topology.topology, system, integrator, platform, properties)

# save trajectories every 100 steps
simulation.reporters.append(DCDReporter('positions.dcd', 100))

# output data to file and to screen
simulation.reporters.append(StateDataReporter('sim.log', 100, step=True, temperature=True, potentialEnergy=True, kineticEnergy=True, volume=True, density=True, totalEnergy=True))
simulation.reporters.append(StateDataReporter(stdout, 100, step=True, totalEnergy=True, remainingTime=True, totalSteps=nsteps))

# setting initial positions
simulation.context.setPositions(coord.positions)

simulation.step(nsteps)

