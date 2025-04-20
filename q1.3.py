# Amit Kaplan - MMN12
# Q1.C - one spike only

import numpy as np
import matplotlib.pyplot as plt

# Simulation settings
T = 10      # Shortened total time to zoom into first spike
dt = 0.01   # Higher resolution
time = np.arange(0, T + dt, dt)

# Neuron parameters
vRest = -70    # mV
Rm = 1         # kOhm
Cm = 5         # uF
I = 0.2        # mA
vSpike = 50    # mV
tau_m = Rm * 1e3 * Cm * 1e-6  # seconds

# Thresholds to test
thresholds = [20, -10, -50]
colors = ['#FF6B6B', '#4ECDC4', '#556270']

# Create figure
plt.figure(figsize=(10, 6))
plt.title("First Spike Line", fontsize=16, fontweight='bold')

for vTh, color in zip(thresholds, colors):
    Vm = np.ones(len(time)) * vRest * 1e-3
    stim = I * 1e-3 * np.ones(len(time))
    spike_time = None

    for i, t in enumerate(time[:-1]):
        uinf = vRest * 1e-3 + Rm * 1e3 * stim[i]
        Vm[i+1] = uinf + (Vm[i] - uinf) * np.exp(-dt * 1e-3 / tau_m)
        if Vm[i] >= vTh * 1e-3:
            Vm[i+1] = vSpike * 1e-3
            spike_time = t
            Vm[i+2:] = vRest * 1e-3  # Cut the signal after the spike
            break

    plt.plot(time, Vm * 1e3, label=f"Threshold = {vTh} mV", color=color, linewidth=2)
    if spike_time:
        plt.axvline(x=spike_time, color=color, linestyle='--', alpha=0.7)
        plt.text(spike_time + 0.05, vSpike + 2, f"{spike_time:.2f} ms", color=color, fontsize=10)

plt.axhline(y=vRest, color='gray', linestyle=':', label="Resting potential")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Potential V(t) [mV]")
plt.xlim([0, 4])  # Limit to first 4 ms
plt.grid(True, linestyle=':')
plt.legend()
plt.tight_layout()
plt.savefig("First_Spikes_Only_Annotated.png")
