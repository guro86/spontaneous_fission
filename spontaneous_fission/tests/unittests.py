#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:42:26 2022

@author: robertgc
"""

#import packages
import unittest
import sys
import os 

#Add parent path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../..'
            )
        )
    )

#Import spontaneous fission
import spontaneous_fission as sf


#Set of tests (only one) for the materials class
class test_material(unittest.TestCase):
    
    #Test the SFR calculation against pre-calculated value from serpent
    def test_SFR(self):
        
        #Material
        mat = sf.material()

        #Nuclides
        nuclides = {
               'O16'    :4.68470138170614E-02, 
               'U232'   :6.94469768393013E-15, 
               'U233'   :2.31214915745100E-11, 
               'U234'   :2.99148081430987E-08, 
               'U235'   :4.42131481806163E-04, 
               'U236'   :6.78385347121593E-05, 
               'U238'   :2.22968754873230E-02, 
               'NP237'  :4.47765188867715E-06, 
               'PU236'  :1.86622393795350E-14, 
               'PU238'  :7.34129320039848E-07, 
               'PU239'  :1.22348031497154E-04, 
               'PU240'  :2.86915260725346E-05, 
               'PU241'  :1.59409017487767E-05, 
               'PU242'  :2.44316277946802E-06, 
               'AM241'  :3.43242993898377E-07, 
               'CM242'  :6.80583783232581E-08, 
               'CM244'  :3.28676321696389E-08, 
               'CM246'  :3.10180320789068E-11, 
               }

        #Add nuclides
        mat.add_nuclides(nuclides)
        #Set density
        mat.set_density(10.5)
        #Set volume
        mat.set_volume(1)
        
        #Calculate SFR
        SFR = mat.get_SFR()
        
        #Check if almost equal, maximum diff of 4 fissions / s
        self.assertAlmostEqual(SFR, 277.,None,delta=4)
        
#If called as program, run the tests
if __name__ == '__main__':
    unittest.main()