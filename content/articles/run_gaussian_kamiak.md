Title: Running a calculation with Gaussian
Date: 2019-06-03 23:00
Modified: 2019-06-03 23:20
Category: misc
Tags: gaussian, kamiak, wsu, misc
Slug: gaussianjob
Authors: Ernek
Summary: How to run a job with Gaussian on Kamiak HPC cluster at WSU. Submission script, input and output files.

# Starting with Gaussian  

In this post I will present essential steps needed to sucessfully run your first Gaussian calculations.
We will run Gaussian on the WSU HPC cluster **Kamiak** where Gaussian09 is already installed and available to licensed users.

## Input File

All directives of your job as well as the system's molecular geometry should be contained in the **input** file. Here is an example of a **HF single point energy calculation**:

```bash
%chk=test_run                    ! Checkpoint file needed to save info needed to restart job    
#P hf/cc-pVDZ                    ! Job directives . Hartree Fock single point calc with cc-pVDZ basis sets
                                 ! Empty line ... This empty line is needed
job name                         ! Job name descriptor
                                 ! Empty line ... This empty line is needed
-1 1                             ! Charge Spin
Al 4.158934 12.319204 8.139289   ! Atomic-symbol x-coord y-coord z-coord
O 5.204656 12.33906 6.772874
H 5.524529 11.426276 6.453445
O 4.893735 13.419199 9.302062
H 5.82317 13.510635 9.461939
O 2.621193 13.123312 7.624101
H 2.124667 13.404712 8.410292
O 3.723529 10.689556 8.948275
H 3.223616 10.091097 8.387248
                                 ! Empty line ... This empty line is needed                   
```

With this simple input file (let's save it and name it: "gaussian_test.com"), the only other thing we need in order to run our first Gaussian calculation on the **Kamiak** cluster is a submission script to launch our calculation on **Kamiak** nodes.

## Submission Script for Gaussian on Kamiak

```bash
#!/bin/bash

#SBATCH --job-name=test       ###Job Name
#SBATCH --partition=kamiak    ###Partition on which to run
#SBATCH --nodes=1             ###Number of nodes to use
#SBATCH --ntasks-per-node=20   ###Number of tasks per node (aka MPI processes)
#SBATCH --cpus-per-task=1    ###Number of cpus per task (aka OpenMP threads)
#SBATCH --time=7-00:00:00
module load gaussian          ###Load gaussian module on Kamiak

finit=$1                      ###The base name of your input file  
fend='.com'                     
foutend='.out'

export GAUSS_SCRDIR="$(mkworkspace -q)"  ###Creates a workspace

g09 < ${finit}${fend} > ${finit}${foutend}                                                        

```
Let's save this piece of bash code and save it as: "sub_g09.slurm". Since our input file name is "gaussian_test.com" to run **Gaussian** with this submission script we would type:

```bash
sbatch sub_g09.slurm gaussian_test     ### "gaussian_test" is the base name of our input file  
```

Running this job should generate an output-file named "gaussian_test.out" that will contain all the info of this calculation.
Let's look at some of its elements before we explain one example with a bit more complicated workflow.

## Output File

After the job has run to completion you can check the "gaussian_test.out" output-file located in the folder where you launched your calculation from. You can check the **"Normal termination of Gaussian..."** sentence at the end of the output file.  
The HF Energy after several SCF cycles can normally be found by searching for **"SCF Done:  E(RHF)"**:

```bash
grep -H 'SCF Done:  E(RHF)' gaussian_test.out
```
There are many other interesting properties you will find in the output file i.e Atomic Mulliken partial charges, info about dipole moments etc...

For more info about **input** options or general examples for each type of calculation you can check Gaussian's website directly [here](http://gaussian.com/keywords/) : `http://gaussian.com/keywords/`.

Files related to this simple Gaussian calculation can be found [here](https://github.com/Ernek/NMR/tree/master/hf-run). (note: no output file provided)

## Exploring different basis sets and QM methods with Gaussian

Now, let's increase complexity and try to automate the calculation of the magnetic shielding tensor of Al nucleus in aluminate. Let's use the same molecular geometry we used in our previous HF calculation. We will explore 2 different QM methods and investigate how does the Al shielding value change with an increase in the size of the basis sets (let's use pC[X]VZ (X=D,T,Q) basis sets family).

### Generating the Input File

My strategy to automate this task was to create a python code with the following algorithm in mind:

    1. Read the molecular geometry of interest from an .xyz file
    2. Generate the input file containing said .xyz coordinates and job directives
      + Generating a single input file for each QM/basis sets combination
    3. Generate a Gaussian submissions script associated with each previously generated input file  
