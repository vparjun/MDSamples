#!/bin/bash
#SBATCH -J lammps-bulk                    # Job Name
#SBATCH -o test.o%j                # Output file name (%j expands to jobID)
#SBATCH -e test.e%j                # Error file name (%j expands to jobID)
#SBATCH -N 1                       # Requesting 1 node
#SBATCH -n 16                      # and 16 tasks
#SBATCH -p normal                  # Queue name (normal, skx-normal, etc.)
#SBATCH -t 5:00:00                # Specify 24 hour run time

module load   intel/17.0.4
module load   impi/17.0.3
module load   lammps/16Mar18

export OMP_NUM_THREADS=2   

ibrun lmp_stampede -sf omp -pk omp 2 -in bulk.in > bulk.log
