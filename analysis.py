# ToDo: some haphazard analysis to make sure the timestamps line up
import datetime, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from importUtils import nigel_data_to_pd, thomas_data_to_pd
def import_both_same_timesteps():
    nigel_nwp = nigel_data_to_pd()
    print('Nigel nwp: ', nigel_nwp.columns)
    thomas_nwp = thomas_data_to_pd()
    print('Thomas columns: ', thomas_nwp.columns)

    nigel_nwp = nigel_nwp[nigel_nwp['Time (UTC)'] > min(thomas_nwp['Time'])]
    nigel_nwp = nigel_nwp[nigel_nwp['Time (UTC)'] < max(thomas_nwp['Time'])]

    return nigel_nwp, thomas_nwp


def crosscorrelate_and_plot():
    nigel_nwp, thomas_nwp = import_both_same_timesteps()

    all_nwp = pd.merge(thomas_nwp, nigel_nwp, how='inner', left_on='Time', right_on='Time (UTC)')
    thomas_nwp = all_nwp[thomas_nwp.columns]
    nigel_nwp = all_nwp[nigel_nwp.columns]

    coeffs = np.zeros(shape=[len(thomas_nwp.columns), len(nigel_nwp.columns)])

    x=0
    for thomas_variable in thomas_nwp.columns:
        thomas_var_np = thomas_nwp[thomas_variable].to_numpy()

        y=0
        for nigel_variable in nigel_nwp.columns:
            nigel_var_np = nigel_nwp[nigel_variable].to_numpy()

            xcoeff =  np.corrcoef(thomas_var_np, nigel_var_np)
            coeffs[x,y] = xcoeff[0,1]
            y += 1
        x += 1

    max_xs = np.argmax(coeffs, axis=-1)
    for x in range(len(thomas_nwp.columns)):
        thomas_variable = thomas_nwp.columns[x]
        corresponding_nigel_variable  = nigel_nwp.columns[max_xs[x]]


        steps = 5000
        corr = coeffs[x, max_xs[x]]
        print(corr)

        plt.title('corrcoeeff: ' + str(corr))
        plt.plot(nigel_nwp['Time (UTC)'][:steps], nigel_nwp[corresponding_nigel_variable][:steps], label='Nigel: ' + corresponding_nigel_variable )
        plt.plot(thomas_nwp['Time'][:steps], thomas_nwp[thomas_variable][:steps], label='Thomas: ' + thomas_variable)
        plt.legend()
        plt.show()




