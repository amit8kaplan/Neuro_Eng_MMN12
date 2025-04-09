import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

T       = 50    # Simulation time          [mSec]
dt      = 0.1   # Simulation time interval [mSec]
t_init  = 0     # Stimulus init time       [V]
vRest   = -70   # Resting potential        [mV]
Rm      = 1     # Membrane Resistance      [kOhm]
Cm      = 5     # Capacitance              [uF]
tau_ref = 1     # Repreactory Period       [mSec]
vTh     = -40   # Spike threshond          [mV]
I       = 0.2   # Current stimulus         [mA]
vSpike  = 50    # Spike voltage            [mV]

time    = np.arange(0, T*1e-3 + dt*1e-3, dt*1e-3)  # Time array
Vm      = np.ones(len(time))*vRest*1e-3            # Membrane voltage array
tau_m   = Rm*1e3 * Cm*1e-6                         # Time constant
spikes  = []                                       # Spikes timings

stim = I*1e-3 * signal.windows.triang(len(time)) # Triangular stimulation pattern

for i, t in enumerate(time[:-1]):
    if t > t_init:
        uinf = vRest*1e-3 + Rm*1e3 * stim[i]
        Vm[i+1] = uinf + (Vm[i]-uinf)*np.exp(-dt*1e-3/tau_m)
        if Vm[i] >= vTh*1e-3:
            spikes.append(t*1e3)
            Vm[i]=vSpike*1e-3
            t_init = t + tau_ref*1e-3


plt.figure(figsize=(10,5))
plt.title('Leaky Integrate-and-Fire Model', fontsize=15)
plt.ylabel('Membrane Potential (mV)', fontsize=15)
plt.xlabel('Time (msec)', fontsize=15)
plt.plot(time*1e3, Vm*1e3, linewidth=5, label = 'Vm')
plt.plot(time*1e3, 100/max(stim)*stim, label = 'Stimuli (Scaled)', color='sandybrown', linewidth=2)
plt.ylim([-75,100])
plt.axvline(x=spikes[0], c='red', label = 'Spike')
for s in spikes[1:]:
    plt.axvline(x=s, c='red')
plt.axhline(y=vTh, c='black', label = 'Threshold', linestyle='--')
plt.legend()
plt.savefig('leaky_integrate_and_fire_plot.png')  # Save as PNG
