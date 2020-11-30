# ToDo: some haphazard analysis to make sure the timestamps line up
import datetime, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from importUtils import nigel_data_to_pd, thomas_data_to_pd

def somerandomanalysis(crop=True):
    nigel_nwp = nigel_data_to_pd()
    print('Nigel nwp: ', nigel_nwp.columns)
    thomas_nwp = thomas_data_to_pd()
    print('Thomas columns: ', thomas_nwp.columns)

    if crop:
        nigel_nwp = nigel_nwp[nigel_nwp['Time (UTC)'] > min(thomas_nwp['Time'])]
        nigel_nwp = nigel_nwp[nigel_nwp['Time (UTC)'] < max(thomas_nwp['Time'])]

    steps = 5000

    plt.title('ShortWaveDown')
    plt.plot(nigel_nwp['Time (UTC)'][:steps], nigel_nwp['Short_Wave_Flux_Down [W/m2]'][:steps], label='Nigel')
    plt.plot(thomas_nwp['Time'][:steps], thomas_nwp['SWDOWN'][:steps], label='Thomas')
    plt.legend()
    plt.show()

    plt.title('Temp')
    plt.plot(nigel_nwp['Time (UTC)'][:steps], nigel_nwp['Temperature [K]'][:steps], label='Nigel')
    plt.plot(thomas_nwp['Time'][:steps], thomas_nwp['T2'][:steps], label='Thomas')
    plt.legend()
    plt.show()

    plt.title('Rain(1?)')
    plt.plot(nigel_nwp['Time (UTC)'][:steps], nigel_nwp['Precipitation [mm]'][:steps], label='Nigel')
    plt.plot(thomas_nwp['Time'][:steps], thomas_nwp['RAINC'][:steps], label='Thomas')
    plt.legend()
    plt.show()

    plt.title('Rain(2?)')
    plt.plot(nigel_nwp['Time (UTC)'][:steps], nigel_nwp['Precipitation [mm]'][:steps], label='Nigel')
    plt.plot(thomas_nwp['Time'][:steps], thomas_nwp['RAINNC'][:steps], label='Thomas')
    plt.legend()
    plt.show()

