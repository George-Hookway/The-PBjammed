# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 10:11:26 2024

@author: GTH025
"""

import pandas as pd
import pickle
import scipy.stats as st

Directory = 'C:/Users/GTH025/Documents/The-PBjammed' # Replace with your own directory
StarList = pd.read_csv(f'{Directory}/Input/StarList.csv', sep=',', comment='#')

# The star number within the list of stars
Star = 2

# Accessing ModeID results

with open(f'{Directory}/Output/ModeIDs/{StarList.ID[Star]} - {StarList.Np[Star]} - '
          f'{StarList.Type[Star]}.pickle', 'rb') as File:
    ModeID = pickle.load(File)
File.close()

# Accessing Peakbagged results

with open(f'{Directory}/Output/Peakbags/{StarList.ID[Star]} - {StarList.Np[Star]} - '
          f'{StarList.Type[Star]}.pickle', 'rb') as File:
    Peakbagged = pickle.load(File)
File.close()

# Applying an uncertainty width test

PriorSTD = ModeID['summary']['dnu'][0]*0.03
Failures = []
for x in Peakbagged['samples']['freq'].T:
    MedianSTD = st.median_abs_deviation(x)
    if MedianSTD < 0.5*PriorSTD:
        Failures.append('Pass')
    else:
        Failures.append('Fail')

# Creating the table of results

Results = pd.DataFrame()

Results.insert(0, 'l', Peakbagged['ell'])
Results.insert(1, 'n', ModeID['enn'])
Results.insert(2, 'freq', Peakbagged['summary']['freq'][0])
Results.insert(3, 'freq_err', Peakbagged['summary']['freq'][1])
Results.insert(4, 'height', Peakbagged['summary']['height'][0])
Results.insert(5, 'height_err', Peakbagged['summary']['height'][1])
Results.insert(6, 'width', Peakbagged['summary']['width'][0])
Results.insert(7, 'width_err', Peakbagged['summary']['width'][1])
Results.insert(8, 'Approval', Failures)

# Removing modes that failed the uncertainty test.

Results.drop(Results[Results['Approval']=='Fail'].index, inplace=True)
Results.reset_index(inplace=True)
Results.drop(columns=['index', 'Approval'], inplace=True)

Results.to_csv(f'{Directory}/Output/{StarList.ID[Star]}.csv', index=False)
