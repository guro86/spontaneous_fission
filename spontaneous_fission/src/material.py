# -*- coding: utf-8 -*-


from .data import data
import numpy as np
from scipy.constants import N_A

class material():
    
    #Data object to retrive decay data
    _data = data()
    
    def __init__(self):
        '''
        Constructs a new material.

        Returns
        -------
        None.

        '''
        
        #Composition of the material
        self._composition = []
        
        #Volume and density
        self.density = None 
        self.volume = None 
        
    def set_density(self,density):
        '''
        Sets the density of the material in g/cm3.

        Parameters
        ----------
        density : float
            density in g/cm3

        Returns
        -------
        None.

        '''
                
        self.density = density
        
    def set_volume(self,volume):
        '''
        Sets the volume of the material.

        Parameters
        ----------
        volume : float
            volume in cm3

        Returns
        -------
        None.

        '''    
        
        self.volume = volume
        
    def add_nuclide(self,name,fraction):
        '''
        Adds a nuclide to the material.

        Parameters
        ----------
        name : str
            String name of the material, e.g. U235
        fraction : float
            Atomic fraction or density

        Returns
        -------
        None.

        '''
        
        self._composition.append((fraction,nuclide(name)))
        
    def add_nuclides(self,nuclides):
        '''
        Add several nuclides as dictionary.

        Parameters
        ----------
        nuclides : dict
            A dictionary with several names and atomic fractions.
            E.g. {'U235':.5,'Pu239':.5}

        Returns
        -------
        None.

        '''
    
        
        for name, fraction in nuclides.items():
            self.add_nuclide(name, fraction)
    
    def get_nuclides(self):
        '''
        Get a list of present nuclide names

        Returns
        -------
        list
            E.g. ['U235']

        '''
        
        #Get nuclides
        return [nuclide for _,nuclide in self._composition]
    
    def get_fractions(self):
        '''
        Get the normalized atomic fractions. 

        Returns
        -------
        fractions : np.array
            List if fractions equally long as the number of nuclides. 
            E.g. [.5,.5]

        '''
        
        #Get atomic fractions 
        fractions = np.array([fraction for fraction,_ in self._composition])
        
        #Normalize fractions
        fractions /= np.sum(fractions)
        
        return fractions
    
    def get_lambs(self):
        '''
        Get a list if decay constants for all nuclides.

        Returns
        -------
        lambds : np.array
            List if decay constants for all nuclides

        '''
        
        nuclides = self.get_nuclides()
        
        #Get lambdas
        lambds =  np.array([nuclide.get_lamb() for nuclide in nuclides])
        
        return lambds
    
    def get_SF_percents(self):
        '''
        Get a list of SF persentages. I.e. how much in percent of the decay
        that is spontanous fission.

        Returns
        -------
        SF_percents : np.arrat
            list of percentages

        '''
        nuclides = self.get_nuclides()
        
        #Get and return sf percents
        SF_percents = np.array([
            nuclide.get_SF_percent() for nuclide in nuclides
            ])
        
        return SF_percents
        
    
    def get_atomic_numbers(self):
        '''
        Retrun a list of atomic numbers

        Returns
        -------
        atomic_numbers : np.array
            A list of atomic numbers.

        '''
        
        nuclides = self.get_nuclides()
        
        #Get the atomic nubers
        atomic_numbers = np.array([
            nuclide.get_item('a') for nuclide in nuclides
            ])
        
        return atomic_numbers
    
    def get_Ns(self):
        '''
        Get the number densities per nuclide.

        Returns
        -------
        Ns : np.array
            number of atoms per cm3

        '''
        
        
        density = self.density
        
        atomic_numbers = self.get_atomic_numbers()
        fractions = self.get_fractions()
        
        #Calculate atomic densities
        Ns =  density / np.sum(atomic_numbers * fractions) * N_A * fractions
        
        return Ns
    
    def get_SF_rates(self):
        '''
        Get the spontaneous fission rate.

        Returns
        -------
        SF_rates : np.array
            List of SF rates for all nuclides in fission / s.

        '''
        
        Ns = self.get_Ns()
        
        lambs = self.get_lambs()
        
        SF_percents = self.get_SF_percents()     
        
        #Calculate SF rates 
        SF_rates = lambs * SF_percents /100. * Ns
        
        return SF_rates
    
    
    def get_SFR(self):
        '''
        Get the SF rate. 

        Returns
        -------
        SF_rate : float
            SF rate, fission / s / cm3 or fission / cm3 if a volume is set

        '''
        
        #Get the volume
        volume = self.volume
                
        SF_rates = self.get_SF_rates()
        
        #Sum all rates, treat nans as zero
        SF_rate = np.nansum(SF_rates)
        
        #If the volume is set
        if volume: 
            
            #Then get the fission rate as fission / s
            SF_rate *= volume
        
        #Return the SF_rate
        return SF_rate
        
        
class nuclide():
    
    _data = data()
    
    def __init__(self,name):
        '''
        Construct a nuclide-

        Parameters
        ----------
        name : str
            String name of the nuclide, e.g. U235

        Returns
        -------
        None.

        '''
        
        #Name of nuclide
        self.name = name 
        
    def get_hl(self):
        '''
        Get the half life of the nuclide

        Returns
        -------
        hl : float
            half life in seconds

        '''
        
        #get data and name
        data = self._data
        name = self.name
        
        hl = data.get_item(name,'half_life_sec')
        
        return hl
    
    def get_item(self,item):
        '''
        Get item for nuclide from data. 

        Parameters
        ----------
        item : str
            Name of item present in the data. E.g. 'half_life_sec'

        Returns
        -------
        value: float / str
            Returns whatever value that is store for the item.

        '''
        
        #get data and name
        data = self._data
        name = self.name
        
        value =  data.get_item(name, item)
        
        return value
    
    def get_SF_percent(self):
        '''
        Get the percent of the decay that is due to SF

        Returns
        -------
        SF_percent : float
            Percet that is due to SF, returns nan if no SF.

        '''
        
        data = self._data
        name = self.name
        
        SF_percent = data.get_SF_percent(name)
        
        return SF_percent
        
    def get_lamb(self):
        '''
        Get decay constants of nuclide.

        Returns
        -------
        lamb : float
            Decay constant of nuclide.

        '''
        
        #Half life
        hl = self.get_hl()
        
        #Calc lambda
        lamb = np.log(2) / hl
        
        #Return lambda
        return lamb