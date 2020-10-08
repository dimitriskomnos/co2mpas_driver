import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

############################ USER INPUTS #########################################
path = 'C:/Users/dimit/Desktop/jaime_sims/test_ds_script/'
test_velocities_file_path = 'c:/Users/dimit/Desktop/jaime_sims/test_ds_script/velocities.dat'
plot_vars = True
save_to_dat_file = True
show_header_in_export = False
############################ USER INPUTS #########################################

#df_test_velocities = pd.read_excel(test_velocities_file_path)
test_data = [i.strip().split() for i in open(test_velocities_file_path).readlines()]
test_data = pd.DataFrame(test_data).astype(float)
test_data.columns = ['times', 'velocities']
test_velocities = test_data['velocities'].values
test_times = test_data['times'].values


gs = list(pd.read_excel(path + 'gs.xlsx')['gear_shift_limits'].values)
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
test_times_diff = np.diff(test_times)
test_velocities_diff = np.diff(test_velocities)
test_accelerations = np.append(0, test_velocities_diff / test_times_diff)
test_ds = test_accelerations / test_potential_accelerations

test_data['potential_accelerations'] = test_potential_accelerations
test_data['accelerations'] = test_accelerations
test_data['DS'] = test_ds

filename_to_write = test_velocities_file_path.split('.dat')[0] + '_potential_accelerations'
if not save_to_dat_file:
    test_data.to_excel(filename_to_write+'.xlsx')
else:
    test_data.to_csv(filename_to_write + '.dat', sep=' ', header=show_header_in_export, index=False, )

if plot_vars:
    fig, ax = plt.subplots()
    for i in range(len(discrete_accelerations)):
        ax.plot(discrete_speeds[i], discrete_accelerations[i])
    for i in np.arange(1, len(gs), 1):
        ax.axvline(x=gs[i])
    ax.scatter(test_velocities, test_potential_accelerations)
    plt.show()