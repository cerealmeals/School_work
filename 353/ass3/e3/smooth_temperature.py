import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from scipy import stats
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter

filename1 = sys.argv[1]
cpu_data = pd.read_csv(filename1)

float_time = cpu_data['timestamp'].apply(lambda x: datetime.timestamp(datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f")))
loess_smoothed = lowess(cpu_data['temperature'].values, float_time, frac = 0.05)


kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]

initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([3, 2, 2, 50]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.01, 0.01, 0.05, 0.05]) ** 2 # TODO: shouldn't be zero
transition = [[0.97,0.5,0.2,00.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]] # TODO: shouldn't (all) be zero

kf = KalmanFilter(
    initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition
)

pred_state, state_cov = kf.smooth(kalman_data)

plt.figure(figsize=(12, 4))
plt.xticks(range(0, len(cpu_data['timestamp'].values), 300), rotation=25)
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-', linewidth=2)
plt.plot(cpu_data['timestamp'], pred_state[:, 0], 'g-', linewidth=2)
plt.legend(['Sensor reading', 'LOESS-smoothed', 'Kalman-smoothed'])
plt.xlabel('Time')
plt.ylabel('CPU Temperature')
#plt.show() # maybe easier for testing

plt.savefig('cpu.svg') # for final submission
