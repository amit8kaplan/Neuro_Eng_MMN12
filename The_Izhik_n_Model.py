# Amit Kaplan - MMN12
# Q2

import numpy as np
import matplotlib.pyplot as plt

x  = 5
y  = 140

titles = ['Regular Spiking', 'Intrinsically Bursting', 'Chattering', 'Fast spiking',
          'Low Threshold Spiking', 'TC - Tonic Firing', 'TC - Rebound Burst',
          'Resonator - Appropriate Frequency', 'Resonator - Inappropriate Frequency']
a  = [0.02, 0.02, 0.02, 0.1, 0.02, 0.02, 0.02, 0.1, 0.1]
b  = [0.2, 0.2, 0.2, 0.2, 0.25, 0.25, 0.25, 0.26, 0.26]
c  = [-65, -55, -50, -65, -65, -65, -65, -65, -65]
d  = [8, 4, 2, 2, 2, 0.05, 0.05, 2, 2]

v0s = [-70, -70, -70, -70, -70, -60, -90, -70, -70]
# v0 = -70         # Resting potential        [mV]
T       = 200    # Simulation time          [mSec]
dt      = 0.1  # Simulation time interval [mSec]

time    = np.arange(0, T + dt, dt)  # Time array

DefulatStim = np.zeros(len(time))
for i,t in enumerate(DefulatStim):
    if i > 20:
        DefulatStim[i] = 10

for exp in range(len(a)):
    trace = np.zeros((2, len(time)))  # Tracing du and dv

    if titles[exp] == 'TC - Rebound Burst':
        tempStim = np.zeros(len(time))
        tempStim[int(0 / dt):int(40 / dt)] = -20
        tempStim[int(40 / dt):] = 0
        stimLabel = "I(t): -20→0"
    elif titles[exp] == 'Resonator - Appropriate Frequency':
        tempStim = np.ones(len(time)) * -0.65
        # pulse_times = [70, 95, 120, 145, 170]
        pulse_times = [50, 100, 150]
        for pt in pulse_times:
            pulse_start = int(pt / dt)
            pulse_end = int((pt + 1) / dt)
            tempStim[pulse_start:pulse_end] = 6
        stimLabel = "I(t): pulses of 6 at 25ms intervals, Rest at -0.65"
    elif titles[exp] == 'Resonator - Inappropriate Frequency':
        tempStim = np.ones(len(time)) * -0.65
        # pulse_times = [15,30,45,60,75, 90, 105, 120, 135]
        pulse_times = np.arange(45, 155, 10)
        # pulse_times = [20, 22.5, 25, 27.5, 30, 32.5, 35, 37.5, 40]
        for pt in pulse_times:
            pulse_start = int(pt / dt)
            pulse_end = int((pt + 1) / dt)
            tempStim[pulse_start:pulse_end] = 10
        stimLabel = "I(t): pulses of 10 at 10ms intervals, Rest at -0.65"
    else:
        tempStim = np.zeros(len(time))
        tempStim = DefulatStim
        stimLabel = "I(t) = 10"
    v  = v0s[exp]
    u  = b[exp]*v
    spikes = []
    for i, j in enumerate(tempStim):
        v += dt * (0.04*v**2 + x*v + y - u + tempStim[i])
        u += dt * a[exp]*(b[exp]*v-u)
        if v > 30:
            trace[0,i] = 30
            v = c[exp]
            u += d[exp]
        else:
            trace[0,i] = v
            trace[1,i] = u

    param_label = f'a={a[exp]}, b={b[exp]}, c={c[exp]}, d={d[exp]}, {stimLabel}'

    plt.figure(figsize=(10,5))
    plt.title('Izhikevich Model: {}'.format(titles[exp]), fontsize=15)
    plt.ylabel('Membrane Potential (mV)', fontsize=15)
    plt.xlabel('Time (msec)', fontsize=15)
    plt.plot(time, trace[0], linewidth=2, label = 'Vm')
    plt.plot(time, trace[1], linewidth=2, label = 'Recovery', color='green')
    plt.plot(time, tempStim + v0s[exp], label='Stimuli (Scaled) I(t)', color='sandybrown', linewidth=2)
    plt.legend(loc=1)
    plt.figtext(0.5, -0.05, param_label, wrap=True, ha='center', fontsize=11)

    filename = f'izhikevich_mmn12_15.0_{titles[exp].replace(" ", "_").lower()}.png'
    plt.savefig(f"{filename}",  bbox_inches='tight')
