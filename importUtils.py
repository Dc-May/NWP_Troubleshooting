import datetime, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Reads thomas NWP format, crops it accordingly and aggregates into one dataframe
def thomas_data_to_pd(data_folder_name="ThomasNWP"):
    folder_path = os.path.join(os.getcwd(), data_folder_name)
    nwp_csvs = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('csv')]

    full_nwp_pd = None
    for file in nwp_csvs:
        buffer = pd.read_csv(file)
        # time to timestamp, inelegant but more readable
        buffer['Time'] = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in buffer['Time'].to_list()]
        buffer['Time'] = [datetime.datetime.timestamp(date) for date in buffer['Time'].to_list()]

        # here we concat conditionally to build the full NWP
        # basically always discarding the first 6 hours of spinup
        if full_nwp_pd is None:
            full_nwp_pd = buffer[buffer['Time'] > min(buffer['Time']) + 6*60*60]
        else:
            max_time = max(full_nwp_pd['Time'])
            buffer = buffer[buffer['Time'] > max_time]

            # merge might be smarter here?
            full_nwp_pd = pd.concat([full_nwp_pd, buffer], join='outer', ignore_index=True)

    return full_nwp_pd

def nigel_data_to_pd(data_folder_name='NWP_data/Edmonton'):
    default_house = 'egauge18369'
    folder_path = os.path.join(os.getcwd(), data_folder_name)
    if default_house not in os.listdir(folder_path):
        print('cannot find the default house (', default_house, ') in the specified folder')
    else:
        folder_path = os.path.join(folder_path, default_house)
        if default_house + '.csv' not in os.listdir(folder_path):
            print('didnt find the csv file, pls check naming convention')
        else:
            file = os.path.join(folder_path, default_house + '.csv')

            nwp_pd = pd.read_csv(file)
            nwp_pd['Time (UTC)'] = [datetime.datetime.strptime(date, "%Y-%m-%d %H:%M") for date in
                              nwp_pd['Time (UTC)'].to_list()]
            nwp_pd['Time (UTC)'] = [datetime.datetime.timestamp(date) for date in nwp_pd['Time (UTC)'].to_list()]

            return nwp_pd

