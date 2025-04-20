# Amit Kaplan - MMN12
# Q3

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

class HHModel:

    class Gate:
        alpha, beta, state = 0, 0, 0

        def update(self, deltaTms):
            alphaState = self.alpha * (1-self.state)
            betaState = self.beta * self.state
            self.state += deltaTms * (alphaState - betaState)

        def setInfiniteState(self):
            self.state = self.alpha / (self.alpha + self.beta)

    # ENa, EK, EKleak = 115, -12, 10.6
    # gNa, gK, gKleak = 120, 36, 0.3
    # m, n, h = Gate(), Gate(), Gate()
    # Cm = 1

    def __init__(self, ENa, EK, EKleak, gNa=120, gK=36, gKleak=0.3, startingVoltage=0):
        self.ENa, self.EK, self.EKleak = ENa, EK, EKleak
        self.gNa, self.gK, self.gKleak = gNa, gK, gKleak
        self.m, self.n, self.h = self.Gate(), self.Gate(), self.Gate()
        self.Cm = 1
        self.Vm = startingVoltage
        self.UpdateGateTimeConstants(startingVoltage)
        self.m.setInfiniteState()
        self.n.setInfiniteState()
        self.h.setInfiniteState()
        self.INa = 0
        self.IK  = 0
        self.IKleak = 0
        self.Isum = 0

    def UpdateGateTimeConstants(self, Vm):
        self.n.alpha = .01 * ((10-Vm) / (np.exp((10-Vm)/10)-1))
        self.n.beta = .125*np.exp(-Vm/80)
        self.m.alpha = .1*((25-Vm) / (np.exp((25-Vm)/10)-1))
        self.m.beta = 4*np.exp(-Vm/18)
        self.h.alpha = .07*np.exp(-Vm/20)
        self.h.beta = 1/(np.exp((30-Vm)/10)+1)

    def UpdateCellVoltage(self, stimulusCurrent, deltaTms):
        self.INa = np.power(self.m.state, 3) * self.gNa * self.h.state*(self.Vm-self.ENa)
        self.IK = np.power(self.n.state, 4) * self.gK * (self.Vm-self.EK)
        self.IKleak = self.gKleak * (self.Vm-self.EKleak)
        self.Isum = stimulusCurrent - self.INa - self.IK - self.IKleak
        self.Vm += deltaTms * self.Isum / self.Cm

    def UpdateGateStates(self, deltaTms):
        self.n.update(deltaTms)
        self.m.update(deltaTms)
        self.h.update(deltaTms)

    def Iterate(self, stimulusCurrent=0, deltaTms=0.05):
        self.UpdateGateTimeConstants(self.Vm)
        self.UpdateCellVoltage(stimulusCurrent, deltaTms)
        self.UpdateGateStates(deltaTms)


configs = [
    {'ENa': 115, 'EK': -12, 'EKleak': 10.6},
    {'ENa': 90,  'EK': -20, 'EKleak': 10.6},
    {'ENa': 140, 'EK': 5, 'EKleak': 20}
]

# e_na_values = [115, 100, 130]  # mV
# e_k_values = [-12, -20, -5]    # mV
# e_leak_values = [10.6, 0, 20]  # mV
# hh = HHModel()
pointCount = 5000
times = np.arange(pointCount) * 0.05
stim = np.zeros(pointCount)
stim[2000:3000] = 10

n = np.empty(pointCount)
m = np.empty(pointCount)
h = np.empty(pointCount)
INa = np.empty(pointCount)
IK = np.empty(pointCount)
IKleak = np.empty(pointCount)
Isum = np.empty(pointCount)

voltage_curves = []

for cfg in configs:
    hh = HHModel(**cfg)
    Vm = np.empty(pointCount)
    for i in range(pointCount):
        hh.Iterate(stimulusCurrent=stim[i], deltaTms=0.05)
        Vm[i] = hh.Vm - 70
    voltage_curves.append((Vm, cfg))

plt.figure(figsize=(10, 5))
for i, (Vm, cfg) in enumerate(voltage_curves):
    label = f'ENa={cfg["ENa"]}, EK={cfg["EK"]}, Eleak={cfg["EKleak"]}'
    plt.plot(times, Vm, label=label)

plt.plot(times, stim - 70, label='Stimuli (scaled) - step current I=10 ', color='sandybrown', linestyle='--')
plt.ylabel("Membrane Potential (mV)", fontsize=15)
plt.xlabel('Time (msec)', fontsize=15)
plt.xlim([90, 160])
plt.title("HH Model: 3 Curves (V-T) Different Reversal Potentials", fontsize=15)
plt.legend(loc='upper right')
plt.tight_layout()
filename = 'HH_3.0'
plt.savefig(f'{filename}.png')
