#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 20:46:05 2022

@author: robertgc
"""

import spontaneous_fission as sf

#uo2
uo2 = sf.material()

uo2.add_nuclide('U235', 0.04)
uo2.add_nuclide('U238', 0.96)
uo2.add_nuclide('O16', 2.0)
uo2.set_density(10.5)


print(uo2.get_SFR())

#Nuclides
nuclide = sf.nuclide('U235')
nuclide.get_hl()
nuclide.get_SF_percent()
nuclide.get_item('abundance')
