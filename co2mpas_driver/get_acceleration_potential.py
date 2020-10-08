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
    fig, ax = plt.subplots(ncols=2)
    for i in range(len(discrete_accelerations)):
        ax[0].plot(discrete_speeds[i], discrete_accelerations[i])
    for i in np.arange(1, len(gs), 1):
        ax[0].axvline(x=gs[i])
    ax[0].scatter(test_velocities, test_potential_accelerations)
    ax[0].set_ylabel('Acceleration [m/s^2]')
    ax[0].set_xlabel('Speed [m/s]')

    ax[1].plot(test_data['times'].values,
               test_data['accelerations'].values, 'r--', label='accelerations')
    ax[1].set_ylabel('Acceleration [m/s^2]', color='r')
    ax[1].set_xlabel('Time [s]')
    ax2 = ax[1].twinx()
    ds_median = round(np.median(test_data['DS'].values), 2)
    ax2.plot(test_data['times'].values,
             test_data['DS'].values, 'g-', label='DS\nmedian: %s'%(ds_median))
    ax2.set_ylabel('DS [-]', color='g')
    ax[1].legend(loc=2); ax2.legend(loc=1)

    plt.tight_layout()
    plt.show()