# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 13:08:55 2024

@author: gth025
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Connor Adam code.
def fft(Data):
    Data = np.array(Data)
    data = Data[1]    # Power
    Frequency = Data[0]
    Mean = np.mean(data)
    N = len(Frequency)
    Delta_t = Frequency[1] - Frequency[0]
    data_ft = np.abs(np.fft.fft(data-Mean))**2
    freq = np.abs(np.fft.fftfreq(N, Delta_t))    # freq being the frequency of the frequency (time).

    return freq, data_ft, Delta_t

Data = pd.read_csv('G:/george/Sinister Six/rafas_stars/ktwo003241581_01_kasoc-psd_slc_v1.dat',
                   sep=' ', comment='#', names=['Time', 'Flux'])

Transformed = fft([Data.Time*24*3600, Data.Flux])

plt.figure()
plt.plot(Transformed[0]*10**6, Transformed[1])
plt.show()
