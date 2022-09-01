#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 20:46:05 2022

@author: robertgc
"""

import spontaneous_fission as sf

#material = sf.material()
#material.add_nuclide('U235')

# nuclide = sf.nuclide('PU240')
# print(nuclide.get_lamb())

print(sf.data().df.loc['O16'])

uo2 = sf.material()

uo2.add_nuclide('U235', 0.04)
uo2.add_nuclide('U238', 0.96)
#uo2.add_nuclide('O16', 2.0)

#uo2.get_SFR()


# uo2.set_density(10.5)


# uo2.get_SFR()