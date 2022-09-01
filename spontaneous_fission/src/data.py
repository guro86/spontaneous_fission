#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 18:51:02 2022

@author: robertgc
"""

import pandas as pd
import os
import numpy as np

class data():
    
    def __init__(self):
        '''
        Constructs the data object.

        Returns
        -------
        None.

        '''

        #Relative path to the data
        data_path = os.path.dirname(os.path.abspath(__file__)) \
            + '/../data/decay_data.csv'
        
        #Get data
        self.df = pd.read_csv(
            data_path,
            na_values=[' ','']
            )
        
        #Prepare the data
        self._prepare()
        
    def get_SF_percent(self,name):
        '''
        Get the SF percent for a material with name.

        Parameters
        ----------
        name : str
            name, e.g. U235

        Returns
        -------
        SF_percet : float
            The percent that is due to SF, nan if no SF.

        '''
        
        #Get dictionary with percents
        dic = self.get_decay_percent(name)
        
        #If sponatenous fission
        if 'SF' in dic:
            #Return percent spontaneous fission
            return dic['SF']
        
        else:
            #Return nan
            return np.nan
        
    def get_decay_percent(self,name):
        '''
        Get a dictionary with decay percents.

        Parameters
        ----------
        name : str
            name of nuclide, e.g. U235

        Returns
        -------
        dic : dictionary
            dict with percents, e.g. {'SF':100} 

        '''
        
        #The data frame 
        df = self.df
        
        #Get labels and decay percent for name
        labels = df.filter(regex = '^decay_\d$').loc[name].values
        decay_percents = df.filter(regex = '^decay_\d_%$').loc[name].values
        
        #Generate dictionary with labels and percents
        dic = {
            label:decay_percent for label,decay_percent \
                in zip(labels,decay_percents)
            }
        
        #return dict
        return dic
        
    def get_item(self,name,item):
        '''
        Get any item stored in the data for the nuclide.

        Parameters
        ----------
        name : str
            name of nuclide, e.g. U235
        item : str
            item description, e.g. half_life_s

        Returns
        -------
        value : float / str
            Returns whatever value stored.

        '''
        
        #Data frame 
        df = self.df
        
        #Return the item for the isotope 
        return df.loc[name,item]
    
    def check_name(self,name):
        '''
        Check if nuclide is present in the data.

        Parameters
        ----------
        name : str
            name of nuclide, i.e. U235

        Returns
        -------
        isin : bool
            True if present, False if not

        '''
        
        #Data frame 
        df = self.df
        
        #Check if name is in index and return result
        isin = name in df.index
        
        return isin
        
    def _prepare(self):
        '''
        Internal method that prepares the data for reading.

        Returns
        -------
        None.

        '''
        
        #Get the data frame
        df = self.df
        
        #Calculate and store a
        df['a'] = df[['z','n']].sum(axis=1)
        
        #Set the name needed 
        df['name'] = \
            df[['symbol','a']].apply(
                lambda x: '{}{}'.format(*x),axis=1
                ).str.upper()
        
        #Use the name as index    
        df.set_index('name',inplace=True)
          
        #Narrow down dataframe to only spontanous fission isotopes 
        df = df[df.filter(regex='decay_\d$').isin(['SF']).any(axis=1)]
        

if __name__ == '__main__':
    
    dobj = data()
    item = dobj.get_item('U235','half_life')
    print('half-life for U-235')
    print(item)
    
    print('decay percents for U-235')
    decay = dobj.get_decay_percent('U235')
    print(decay)
    
    print('spontaneous fission rate percent for U235')
    sf_percent = dobj.get_SF_percent('U235')
    print(sf_percent)