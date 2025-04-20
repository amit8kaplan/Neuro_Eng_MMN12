# Amit Kaplan - MMN12
# Q1.B

import numpy as np
import matplotlib.pyplot as plt

# Simulation settings
T = 50      # Total time [ms]
dt = 0.1    # Time step [ms]
time = np.arange(0, T + dt, dt)  # Time array

# Fixed neuron parameters
vRest = -70    # Resting potential [mV]
Rm = 1         # Resistance [kOhm]
Cm = 5         # Capacitance [uF]
tau_ref = 1    # Refractory period [ms]
I = 0.2        # Input current [mA]
vSpike = 50    # Spike voltage [mV]
tau_m = Rm * 1e3 * Cm * 1e-6  # Time constant

# Thresholds to test
thresholds = [20, -10, -50]
colors = ['#FF6B6B', '#4ECDC4', '#556270']

plt.figure(figsize=(10, 6))
plt.title("V–T Curves",fontsize=17, fontweight='bold')

for vTh, color in zip(thresholds, colors):
    Vm = np.ones(len(time)) * vRest * 1e-3  # Initialize membrane voltage in Volts
    spikes = []
    t_init = 0
    stim = I * 1e-3 * np.ones(len(time))  # Step current

    for i, t in enumerate(time[:-1]):
        if t >= t_init:
            uinf = vRest * 1e-3 + Rm * 1e3 * stim[i]
            Vm[i+1] = uinf + (Vm[i] - uinf) * np.exp(-dt * 1e-3 / tau_m)
            if Vm[i] >= vTh * 1e-3:
                spikes.append(t)
                Vm[i] = vSpike * 1e-3
                t_init = t + tau_ref

    plt.plot(time, Vm * 1e3, label=f"Threshold = {vTh} mV", color=color, linewidth=2)

plt.axhline(y=vRest, color='gray', linestyle=':', label="Resting potential")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential V(t) [mV]")
plt.grid(True, linestyle=':')
plt.legend()
plt.tight_layout()
plt.savefig("V_T_Curves_Different_Thresholds.png")
