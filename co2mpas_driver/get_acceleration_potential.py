import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

############################ USER INPUTS #########################################
path = 'C:/Users/dimit/Desktop/'
test_velocities_file_path = 'C:/Users/dimit/Desktop/velocities.xlsx'
plot_vars = True
############################ USER INPUTS #########################################

df_test_velocities = pd.read_excel(test_velocities_file_path)
test_velocities = df_test_velocities['velocities'].values


gs = list(pd.read_excel(path + 'gs.xlsx').values)
gs = [0.] + gs
discrete_acceleration_curves = pd.read_excel(path + 'discrete_acceleration_curves.xlsx')

vels = discrete_acceleration_curves['velocities'].values
accs = discrete_acceleration_curves['accelerations'].values
discrete_speeds = [eval(v) for v in vels]
discrete_accelerations = [eval(a) for a in accs]

curves = [interp1d(discrete_speeds[i], discrete_accelerations[i]) for i in range(len(discrete_speeds))]

def get_acceleration_potential(vel, gs, curves):
    b = list(gs > vel)
    if True in b:
        index = b.index(True) - 1
    else:
        index = -1
    return curves[index](vel)

test_potential_accelerations = [get_acceleration_potential(vel, gs, curves) for vel in test_velocities]
filename_to_write = test_velocities_file_path.split('.xlsx')[0] + '_potential_accelerations.xlsx'
df_test_velocities['potential_accelerations'] = test_potential_accelerations
df_test_velocities.to_excel(filename_to_write)

if plot_vars:
    fig, ax = plt.subplots()
    for i in range(len(discrete_accelerations)):
        ax.plot(discrete_speeds[i], discrete_accelerations[i])
    for i in np.arange(1, len(gs), 1):
        ax.axvline(x=gs[i])
    ax.scatter(test_velocities, test_potential_accelerations)
    plt.show()