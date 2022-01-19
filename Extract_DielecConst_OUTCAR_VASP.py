#!/usr/bin/env python

import os
import numpy as np

# PEP 8


def parse_outcar(fname):

    elec = np.zeros((3, 3))

    ion = np.zeros((3, 3))


    with open(fname, "r") as fd:

        line = fd.readline()  # read first line
        while "MACROSCOPIC STATIC DIELECTRIC TENSOR (including local field effects in DFT)" not in line:
            line = fd.readline()


        for ii in range(3):  # read electronic part

            values = fd.readline().split()

            for jj, value in enumerate(values):

                elec[ii, jj] = float(value)

        while "MACROSCOPIC STATIC DIELECTRIC TENSOR IONIC CONTRIBUTION" not in line:

            line = fd.readline()


        fd.readline()  # skip line

        for ii in range(3):  # read ionic part

            values = fd.readline().split()

            ion[ii] = [float(value) for value in values]

            # ion[ii] = list(map(float, values))

    return elec, elec + ion


def print_header():

    headers = ['material',

               'eps_el_x', 'eps_el_y', 'eps_el_z',

               'eps_tot_x', 'eps_tot_y', 'eps_tot_z']

    print(", ".join(headers))



def print_constants(material, elec,  tot):

    values = []

    values += [f"{value:.6e}" for value in np.diag(elec)]

    values += [f"{value:.6e}" for value in np.diag(tot)]

    print(f"{material}, " + ", ".join(values))



if __name__ == '__main__':



    print_header()



    for material in os.listdir('PATH'):

        elec, tot = parse_outcar(f'PATH/{material}/Bulk/DFT/OUTCAR')

        print_constants(material, elec, tot)
        

