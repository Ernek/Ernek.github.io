Title: Exploring different basis sets and QM methods with Gaussian
Date: 2023-04-22 12:00
Modified: 2023-04-22 12:00
Category: misc
Tags: gaussian, kamiak, wsu, misc
Slug: bset_qm_gaussian
Authors: Ernek
Summary: How to run an automated job with Gaussian to explore the effect of basis sets and QM method on NMR calculations

## Exploring different basis sets and QM methods with Gaussian

Now, let's increase complexity and try to automate the calculation of the magnetic shielding tensor of Al nucleus in aluminate. Let's use the same molecular geometry we used in our previous HF calculation. We will explore 2 different QM methods and investigate how does the Al shielding calculated value change with an increase in the size of the basis sets (let's use pC[X]VZ (X=D,T,Q) basis sets family) used to describe the Al atomic orbitals.

### Generating the Input and Job-submission files

My strategy to automate this task was to create a python code with the following algorithm in mind:

    1. Read the molecular geometry of interest from an .xyz file
    2. Generate the input file containing said .xyz coordinates and job directives
      + Generating a single input file for each QM/basis sets combination
    3. Generate a Gaussian submissions script associated with each previously generated input file  

The .xyz file should be on the same folder of our python code (I will get into the python code in a moment) and shold look like this:

```bash
9

Al 4.158934 12.319204 8.139289   
O 5.204656 12.33906 6.772874
H 5.524529 11.426276 6.453445
O 4.893735 13.419199 9.302062
H 5.82317 13.510635 9.461939
O 2.621193 13.123312 7.624101
H 2.124667 13.404712 8.410292
O 3.723529 10.689556 8.948275
H 3.223616 10.091097 8.387248
```

We can save it as "al-oh_4_config.xyz". The first line is the number of atoms and the block of data is similar to the format we used in the **input** file above. Leave that empty line between the number of atoms (N) and the start of the coordinates' data (this is the format of .xyz files).

Let's look at our python code by sections. The first snippet of code is just to import modules.

```{py}
#!/usr/bin/env python
# coding: utf-8

# Code to transform an .xyz snap file to Gaussian input exploring several Basis Sets and QM methods

#%%
# Importing modules ######################################################################################

import sys, os
import numpy as np
import pandas as pd
import math
import fnmatch    			# To read files
from django.utils.text import slugify   # To convert special characters to valid file_path names
import itertools
from unidecode import unidecode
import re
import argparse  

```
We need to use core-valence Dunning basis sets for Al. These basis sets are not included in the default keywords of Gaussian software. We need to explicitly include basis-sets functions' coefficients and exponents for each atom in the input file (i.e we cannot use hf/cc-pCVZ in the input because cc-pCVZ basis sets keyword will not be recognized by Gaussian).   

We make use of a cloned repository of basis sets containing the EMSL Basis-Sets Database (you can find the basis_set_exchange repository [here](https://github.com/aoterodelaroza/emsl_basis_set_library) )

Let's define the some functions that will be necessary to create our input files:

```{py}
#%%
# Functions   ############################################################################################

def u_slugify(txt):
        """A custom version of slugify that retains non-ascii characters. The purpose of this
        function in the application is to make folder names readable by command line tools."""
        txt = txt.strip() # remove trailing whitespace
        txt = re.sub('\*', '-pol', txt, re.UNICODE) # replace * for text pol=polarization funcitons
        txt = re.sub('\+', '-dif', txt, re.UNICODE) # replace + for text dif=diffuse funcitons
        txt = re.sub('\(', '-', txt, re.UNICODE) # replace left parenthesis with dash
        txt = re.sub(r'[?,:!@#~`=$%^&\)\[\]{}<>]','',txt, re.UNICODE) # remove some characters altogether
        return txt

def get_bse_local(loc_basis, element):
        """A function to extract element basis sets data from local EMSL database located
        in /data/clark/ernesto/bss/emsl_basis_set_library/gbs """
        addrs = '/data/clark/ernesto/bss/emsl_basis_set_library/gbs/'
        with open(addrs + str(loc_basis) + '.gbs', 'r') as fbasis:
            lines = fbasis.readlines()
            bs_list = []
            for i in range(len(lines)):
                if lines[i].split()[0] == str('-') + element:
                    oidx = i
                    oline = lines[oidx]
                    while not oline.split()[0] == '****':
                        bs_list.append(oline)
                        oidx += 1
                        oline = lines[oidx]
                else:
                    continue
        return bs_list

```

The second function contains a variable "addrs" that should be equal to the path where you will save the basis-sets EMSL Database repository (note you will have to clone the repo on Kamiak from [here](https://github.com/aoterodelaroza/emsl_basis_set_library)).

Now we can define our Main function. Our code creates folders for each combination of Method and Basis-sets and generates the corresponding input files. Additionally, the code creates the corresponding Gaussian submission scripts ready to be launched on Kamiak cluster with no additional flags.  

```{py}
#%%

# Main Function -- Program  #########################################################################

def main(fname, charge, spin, key_run_01):

    key_method_01 = 'giao'

    #Create dictionary with QM methods to be used in Gaussian calculation
    functionals = {'hf': ['hf'],
                   'mp2': ['mp2'],
                   'gga': ['pbe','blyp']
                  }
    #Create dictionary with basis sets to explore with each QM method
    basis_sets = {'core_valence': [],
		  'dunning': ['cc-pVDZ','cc-pVTZ','cc-pVQZ']
                 }

    core_valence_basis = list(itertools.product(['cc-pCV'], ['DZ','TZ','QZ']))
    add_val = []
    for k in core_valence_basis:
        add_val.append(str(k[0]+k[1]))
        add_val.append('aug-'+ str(k[0]+k[1]))

    for key,val in basis_sets.items():
        if key == 'core_valence':
            for p in add_val:
                if p not in val:
                    basis_sets[key].append(p)
                else:
                    continue
        else:
            continue

    cwd = os.getcwd()  # get Current Working Directory

    # Initializing input file reading and outputting file
    with open(fname, 'r') as f:
        cnt = 0
        a = []
        for line in f:
            if cnt == 0:
                N = line.split()[0]
                cnt += 1
            elif cnt == 1:
                cnt += 1
            else:
                a.append(line)
                cnt += 1

    for fkey,fval in functionals.items():
        for i in fval:
            try:
                os.makedirs(str(cwd)+'/'+i)
            except FileExistsError:
                pass

            for bkey,bval in basis_sets.items():
                try:
                    os.makedirs(str(cwd)+ '/' + i + '/' + bkey)
                except FileExistsError:
                    pass
                if  bkey == 'core_valence':
                    for j in bval:
                        try:
                            os.makedirs(str(cwd)+ '/' + i + '/' + bkey + '/' + u_slugify(j))
                        except FileExistsError:
                            pass

                        al_bse = get_bse_local(j, 'Al')

                        for p in [basis_sets['dunning'][indx] for indx,t in enumerate(basis_sets['dunning']) if t[-2]!='5']:
                            out_fname = str(fname).rpartition('.')[0] + '_' + i + '_' + u_slugify(j) + '_' + u_slugify(p) + '.com'
                            os.chdir(str(cwd)+ '/' + i + '/' + bkey + '/' + u_slugify(j))
                            o_bse = get_bse_local(p, 'O')
                            h_bse = get_bse_local(p, 'H')
                            with open(out_fname, 'w') as output:
                                output.write('%chk=' + str(fname).rpartition('.')[0] + '_' + i + '_' + u_slugify(j) +'_' + u_slugify(p) + '\n'
                                            + f"#P {key_run_01}={key_method_01} {i}/Gen"                              
                                            + '\n\n' + str(fname).rpartition('.')[0] + '_' + i + '_' + u_slugify(j) +'_' + u_slugify(p) + '\n\n'
                                            + str(charge) + ' ' + str(spin) + '\n'                             
                                            + "".join(map(str, a))
                                            + '\n'
                                            + "".join(map(str,al_bse))
                                            + '****\n'
                                            + "".join(map(str,o_bse))
                                            + '****\n'
                                            + "".join(map(str,h_bse))
                                            + '****\n'
                                            + '\n'
                                        )

                            sub_fname = 'sub_g09'+'_'+ u_slugify(p)+'.slurm'
                            with open(sub_fname, 'w') as sub_out:
                                sub_out.write('#!/bin/bash' +'\n'                                   
                                              +'#SBATCH --job-name=' + i + '_' + slugify(j) + '_' + u_slugify(p) + '   ###Job Name' + '\n'
                                              +'#SBATCH --partition=clark,kamiak,cas  ###Partition on which to run' + '\n'
                                              +'#SBATCH --nodes=1           ###Number of nodes to use' +'\n'
                                              +'#SBATCH --ntasks-per-node=20 ###Number of tasks per node (aka MPI processes)' +'\n'
                                              +'#SBATCH --cpus-per-task=1   ###Number of cpus per task (aka OpenMP threads)' +'\n'
                                              +'#SBATCH --time=7-00:00:00' + '\n'
                                              +'module load gaussian' + '\n'
                                              +'\n'
                                              +'finit=' + '"' + str(fname).rpartition('.')[0] + '_' + i + '_' + u_slugify(j) +'_' + u_slugify(p) + '"' + '\n
'
                                              +'fend=' + '"' + '.com' + '"' + '\n'
                                              +'foutend=' + '"'+ '.out' + '"' +'\n'
                                              +'\n'
                                              +'export GAUSS_SCRDIR="$(mkworkspace -q)" ' +'\n'
                                              +'g09 < ${finit}${fend} > ${finit}${foutend}' + '\n'                     
                                              +'\n'
                                            )
                        os.chdir(cwd)
                else:
                    continue
    os.chdir(cwd)

```

and finally the last bit to make our code modular and define some flags to specify for each molecular system. Flags include:

    1. Name of the .xyz file
    2. Total Charge of the system
    3. Spin state of the system
    4. Method:
        + HF single point calculation , if no flag present
        + NMR shielding tensor calculation , if option "-m nmr" is included

```{py}
#%%    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Enter the xyz filename, i.e "aloh4.xyz" ')
    parser.add_argument('charge', help='Enter the system total charge, i.e "-1" or "1" ', type=int)
    parser.add_argument('spin', help='Enter spin state of the whole system i.e "1" ', type=int)
    parser.add_argument("-m", "--method", help='Enter job directive, i.e "nmr";' \
                        +'if no arg passed defaults to single point energy calc', type=str, choices=['nmr'])
    args = parser.parse_args()

    if args.method:
        print(f"Method selected is: {args.method}")
    else:
        print("Default method. Generating input with single point energy calculation")
    main(args.filename, args.charge, args.spin, args.method)

```

After running this code you can launch the jobs using the generated submission scripts.
Remember to create an environment on Kamiak to install necessary python modules

```bash
conda create -n env_name
conda activate env_name
conda install pandas
conda install django
.
.

```
This code runs with the latests versions of python 3 since it uses "formatted string literals" (f-string methods).
You can find this python code in one piece in one of my Github repositories: [https://github.com/Ernek/NMR/tree/master/nmr-run](https://github.com/Ernek/NMR/tree/master/nmr-run) . In its current version it explores HF, MP2, BLYP and PBE methods and uses a combination of Al core-valence basis sets (aug-/cc-pC[D,T,]VZ) combined with cc-pV[D,T,Q]Z for oxygen [O] and hydrogen [H] atoms. 

Details about the code functionality are limited to most fundamental aspects. Test your outputs at your own discretion.

Have fun!

