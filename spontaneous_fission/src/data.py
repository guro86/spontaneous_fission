#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 18:51:02 2022

@author: robertgc
"""

import pandas as pd
import os

class data():
    
    def __init__(self):

        #Relative path to the data
        data_path = os.path.dirname(os.path.abspath(__file__)) \
            + '/../data/decay_data.csv'
        
        #Get data
        self.df = pd.read_csv(data_path)
        
        #Prepare the data
        self._prepare()
        
    def get_SF_percent(self,name):
        
        #Get dictionary with percents
        dic = self.get_decay_percent(name)
        
        #Return percent spontaneous fission
        return dic['SF']
        
    def get_decay_percent(self,name):
        
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
        
        #Data frame 
        df = self.df
        
        #Return the item for the isotope 
        return df.loc[name,item]
    
    def check_name(self,name):
        
        #Data frame 
        df = self.df
        
        #Check if name is in index and return result
        return name in df.index
        
    def _prepare(self):
        
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