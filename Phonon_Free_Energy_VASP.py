#!/usr/bin/env python
import argparse
import numpy as np
import sys

parser = argparse.ArgumentParser(description='Calculate the free energy contribution of phonons')
parser.add_argument('OUTCAR', type=str, help='The location of the OUTCAR to parse')
parser.add_argument('T', type=float, help='The temperature in Kelvin')
args = parser.parse_args()

kT = args.T * 8.61733034e-5

with open(args.OUTCAR) as f:
    omega = []

    for line in f:
        if 'meV' not in line:
            continue
        value = float(line.split()[-2])
        omega.append(value)

omega = np.sort(omega) / 1e3
omega_op = omega[3:]
omega_ac = omega[3:6]

E_free_op = omega_op/2
if kT > 0:
    E_free_op += kT * np.log(1 - np.exp(-omega_op / kT))

x = np.linspace(0, 1, 1000)[1:]
weight_x = x**2
weight_x /= weight_x.sum()

E_free_ac = np.zeros(3)
for i in range(3):
    omega_x = x * omega_ac[i]
    E_free_x = weight_x * omega_x / 2
    if kT > 0:
        E_free_x += weight_x * kT * np.log(1 - np.exp(-omega_x / kT))
    E_free_ac[i] = E_free_x.sum()

print('Contributions')
for ii, (E_freei, omegai) in enumerate(zip(E_free_ac, omega_ac), 1):
    print('ac {:d}-{:d} (0-{:.2f}meV): {:.1f}meV'.format(ii, ii+3,
                                                      omegai * 1e3,
                                                      E_freei * 1e3))
for ii, (E_freei, omegai) in enumerate(zip(E_free_op, omega_op), 1):
    print('op {:2d} ({:.2f}meV): {:.1f}meV'.format(ii,
                                                    omegai * 1e3,
                                                    E_freei * 1e3))

print('accoustic energy (-ST): {:.6e} eV'.format(E_free_ac.sum()))
print('optical energy (-ST): {:.6e} eV'.format(E_free_op.sum()))
print('total energy (-ST): {:.6e} eV'.format(E_free_ac.sum() + E_free_op.sum()))
