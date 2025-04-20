# Amit Kaplan - MMN12
# Q1.A

import numpy as np
import matplotlib.pyplot as plt
custom_colors = ['#FF6B6B', '#4ECDC4', '#556270']  # Custom color palette

# Constants
T = 100     # Simulation time [mSec]
dt = 0.1    # Time interval [mSec]
vRest = -70 # Resting potential [mV]
Rm = 1      # Membrane Resistance [kOhm]
Cm = 5      # Capacitance [uF]
tau_ref = 1 # Refractory period [mSec]
vTh = -40   # Spike threshold [mV]
vSpike = 50 # Spike voltage [mV]

# Currents to test
currents = np.linspace(0.1, 1.0, 20)  # 20 current values from 0.1 mA to 1.0 mA

# Tau values to compare (in milliseconds)
tau_values = [5, 50, 100]

# Time array
time = np.arange(0, T + dt, dt)

# Create figure
plt.figure(figsize=(10, 6))

# For each tau, simulate and calculate firing rate vs input current
for tau_m_ms, color in zip(tau_values, custom_colors):
    firing_rates = []

    for I in currents:
        tau_m = tau_m_ms * 1e-3  # Convert tau to seconds
        stim = I * 1e-3 * np.ones(len(time))  # Constant current stimulation
        Vm = np.ones(len(time)) * vRest * 1e-3
        spikes = []
        t_init = 0

        for i, t in enumerate(time[:-1]):
            if t >= t_init:
                uinf = vRest * 1e-3 + Rm * 1e3 * stim[i]
                Vm[i+1] = uinf + (Vm[i] - uinf) * np.exp(-dt * 1e-3 / tau_m)
                if Vm[i] >= vTh * 1e-3:
                    spikes.append(t)
                    Vm[i] = vSpike * 1e-3
                    t_init = t + tau_ref

        firing_rate = len(spikes) / (T / 1000)  # Hz
        firing_rates.append(firing_rate)

    plt.plot(currents, firing_rates, marker='D', linestyle='--', linewidth=2.5,
             color=color, label=f'τ = {tau_m_ms} ms')

plt.title('I–F Curves', fontsize=17, fontweight='bold')
plt.xlabel('Input Current (mA)', fontsize=14)
plt.ylabel('Firing Rate (Hz)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle=':', linewidth=0.7)
plt.legend(loc='upper left', fontsize=12)
plt.ylim(0, 1000)
plt.tight_layout()

plt.savefig("I_F_Curves1.png")
