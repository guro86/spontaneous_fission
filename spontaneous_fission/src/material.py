# -*- coding: utf-8 -*-


from .data import data

import numpy as np

class material():
    
    _data = data()
    
    def __init__(self):
        
        self.composition = []
        
        self.density = None 
        self.volume = None 
        
    def set_density(self,density):
        
        self.density = density
        
    def set_volume(self,volume):
            
            self.volume = volume
        
    def add_nuclide(self,name,weight):
       
        self.composition.append((weight,nuclide(name)))
    
    def get_SFR(self):
        
        #Get nuclides
        nuclides = [nuclide for _,nuclide in self.composition]
        
        #Get weights 
        weights = np.array([weight for weight,_ in self.composition])
        
        #Get lambdas
        lambs = np.array([nuclide.get_lamb() for nuclide in nuclides])
        
        print(nuclides,weights,lambs)
        
        
class nuclide():
    
    _data = data()
    
    def __init__(self,name):
        
        #Name of nuclide
        self.name = name 
        
    def get_hl(self):
        
        #get data and name
        data = self._data
        name = self.name
        
        
        if data.check_name(name):
            #get halflife
            print(name)
            hl = float(data.get_item(name,'half_life_sec'))
            
        else:
            hl = np.nan
        
        
        return hl
        
    def get_lamb(self):
        
        #Half life
        hl = self.get_hl()
        
        #Calc lambda
        lamb = np.log(2) / hl
        
        #Return lambda
        return lamb