#!/usr/bin/env python3
"""Generate Day 4 diagrams for signal integrity notes."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.expanduser('~/.openclaw/workspace/hardware-study-plan/assets')

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f'  {path}')

# ============================================================
# 04-eye-diagram.png — Eye diagram explanation
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Eye Diagram — Signal Quality at a Glance', fontsize=14, fontweight='bold')

# (a) Clean eye
ax = axes[0, 0]
np.random.seed(42)
n_bits = 500
T = 1.0
bits = np.random.choice([0, 1], n_bits)
t_bit = np.linspace(0, 1, 50)
# Clean: rise/fall = 0.1T
tr = 0.1
for b in bits:
    t = np.linspace(0, T, 100)
    y = np.zeros_like(t)
    for j, ti in enumerate(t):
        if ti < tr:
            y[j] = b * ti / tr + (1 - b) * (1 - ti / tr)
        elif ti > T - tr:
            y[j] = b * (1 - (ti - (T - tr)) / tr) + (1 - b) * ((ti - (T - tr)) / tr)
        else:
            y[j] = b
    t_offset = t_bit[np.random.randint(0, 45)]
    ax.plot(t + t_offset, y + 0.05 * np.random.randn(len(t)), 'b-', alpha=0.15, lw=0.5)
ax.set_title('(a) Clean Eye — wide open, thin eyelids', fontsize=11)
ax.set_xlabel('Time (UI)')
ax.set_ylabel('Voltage')
ax.set_ylim(-0.3, 1.5)
ax.grid(True, alpha=0.3)

# (b) Eye with jitter
ax = axes[0, 1]
for b in bits:
    t = np.linspace(0, T, 100)
    y = np.zeros_like(t)
    for j, ti in enumerate(t):
        if ti < tr:
            y[j] = b * ti / tr + (1 - b) * (1 - ti / tr)
        elif ti > T - tr:
            y[j] = b * (1 - (ti - (T - tr)) / tr) + (1 - b) * ((ti - (T - tr)) / tr)
        else:
            y[j] = b
    t_offset = t_bit[np.random.randint(0, 45)] + 0.15 * np.random.randn()
    ax.plot(t + t_offset, y + 0.05 * np.random.randn(len(t)), 'r-', alpha=0.12, lw=0.5)
ax.set_title('(b) Jitter — crossing point blurred', fontsize=11)
ax.set_xlabel('Time (UI)')
ax.set_ylabel('Voltage')
ax.set_ylim(-0.3, 1.5)
ax.grid(True, alpha=0.3)

# (c) Eye with noise
ax = axes[1, 0]
for b in bits:
    t = np.linspace(0, T, 100)
    y = np.zeros_like(t)
    for j, ti in enumerate(t):
        if ti < tr:
            y[j] = b * ti / tr + (1 - b) * (1 - ti / tr)
        elif ti > T - tr:
            y[j] = b * (1 - (ti - (T - tr)) / tr) + (1 - b) * ((ti - (T - tr)) / tr)
        else:
            y[j] = b
    t_offset = t_bit[np.random.randint(0, 45)]
    ax.plot(t + t_offset, y + 0.12 * np.random.randn(len(t)), 'orange', alpha=0.12, lw=0.5)
ax.set_title('(c) Noise — eyelids thickened', fontsize=11)
ax.set_xlabel('Time (UI)')
ax.set_ylabel('Voltage')
ax.set_ylim(-0.3, 1.5)
ax.grid(True, alpha=0.3)

# (d) Annotated eye diagram
ax = axes[1, 1]
t = np.linspace(0, T, 100)
for b in bits[:100]:
    y = np.zeros_like(t)
    for j, ti in enumerate(t):
        if ti < tr:
            y[j] = b * ti / tr + (1 - b) * (1 - ti / tr)
        elif ti > T - tr:
            y[j] = b * (1 - (ti - (T - tr)) / tr) + (1 - b) * ((ti - (T - tr)) / tr)
        else:
            y[j] = b
    t_offset = t_bit[np.random.randint(0, 45)]
    ax.plot(t + t_offset, y + 0.04 * np.random.randn(len(t)), 'b-', alpha=0.2, lw=0.5)

# Annotations
ax.annotate('Eye Height\n(vertical opening)', xy=(0.5, 0.92), fontsize=9, ha='center',
            bbox=dict(boxstyle='round', fc='lightgreen', alpha=0.7))
ax.annotate('Eye Width\n(timing margin)', xy=(0.5, 0.5), fontsize=9, ha='center',
            bbox=dict(boxstyle='round', fc='lightblue', alpha=0.7))
ax.annotate('Rise Time\n(10%-90%)', xy=(0.07, 0.5), fontsize=8, ha='center',
            bbox=dict(boxstyle='round', fc='yellow', alpha=0.6))
ax.annotate('Overshoot', xy=(0.85, 1.15), fontsize=8, ha='center',
            bbox=dict(boxstyle='round', fc='salmon', alpha=0.6))
ax.annotate('Crossing\nPoint', xy=(0.5, 0.45), fontsize=8, ha='center',
            bbox=dict(boxstyle='round', fc='plum', alpha=0.6))
ax.set_title('(d) Key Eye Diagram Parameters', fontsize=11)
ax.set_xlabel('Time (UI)')
ax.set_ylabel('Voltage')
ax.set_ylim(-0.3, 1.5)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save(fig, '04-eye-diagram.png')

# ============================================================
# 04-crosstalk-mechanism.png — Capacitive + Inductive coupling
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Crosstalk Mechanisms', fontsize=14, fontweight='bold')

# (a) Capacitive coupling
ax = axes[0]
x = np.linspace(0, 10, 100)
# Aggressor signal
ax.plot(x, 2 + 0.5 * (x > 2) * (1 - np.exp(-(x-2)*2)), 'r-', lw=2.5, label='Aggressor')
# Victim (far-end)
ax.plot(x, 0.8 + 0.08 * (x > 2.5) * np.exp(-(x-2.5)*3) * np.sin((x-2.5)*8), 'b-', lw=2, label='Victim (FEXT)')
ax.axhline(y=1.5, xmin=0.1, xmax=0.5, color='gray', linestyle='--', alpha=0.5)
ax.axhline(y=0.5, xmin=0.1, xmax=0.5, color='gray', linestyle='--', alpha=0.5)

# Draw parallel lines symbol
for yi in [2.5, 0.2]:
    ax.plot([1, 2], [yi, yi], 'k-', lw=3)
ax.plot([1, 2], [2.0, 1.2], 'k-', lw=3)
# Capacitor symbol
ax.plot([1.5, 1.5], [2.0, 1.2], 'k-', lw=2)
ax.plot([1.3, 1.7], [1.65, 1.65], 'k-', lw=1.5)
ax.plot([1.3, 1.7], [1.55, 1.55], 'k-', lw=1.5)
ax.text(2.7, 1.65, '$C_m$', fontsize=12, color='purple')
ax.text(4, 2.3, 'Aggressor dv/dt', fontsize=9, color='red')
ax.text(4, 0.7, 'Coupled noise pulse', fontsize=9, color='blue')
ax.set_title('(a) Capacitive Coupling', fontsize=12)
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.set_ylim(-0.2, 3.0)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# (b) Inductive coupling
ax = axes[1]
# Aggressor current pulse
t2 = np.linspace(0, 10, 100)
i_agg = (t2 > 2) * (1 - np.exp(-(t2-2)*3)) * 2
ax.plot(t2, 2 + i_agg, 'r-', lw=2.5, label='Aggressor current')
# Victim induced
v_ind = -0.3 * np.gradient(i_agg) * 2
ax.plot(t2, 0.8 + v_ind, 'b-', lw=2, label='Victim (inductive)')

# Draw coupled inductors
for yi in [2.8, 0.2]:
    ax.plot([1, 2], [yi, yi], 'k-', lw=3)
# Coils
theta = np.linspace(0, 3*np.pi, 30)
ax.plot(1.5 + 0.2*np.sin(theta), 2.4 + 0.1*np.cos(theta), 'k-', lw=1.5)
ax.plot(1.5 + 0.2*np.sin(theta), 0.5 + 0.15*np.cos(theta), 'k-', lw=1.5)
ax.text(2.7, 1.7, '$L_m$', fontsize=12, color='purple')
ax.text(5, 2.5, 'Aggressor di/dt', fontsize=9, color='red')
ax.text(2.5, 1.0, 'Induced voltage\nspike', fontsize=9, color='blue')
ax.set_title('(b) Inductive Coupling', fontsize=12)
ax.set_xlabel('Time')
ax.set_ylabel('Voltage / Current')
ax.set_ylim(-0.2, 3.2)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save(fig, '04-crosstalk-mechanism.png')

# ============================================================
# 04-next-vs-fext.png — Near-end vs Far-end crosstalk
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('NEXT vs FEXT — Near-End and Far-End Crosstalk', fontsize=14, fontweight='bold')

# Top: Geometry
ax = axes[0, 0]
t_lines = np.linspace(0, 10, 100)
# Aggressor line
ax.plot(t_lines, np.ones_like(t_lines) * 2, 'r-', lw=3, label='Aggressor')
# Victim line
ax.plot(t_lines, np.ones_like(t_lines) * 1, 'b-', lw=3, label='Victim')
# Driver
ax.plot(-0.5, 2, 'rs', markersize=10)
ax.text(-0.8, 2, 'Driver', fontsize=8, ha='right')
# Near end
ax.plot(0, 1, 'b^', markersize=10)
ax.text(0, 0.5, 'Near End\n(NEXT)', fontsize=7, ha='center')
# Far end
ax.plot(10, 1, 'bv', markersize=10)
ax.text(10, 0.5, 'Far End\n(FEXT)', fontsize=7, ha='center')
# Termination
ax.plot(10.5, 2, 'rD', markersize=8)
ax.text(10.8, 2, 'Term.', fontsize=8)
# Coupling arrows
for x_pos in [3, 5, 7]:
    ax.annotate('', xy=(x_pos, 1.15), xytext=(x_pos, 1.85),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1))
ax.text(5, 2.3, 'EM Coupling', fontsize=9, ha='center', color='purple')
ax.set_xlim(-1.5, 11.5)
ax.set_ylim(0, 3)
ax.set_title('(a) Coupled Line Geometry', fontsize=11)
ax.legend(fontsize=8, loc='upper right')
ax.axis('off')

# NEXT waveform
ax = axes[0, 1]
t = np.linspace(0, 10, 200)
next_pulse = -0.4 * (t > 1) * np.exp(-(t-1)*1.5) + 0.4 * (t > 1.5) * np.exp(-(t-1.5)*2)
ax.plot(t, next_pulse, 'b-', lw=2)
ax.fill_between(t, next_pulse, 0, where=(next_pulse > 0), color='blue', alpha=0.2)
ax.fill_between(t, next_pulse, 0, where=(next_pulse < 0), color='red', alpha=0.2)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_title('(b) NEXT — broad pulse at near end', fontsize=11)
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.grid(True, alpha=0.3)

# FEXT waveform (microstrip — non-zero)
ax = axes[1, 0]
fext_pulse = -0.25 * np.exp(-(t-2.5)**2/0.1) + 0.25 * np.exp(-(t-2.8)**2/0.1)
ax.plot(t, fext_pulse, 'orange', lw=2, label='Microstrip')
# FEXT (stripline — zero)
ax.axhline(y=0, color='green', linestyle='-', lw=2, label='Stripline (ideal)')
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_title('(c) FEXT — narrow spike (microstrip)', fontsize=11)
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# FEXT vs trace length
ax = axes[1, 1]
lengths = np.array([1, 2, 3, 5, 8, 12, 18, 25])
next_amp = 1 - np.exp(-lengths/6)  # NEXT saturates
fext_amp = 0.6 * lengths / 10  # FEXT grows linearly
ax.plot(lengths, next_amp, 'b-o', lw=2, label='NEXT')
ax.plot(lengths, fext_amp, 'r-s', lw=2, label='FEXT (microstrip)')
ax.axhline(y=0, color='green', linestyle='--', lw=1.5, label='FEXT (stripline)')
ax.set_title('(d) NEXT saturates, FEXT grows with length', fontsize=11)
ax.set_xlabel('Coupled Length (cm)')
ax.set_ylabel('Normalized Crosstalk Amplitude')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save(fig, '04-next-vs-fext.png')

# ============================================================
# 04-via-model.png — Via parasitic model
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Via Parasitic Effects', fontsize=14, fontweight='bold')

# (a) Via cross-section
ax = axes[0]
# PCB layers
layers = ['L1-Top', 'L2-GND', 'L3-Sig', 'L4-PWR', 'L5-GND', 'L6-Bot']
for i, name in enumerate(layers):
    y = 5.5 - i
    ax.fill_between([0, 6], y-0.3, y+0.3, color='tan' if i%2==0 else 'sandybrown', alpha=0.5)
    ax.text(3, y, name, ha='center', va='center', fontsize=8)
# Via barrel
ax.plot([3, 3], [0.3, 5.7], 'silver', lw=8, alpha=0.7)
ax.plot([3, 3], [0.3, 5.7], 'k-', lw=1)
# Pads
for y in [0.5, 5.5]:
    ax.plot([3], [y], 'gold', marker='o', markersize=12, markeredgecolor='k', markeredgewidth=1)
# Stub (unused portion)
ax.fill_between([2.6, 3.4], 0.3, 1.5, color='red', alpha=0.3)
ax.text(4.2, 0.9, 'Stub\n(unused via barrel)\n— needs back-drilling', fontsize=8, color='red')
# Signal path
ax.annotate('', xy=(3, 5.5), xytext=(3, 2.2),
            arrowprops=dict(arrowstyle='->', color='blue', lw=2))
ax.text(4.2, 3.8, 'Signal path\nL3→L1', fontsize=8, color='blue')
ax.set_title('(a) Through-hole Via Cross-section', fontsize=12)
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.axis('off')

# (b) Equivalent circuit
ax = axes[1]
# Draw equivalent circuit
# Pad capacitance
x_vals = [1, 3, 5, 7, 9]
# Input
ax.plot([0.5, 1], [6, 6], 'k-', lw=2)
ax.text(0.3, 6, 'IN', fontsize=9, ha='right')
# C_pad1
ax.plot([1, 1], [5, 7], 'k-', lw=2)
ax.plot([0.6, 1.4], [5, 5], 'k-', lw=1.5)
ax.plot([0.6, 1.4], [7, 7], 'k-', lw=1.5)
ax.text(0.5, 6, '$C_{pad}$', fontsize=10, ha='right')
# L_via
ax.plot([1, 3], [6, 6], 'k-', lw=2)
theta = np.linspace(0, 4*np.pi, 50)
ax.plot(2 + 0.3*np.sin(theta), 6 + 0.15*np.cos(theta), 'k-', lw=2)
ax.text(2, 5.5, '$L_{via}$', fontsize=10, ha='center')
# C_stub
ax.plot([3, 3], [4.5, 7.5], 'k-', lw=2)
ax.plot([2.6, 3.4], [4.5, 4.5], 'k-', lw=1.5)
ax.plot([2.6, 3.4], [7.5, 7.5], 'k-', lw=1.5)
ax.text(3.8, 6, '$C_{stub}$', fontsize=10, ha='left')
# R_via
ax.plot([3, 5], [6, 6], 'k-', lw=2)
ax.plot([3.6, 4.5], [6.4, 6.4], 'k-', lw=2)
ax.plot([4.0, 4.55], [5.95, 6.45], 'k-', lw=2)
ax.plot([3.6, 4.5], [5.6, 5.6], 'k-', lw=2)
ax.text(4.1, 5.1, '$R_{via}$', fontsize=10, ha='center')
# L_via2
ax.plot([5, 7], [6, 6], 'k-', lw=2)
ax.plot(6 + 0.3*np.sin(theta), 6 + 0.15*np.cos(theta), 'k-', lw=2)
ax.text(6, 5.5, '$L_{via}$', fontsize=10, ha='center')
# C_pad2
ax.plot([7, 7], [5, 7], 'k-', lw=2)
ax.plot([6.6, 7.4], [5, 5], 'k-', lw=1.5)
ax.plot([6.6, 7.4], [7, 7], 'k-', lw=1.5)
ax.text(7.5, 6, '$C_{pad}$', fontsize=10, ha='left')
# Output
ax.plot([7, 8.5], [6, 6], 'k-', lw=2)
ax.text(8.7, 6, 'OUT', fontsize=9, ha='left')
# Ground
ax.plot([0.5, 8.5], [2, 2], 'k-', lw=1)
ax.text(9, 2, 'GND', fontsize=9)

# Labels
ax.text(4.5, 8.5, 'Equivalent Circuit of a Via', fontsize=12, ha='center', fontweight='bold')
ax.text(1, 1.5, '$C_{pad}$ ~ 0.5-1 pF per pad', fontsize=8, ha='center')
ax.text(4.5, 1.5, '$L_{via}$ ~ 0.5-2 nH per 0.5mm length', fontsize=8, ha='center')
ax.text(1, 1.0, '$C_{stub}$ — removed by back-drilling', fontsize=8, ha='center', color='red')
ax.text(4.5, 1.0, '$R_{via}$ — DC resistance, usually negligible', fontsize=8, ha='center')
ax.set_xlim(0, 9.5)
ax.set_ylim(0, 9)
ax.axis('off')

plt.tight_layout()
save(fig, '04-via-model.png')

# ============================================================
# 04-target-impedance.png — Target Impedance concept
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Power Integrity — Target Impedance', fontsize=14, fontweight='bold')

# (a) Target impedance concept
ax = axes[0]
f = np.logspace(3, 9, 500)  # 1 kHz to 1 GHz
# PDN impedance
Z_pdn = 0.005 + 0.02 * (f/1e6)**1.5 + 0.1 * np.exp(-(f-5e7)**2/2e15)
# Target impedance
Z_target = np.ones_like(f) * 0.05
ax.loglog(f, Z_pdn, 'b-', lw=2, label='PDN Impedance $Z_{PDN}$')
ax.loglog(f, Z_target, 'r--', lw=2, label='Target $Z_{target}$')
ax.fill_between(f, Z_target, 10, where=(Z_pdn > Z_target),
                color='red', alpha=0.3, label='Violation zone')
ax.fill_between(f, 0.001, Z_target, where=(Z_pdn <= Z_target),
                color='green', alpha=0.15, label='Safe zone')

# Annotate regions
ax.axvline(x=1e4, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=1e6, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=1e8, color='gray', linestyle=':', alpha=0.5)
ax.text(3e3, 0.008, 'VRM\nregion', fontsize=8, ha='center')
ax.text(3e5, 0.008, 'Bulk cap\nregion', fontsize=8, ha='center')
ax.text(3e7, 0.008, 'MLCC\nregion', fontsize=8, ha='center')
ax.text(3e8, 0.008, 'On-die/\npackage', fontsize=8, ha='center')

ax.set_title('(a) Target Impedance Concept', fontsize=12)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Impedance ($\\Omega$)')
ax.legend(fontsize=8, loc='upper left')
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(1e3, 1e9)
ax.set_ylim(0.001, 10)

# (b) Decoupling capacitor network
ax = axes[1]
f2 = np.logspace(3, 9, 500)
# Individual caps
# Bulk (100uF electrolytic)
Z_bulk = 0.05 + np.abs(1/(2j*np.pi*f2*100e-6) + 2j*np.pi*f2*5e-9)
# MLCC 10uF
Z_10u = 0.01 + np.abs(1/(2j*np.pi*f2*10e-6) + 2j*np.pi*f2*1e-9)
# MLCC 0.1uF
Z_01u = 0.05 + np.abs(1/(2j*np.pi*f2*0.1e-6) + 2j*np.pi*f2*0.5e-9)
# MLCC 1000pF
Z_1n = 0.1 + np.abs(1/(2j*np.pi*f2*1e-9) + 2j*np.pi*f2*0.3e-9)
# Combined
Z_parallel = 1/(1/Z_bulk + 1/Z_10u + 1/Z_01u + 1/Z_1n)

ax.loglog(f2, Z_bulk, 'brown', lw=1.5, alpha=0.6, label='100$\\mu$F Bulk')
ax.loglog(f2, Z_10u, 'red', lw=1.5, alpha=0.6, label='10$\\mu$F MLCC')
ax.loglog(f2, Z_01u, 'orange', lw=1.5, alpha=0.6, label='0.1$\\mu$F MLCC')
ax.loglog(f2, Z_1n, 'green', lw=1.5, alpha=0.6, label='1000pF MLCC')
ax.loglog(f2, Z_parallel, 'b-', lw=2.5, label='Combined $Z_{PDN}$')
ax.axhline(y=0.05, color='r', linestyle='--', lw=1.5, label='$Z_{target}$=50m$\\Omega$')

ax.set_title('(b) Multi-stage Decoupling Network', fontsize=12)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Impedance ($\\Omega$)')
ax.legend(fontsize=7, loc='upper right', ncol=2)
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(1e3, 1e9)
ax.set_ylim(0.001, 100)

plt.tight_layout()
save(fig, '04-target-impedance.png')

# ============================================================
# 04-eye-measurement.png — Eye diagram measurement setup
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Eye Diagram Measurement & Analysis', fontsize=14, fontweight='bold')

# (a) Measurement setup
ax = axes[0]
# DUT
rect = plt.Rectangle((3, 4), 4, 2, fill=True, facecolor='lightblue', edgecolor='k', lw=2)
ax.add_patch(rect)
ax.text(5, 5, 'PCB / Channel\n(DUT)', ha='center', va='center', fontsize=10)
# Pattern generator
ax.plot([1, 3], [5, 5], 'k-', lw=2)
ax.text(0.5, 5, 'PRBS\nGenerator', ha='center', fontsize=8)
# Oscilloscope
ax.plot([7, 9], [5, 7], 'k-', lw=2)
rect2 = plt.Rectangle((9, 6.5), 2.5, 1.5, fill=True, facecolor='lightyellow', edgecolor='k', lw=2)
ax.add_patch(rect2)
ax.text(10.25, 7.25, 'Scope\nEye Mode', ha='center', va='center', fontsize=8)
# Clock recovery
ax.plot([7, 9], [5, 3], 'k-', lw=2)
rect3 = plt.Rectangle((9, 2.5), 2.5, 1.5, fill=True, facecolor='lightyellow', edgecolor='k', lw=2)
ax.add_patch(rect3)
ax.text(10.25, 3.25, 'Clock\nRecovery', ha='center', va='center', fontsize=8)

ax.set_xlim(0, 13)
ax.set_ylim(0, 10)
ax.set_title('(a) Eye Diagram Measurement Setup', fontsize=12)
ax.axis('off')

# (b) Mask test
ax = axes[1]
# Eye diagram
np.random.seed(123)
for _ in range(200):
    b = np.random.choice([0, 1])
    t = np.linspace(0, 1, 80)
    y = np.zeros_like(t)
    tr = 0.15
    for j, ti in enumerate(t):
        if ti < tr:
            y[j] = b * ti/tr + (1-b)*(1-ti/tr)
        elif ti > 1-tr:
            y[j] = b*(1-(ti-(1-tr))/tr) + (1-b)*((ti-(1-tr))/tr)
        else:
            y[j] = b
    jitter = 0.03 * np.random.randn()
    noise = 0.04 * np.random.randn(len(t))
    ax.plot(t + jitter, y + noise, 'b-', alpha=0.15, lw=0.5)

# Mask
mask_x = [0.3, 0.7, 0.7, 0.3, 0.3]
mask_y1 = [0.75, 0.75, 0.95, 0.95, 0.75]
mask_y2 = [0.05, 0.05, 0.25, 0.25, 0.05]
ax.fill(mask_x, mask_y1, 'red', alpha=0.15)
ax.fill(mask_x, mask_y2, 'red', alpha=0.15)
ax.plot(mask_x, mask_y1, 'r-', lw=1.5, label='Eye Mask')
ax.plot(mask_x, mask_y2, 'r-', lw=1.5)

ax.set_title('(b) Eye Mask Test — Compliance', fontsize=12)
ax.set_xlabel('Time (UI)')
ax.set_ylabel('Voltage')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(-0.1, 1.3)

plt.tight_layout()
save(fig, '04-eye-measurement.png')

# ============================================================
# 04-pdn-network.png — PDN impedance vs frequency
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
fig.suptitle('Power Distribution Network (PDN) — Impedance Profile', fontsize=14, fontweight='bold')

f3 = np.logspace(1, 10, 1000)  # 10 Hz to 10 GHz
# VRM
Z_vrm = 0.001 + 2*np.pi*f3*10e-9
# Bulk capacitor
Z_bulk2 = 0.05 + np.abs(1/(2j*np.pi*f3*330e-6) + 2j*np.pi*f3*3e-9)
# MLCC network
Z_mlcc = 0.01 + np.abs(1/(2j*np.pi*f3*22e-6) + 2j*np.pi*f3*0.5e-9)
# Package/on-die
Z_pkg = 0.005 + 2*np.pi*f3*0.1e-9

# Combined
Z_total = 1/(1/Z_vrm + 1/Z_bulk2 + 1/Z_mlcc + 1/Z_pkg)

ax.loglog(f3, Z_vrm, 'purple', lw=1.5, alpha=0.6, label='VRM')
ax.loglog(f3, Z_bulk2, 'brown', lw=1.5, alpha=0.6, label='Bulk Caps (330$\\mu$F)')
ax.loglog(f3, Z_mlcc, 'orange', lw=1.5, alpha=0.6, label='MLCC Network (22$\\mu$F)')
ax.loglog(f3, Z_pkg, 'green', lw=1.5, alpha=0.6, label='Package / On-die')
ax.loglog(f3, Z_total, 'b-', lw=2.5, label='Total $Z_{PDN}$')

# Target
ax.axhline(y=0.03, color='r', linestyle='--', lw=2, label='$Z_{target}$ (30m$\\Omega$)')

# Annotate anti-resonance
ax.annotate('Anti-resonance\npeak', xy=(8e5, 0.08), xytext=(2e6, 0.3),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=9, color='red',
            bbox=dict(boxstyle='round', fc='white', alpha=0.8))

ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Impedance ($\\Omega$)')
ax.legend(fontsize=8, loc='upper right', ncol=2)
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(10, 1e10)
ax.set_ylim(0.0005, 10)

plt.tight_layout()
save(fig, '04-pdn-network.png')

# ============================================================
# 04-3w-spacing.png — 3W spacing for crosstalk reduction  
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('3W Rule — Spacing Impact on Crosstalk', fontsize=14, fontweight='bold')

# (a) Geometry
ax = axes[0]
# Cross-section view
for i, (x_bottom, label) in enumerate([(1, 'Trace A'), (4.5, 'Trace B')]):
    # Trace
    rect = plt.Rectangle((x_bottom, 4), 1.5, 0.8, fill=True, facecolor='darkorange', edgecolor='k', lw=1.5)
    ax.add_patch(rect)
    ax.text(x_bottom+0.75, 3.3, label, ha='center', fontsize=9)

# Dielectric
rect_d = plt.Rectangle((0.5, 1.5), 7, 2.5, fill=True, facecolor='tan', edgecolor='k', lw=1, alpha=0.5)
ax.add_patch(rect_d)
ax.text(4, 2.2, 'FR4 ($\\epsilon_r$=4.2)', ha='center', fontsize=9)

# Ground plane
rect_g = plt.Rectangle((0, 0.5), 8, 1, fill=True, facecolor='silver', edgecolor='k', lw=1.5)
ax.add_patch(rect_g)
ax.text(4, 1, 'Ground Plane', ha='center', fontsize=9)

# Dimensions
# W
ax.annotate('', xy=(1, 2.8), xytext=(2.5, 2.8),
            arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
ax.text(1.75, 2.5, 'W', fontsize=10, ha='center', color='blue')
# S (edge to edge)
ax.annotate('', xy=(2.5, 3.5), xytext=(4.5, 3.5),
            arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax.text(3.5, 3.2, 'S = 2W (3W pitch)', fontsize=9, ha='center', color='red')
# H
ax.annotate('', xy=(0.3, 1.5), xytext=(0.3, 4),
            arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
ax.text(0.7, 2.75, 'H', fontsize=10, ha='center', color='green', rotation=90)

# Field lines
for xi in np.linspace(1.75, 2.3, 3):
    ax.plot([xi, xi-0.2], [4.8, 5.3], 'orange', lw=0.5, alpha=0.5)
    ax.plot([xi, xi+0.2], [4.8, 5.3], 'orange', lw=0.5, alpha=0.5)

ax.set_xlim(0, 8)
ax.set_ylim(0, 6)
ax.set_title('(a) Cross-section Geometry', fontsize=12)
ax.axis('off')

# (b) Crosstalk vs spacing
ax = axes[1]
spacing_ratio = np.array([1, 1.5, 2, 3, 4, 5, 7, 10])
xtalk = 100 * np.exp(-spacing_ratio/1.5)  # Empirical
ax.semilogy(spacing_ratio, xtalk, 'b-o', lw=2, markersize=8)
ax.axvline(x=3, color='r', linestyle='--', lw=1.5, alpha=0.5)
ax.text(3.1, 30, '3W Rule\n(crosstalk ~5%)', fontsize=8, color='red')
ax.axhline(y=5, color='green', linestyle=':', lw=1, alpha=0.5)
ax.set_title('(b) Crosstalk vs. Spacing (normalized to W)', fontsize=12)
ax.set_xlabel('Center-to-Center Spacing (×W)')
ax.set_ylabel('Crosstalk (%)')
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(0.5, 10.5)

plt.tight_layout()
save(fig, '04-3w-spacing-xtalk.png')

print('All diagrams generated.')
