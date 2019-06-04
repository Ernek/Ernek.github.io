Title: Running a calculation with Gaussian
Date: 2019-06-03 23:00
Modified: 2019-06-03 23:20
Category: misc
Tags: gaussian, kamiak, wsu, misc
Slug: gaussianjob
Authors: Ernek
Summary: How to run a job with Gaussian on Kamiak HPC cluster at WSU. Submission script, input and output files.

In this post I will present essential steps needed to sucessfully run your first Gaussian calculations.
We will run Gaussian on the WSU HPC cluster **Kamiak** where Gaussian09 is already installed and available to licensed users.

## Input File

All directives of your job as well as the system's molecular geometry should be contained in the **input** file. Here is an example of a **HF single point energy calculation**:

```bash
%chk=test_run                    # Checkpoint file needed to save info needed to restart job    
\&#35P; hf/cc-pVDZ                   # Job directives . Hartree Fock single point calc with cc-pVDZ basis sets
                                 # Empty line ... This empty line is needed
job name                         # Job name descriptor
                                 # Empty line ... This empty line is needed
0 1                              # Charge Spin
Al 4.158934 12.319204 8.139289   # Atomic-symbol x-coord y-coord z-coord
O 5.204656 12.33906 6.772874
H 5.524529 11.426276 6.453445
O 4.893735 13.419199 9.302062
H 5.82317 13.510635 9.461939
O 2.621193 13.123312 7.624101
H 2.124667 13.404712 8.410292
O 3.723529 10.689556 8.948275
H 3.223616 10.091097 8.387248
                                 # Empty line ... This empty line is needed                   
```
