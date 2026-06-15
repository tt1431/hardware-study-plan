#!/usr/bin/env python3
"""Generate Day 4 diagrams — Termination & Topology."""
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
# 04-termination-comparison.png — 4 termination types side by side
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle('Four Termination Strategies', fontsize=14, fontweight='bold')

types = [
    ('(a) Series (Source)', 'Driver', 'Rs', 'Z0', 'Receiver\n(Hi-Z)'),
    ('(b) Parallel (End)', 'Driver', 'Z0', '', 'Rt=Z0'),
    ('(c) Thevenin', 'Driver', 'Z0', '', 'R1||R2=Z0'),
    ('(d) AC Termination', 'Driver', 'Z0', '', 'C + Rt=Z0'),
]

for idx, (title, drv, key, mid, rcv) in enumerate(types):
    ax = axes[idx // 2, idx % 2]
    x_positions = [1, 3, 5, 7, 9]
    y = 4

    # Driver symbol
    ax.plot(x_positions[0], y, 'k^', markersize=14)
    ax.text(x_positions[0]-0.3, y+0.5, drv, fontsize=8, ha='center')

    # Series resistor (for type a)
    if idx == 0:
        rect = plt.Rectangle((x_positions[1]-0.3, y-0.2), 0.6, 0.4, fill=True,
                            facecolor='orange', edgecolor='k', lw=1.5)
        ax.add_patch(rect)
        ax.text(x_positions[1], y-1, 'Rs', fontsize=9, ha='center', color='red')

    # Transmission line
    ax.plot([x_positions[1]+0.5 if idx==0 else x_positions[0]+0.5, x_positions[3]-0.5],
            [y, y], 'b-', lw=4, alpha=0.6)
    ax.text(x_positions[2], y+0.4, 'Z0', fontsize=9, ha='center', color='blue')

    # Receiver end
    if idx == 1:  # Parallel
        rect = plt.Rectangle((x_positions[3]-0.3, y-0.2), 0.6, 0.4, fill=True,
                            facecolor='lightgreen', edgecolor='k', lw=1.5)
        ax.add_patch(rect)
        ax.plot([x_positions[3], x_positions[3]], [y-0.2, 1], 'k-', lw=1.5)
        ax.text(x_positions[3], y-1.2, 'Rt=Z0', fontsize=7, ha='center', color='red')
    elif idx == 2:  # Thevenin
        ax.plot([x_positions[3], x_positions[3]], [y-0.2, 1], 'k-', lw=1.5)
        rect1 = plt.Rectangle((x_positions[3]-0.3, 1), 0.6, 0.4, fill=True,
                             facecolor='lightgreen', edgecolor='k', lw=1.5)
        ax.add_patch(rect1)
        ax.text(x_positions[3]+0.8, 1.2, 'R1', fontsize=7, color='red')
        rect2 = plt.Rectangle((x_positions[3]-0.3, 2.2), 0.6, 0.4, fill=True,
                             facecolor='lightgreen', edgecolor='k', lw=1.5)
        ax.add_patch(rect2)
        ax.text(x_positions[3]+0.8, 2.4, 'R2', fontsize=7, color='red')
        ax.text(x_positions[3], 0.6, 'Vcc', fontsize=7, ha='center')
        ax.text(x_positions[3], 3.2, 'GND', fontsize=7, ha='center')
    elif idx == 3:  # AC
        rect = plt.Rectangle((x_positions[3]-0.3, y-0.2), 0.6, 0.4, fill=True,
                            facecolor='lightgreen', edgecolor='k', lw=1.5)
        ax.add_patch(rect)
        # Capacitor symbol
        cap_x = x_positions[3]
        ax.plot([cap_x-0.2, cap_x+0.2], [1.8, 1.8], 'k-', lw=1.5)
        ax.plot([cap_x-0.2, cap_x+0.2], [1.5, 1.5], 'k-', lw=1.5)
        ax.plot([cap_x, cap_x], [1.5, 1.8], 'k-', lw=1.5)
        ax.plot([cap_x, cap_x], [1.5, 1], 'k-', lw=1.5)
        ax.text(cap_x+0.6, 1.65, 'C', fontsize=8, color='red')
        ax.text(cap_x, 0.5, 'Rt=Z0', fontsize=7, ha='center', color='red')

    # Receiver
    ax.plot(x_positions[3], y, 'kv', markersize=14)
    ax.text(x_positions[3], y+0.6, rcv, fontsize=7, ha='center')

    # Ground
    ax.plot([0, 10], [0, 0], 'k-', lw=1)
    ax.text(10.5, 0, 'GND', fontsize=7)

    ax.set_title(title, fontsize=12)
    ax.set_xlim(0, 11)
    ax.set_ylim(-2, 6)
    ax.axis('off')

plt.tight_layout()
save(fig, '04-termination-comparison.png')

# ============================================================
# 04-series-termination-waves.png — Series termination voltage vs time
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
fig.suptitle('Series Termination — Why Half-Voltage Works', fontsize=14, fontweight='bold')

# (a) Voltage at source vs load
ax = axes[0]
t = np.linspace(0, 30, 300)
Td = 4  # one-way delay

# Source waveform
v_src = np.zeros_like(t)
v_src[t >= 2] = 0.5  # half voltage initial
v_src[t >= 2 + 2*Td] = 1.0  # after reflection returns

# Load waveform
v_load = np.zeros_like(t)
v_load[t >= 2 + Td] = 1.0  # incident + reflection = full

ax.plot(t, v_src, 'b-', lw=2, label='At driver (source)')
ax.plot(t, v_load, 'r-', lw=2, label='At receiver (load)')

# Annotations
ax.axvline(x=2, color='gray', linestyle=':', alpha=0.5)
ax.text(2, 1.15, 'Step\nlaunched', fontsize=7, ha='center')
ax.axvline(x=2+Td, color='gray', linestyle=':', alpha=0.5)
ax.text(2+Td, 1.15, 'Arrives at\nload (×2)', fontsize=7, ha='center')
ax.axvline(x=2+2*Td, color='gray', linestyle=':', alpha=0.5)
ax.text(2+2*Td, 1.15, 'Reflection\nreturns', fontsize=7, ha='center')

ax.fill_between(t, 0, v_src, alpha=0.15, color='blue')
ax.fill_between(t, 0, v_load, alpha=0.1, color='red')
ax.set_title('(a) Voltage at Source vs Load', fontsize=11)
ax.set_xlabel('Time')
ax.set_ylabel('Normalized Voltage')
ax.legend(fontsize=8)
ax.set_ylim(-0.1, 1.4)
ax.grid(True, alpha=0.3)

# (b) Bounce diagram
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.set_title('(b) Bounce Diagram', fontsize=11)
ax.set_xlabel('Position (source → load)')
ax.set_ylabel('Time (×Td)')

# Draw transmission line
ax.plot([2, 8], [0, 0], 'b-', lw=4, alpha=0.3)
ax.text(5, -0.5, 'Z0 = 50Ω', fontsize=9, ha='center')
ax.text(1, 0, 'Source\n(Rs+Ro=Z0)', fontsize=7, ha='center')
ax.text(9, 0, 'Load\n(Hi-Z)', fontsize=7, ha='center')
ax.text(5, 0.8, 'Γ = 0', fontsize=9, ha='center', color='green')

# Incident wave
ax.annotate('', xy=(8, 2), xytext=(2, 2),
            arrowprops=dict(arrowstyle='->', color='blue', lw=2))
ax.text(5, 2.3, '① Incident  V=0.5V0', fontsize=8, ha='center', color='blue')

# Reflected wave
ax.annotate('', xy=(2, 6), xytext=(8, 6),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.text(5, 6.3, '② Reflected  V=+0.5V0  (Γ=+1)', fontsize=8, ha='center', color='red')

# No further reflection
ax.annotate('', xy=(8, 9), xytext=(2, 9),
            arrowprops=dict(arrowstyle='->', color='green', lw=2, alpha=0.5))
ax.text(5, 9.3, '③ Γ=0 at source → done', fontsize=8, ha='center', color='green')

# Time labels
ax.text(0.5, 2, 'Td', fontsize=7)
ax.text(0.5, 6, '3Td', fontsize=7)

ax.axis('off')

plt.tight_layout()
save(fig, '04-series-termination-waves.png')

# ============================================================
# 04-topology-types.png — 4 topology types
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Topology Types for Multi-Load Buses', fontsize=14, fontweight='bold')

# (a) Point-to-point
ax = axes[0, 0]
ax.plot([1, 4], [3, 3], 'b-', lw=3, alpha=0.6)
ax.plot(1, 3, 'k^', markersize=12)
ax.plot(4, 3, 'kv', markersize=12)
ax.text(0.5, 3, 'Driver', fontsize=8, ha='right')
ax.text(4.5, 3, 'Receiver', fontsize=8, ha='left')
ax.text(2.5, 3.5, 'Single Z0', fontsize=8, ha='center', color='blue')
ax.set_title('(a) Point-to-Point', fontsize=11)
ax.set_xlim(0, 8)
ax.set_ylim(0, 6)
ax.axis('off')

# (b) Daisy chain
ax = axes[0, 1]
ax.plot([1, 2.5, 4, 5.5], [3, 3, 3, 3], 'b-', lw=3, alpha=0.6)
ax.plot(1, 3, 'k^', markersize=12)
for xp in [2.5, 4, 5.5]:
    ax.plot(xp, 3, 'kv', markersize=10)
ax.text(0.5, 3, 'Driver', fontsize=8, ha='right')
ax.text(2.5, 2.2, 'Rx1', fontsize=7, ha='center')
ax.text(4, 2.2, 'Rx2', fontsize=7, ha='center')
ax.text(5.5, 2.2, 'Rx3', fontsize=7, ha='center')
# Termination
ax.plot([5.5, 5.5], [3, 1.5], 'k-', lw=1)
ax.text(5.5, 1, 'Rt=Z0', fontsize=7, ha='center', color='red')
ax.set_title('(b) Daisy Chain', fontsize=11)
ax.set_xlim(0, 8)
ax.set_ylim(0, 6)
ax.axis('off')

# (c) Star topology
ax = axes[1, 0]
center = [3, 3]
ax.plot(center[0], center[1], 'ko', markersize=8)
# Stubs
for angle, label in [(np.pi, 'Rx1'), (-np.pi/2, 'Rx2'), (0, 'Rx3'), (np.pi/2, 'Rx4')]:
    ex = center[0] + 2.5 * np.cos(angle)
    ey = center[1] + 2.5 * np.sin(angle)
    ax.plot([center[0], ex], [center[1], ey], 'b-', lw=2, alpha=0.6)
    ax.plot(ex, ey, 'kv', markersize=10)
    ax.text(ex + 0.3*np.cos(angle), ey + 0.3*np.sin(angle), label, fontsize=7, ha='center')
ax.plot(center[0]-1.5, center[1], 'k^', markersize=12)
ax.text(center[0]-2, center[1], 'Driver', fontsize=8, ha='right')
# Red X marks
ax.text(center[0]+1, center[1]+1.5, '✗ Stubs cause\nreflections', fontsize=8, color='red')
ax.set_title('(c) Star (Rarely Used)', fontsize=11)
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 7)
ax.axis('off')

# (d) Fly-by (DDR)
ax = axes[1, 1]
addr_x = np.linspace(1, 6, 5)  # 5 devices
for i, xp in enumerate(addr_x):
    ax.plot(xp, 4, 'ks', markersize=10)
    ax.text(xp, 3.5, f'DDR{i+1}', fontsize=6, ha='center')
# Address bus
ax.plot([0.5, 6.5], [4, 4], 'b-', lw=3, alpha=0.6)
ax.text(3.5, 4.5, 'Address/Command (Fly-by)', fontsize=8, ha='center', color='blue')
# Termination
ax.plot([6.5, 6.5], [4, 2], 'k-', lw=1)
ax.text(6.5, 1.5, 'VTT\nRt=Z0', fontsize=7, ha='center', color='red')
# Controller
ax.plot(0.5, 4, 'k^', markersize=14)
ax.text(-0.2, 4, 'Controller', fontsize=8, ha='right')
# DQ lines (point-to-point)
ax.text(3.5, 1.8, 'DQ/DQS: point-to-point per rank', fontsize=8, ha='center', color='green', style='italic')
ax.set_title('(d) Fly-by (DDR4/5)', fontsize=11)
ax.set_xlim(-1, 8)
ax.set_ylim(0, 6.5)
ax.axis('off')

plt.tight_layout()
save(fig, '04-topology-types.png')

# ============================================================
# 04-tdr-principle.png — TDR how it works
# ============================================================
fig, axes = plt.subplots(2, 1, figsize=(12, 7))
fig.suptitle('TDR — Time Domain Reflectometry', fontsize=14, fontweight='bold')

# (a) TDR setup
ax = axes[0]
# Pulse generator
rect = plt.Rectangle((1, 3.5), 2, 1.5, fill=True, facecolor='lightyellow', edgecolor='k', lw=1.5)
ax.add_patch(rect)
ax.text(2, 4.25, 'Fast Step\nGenerator\n(Tr ~ 35ps)', fontsize=8, ha='center')
# DUT
rect2 = plt.Rectangle((4.5, 3.5), 3, 1.5, fill=True, facecolor='lightblue', edgecolor='k', lw=1.5)
ax.add_patch(rect2)
ax.text(6, 4.25, 'DUT\n(PCB trace / cable)', fontsize=8, ha='center')
# Scope
rect3 = plt.Rectangle((9, 3.5), 2, 1.5, fill=True, facecolor='lightyellow', edgecolor='k', lw=1.5)
ax.add_patch(rect3)
ax.text(10, 4.25, 'Sampling\nScope', fontsize=8, ha='center')
# Connections
ax.plot([3, 4.5], [4.25, 4.25], 'k-', lw=2)
ax.plot([7.5, 9], [4.25, 4.25], 'k-', lw=2)
# Reflection path
ax.annotate('Incident', xy=(4, 3), xytext=(3, 2), fontsize=8, color='blue',
            arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
ax.annotate('Reflected', xy=(8, 3), xytext=(7, 2), fontsize=8, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

ax.set_title('(a) TDR Measurement Setup', fontsize=11)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

# (b) TDR waveform interpretation
ax = axes[1]
t = np.linspace(0, 20, 500)
Z = np.ones_like(t) * 50  # baseline 50Ω

# First: slight dip (connector pad)
Z[50:70] = 50 - 5 * np.exp(-(np.arange(20)-10)**2/30)
# Via (inductive spike)
Z[120:135] = 50 + 25 * np.exp(-(np.arange(15)-5)**2/5)
# Stub (capacitive dip)
Z[180:195] = 50 - 20 * np.exp(-(np.arange(15)-5)**2/5)
# Narrow trace (higher Z)
Z[250:350] = 62
# Back to normal
Z[380:420] = 50 + 8 * np.exp(-(np.arange(40)-20)**2/100)

ax.plot(t, Z, 'b-', lw=2)
ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
ax.fill_between(t, 45, 55, alpha=0.08, color='green')
ax.text(18, 52, '50Ω ±10%', fontsize=8, ha='right', color='green')

# Annotations
ax.annotate('Connector\npad cap', xy=(t[55], Z[55]), xytext=(2, 42),
            fontsize=7, color='red', arrowprops=dict(arrowstyle='->', color='red', lw=1))
ax.annotate('Via\n(inductive)', xy=(t[128], Z[128]), xytext=(5, 72),
            fontsize=7, color='red', arrowprops=dict(arrowstyle='->', color='red', lw=1))
ax.annotate('Stub\n(capacitive)', xy=(t[188], Z[188]), xytext=(8, 35),
            fontsize=7, color='red', arrowprops=dict(arrowstyle='->', color='red', lw=1))
ax.annotate('Narrow trace\n(Z > 50Ω)', xy=(t[300], Z[300]), xytext=(13, 68),
            fontsize=7, color='blue', arrowprops=dict(arrowstyle='->', color='blue', lw=1))

ax.set_title('(b) TDR Waveform — What Each Feature Means', fontsize=11)
ax.set_xlabel('Distance / Time')
ax.set_ylabel('Impedance (Ω)')
ax.grid(True, alpha=0.3)
ax.set_ylim(25, 80)

plt.tight_layout()
save(fig, '04-tdr-principle.png')

# ============================================================
# 04-termination-decision.png — Decision tree
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
fig.suptitle('Termination Decision Flow', fontsize=14, fontweight='bold')
ax.set_xlim(0, 20)
ax.set_ylim(0, 16)
ax.axis('off')

# Root
ax.text(10, 15, 'Need termination?', fontsize=11, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round', fc='lightyellow', ec='k'))
ax.annotate('', xy=(6, 13.5), xytext=(10, 14.5),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.annotate('', xy=(14, 13.5), xytext=(10, 14.5),
            arrowprops=dict(arrowstyle='->', lw=1.5))

# L > L_critical?
ax.text(6, 13, 'L > L_critical?', fontsize=9, ha='center',
        bbox=dict(boxstyle='round', fc='white', ec='k'))
ax.text(14, 13, 'No → wire model', fontsize=8, ha='center', color='gray')

# Topology?
ax.annotate('', xy=(6, 11.5), xytext=(6, 12.5),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(6, 11, 'Topology?', fontsize=10, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round', fc='lightblue', ec='k'))

# Point-to-point
ax.annotate('', xy=(2, 9), xytext=(5, 10.5),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(2, 8.5, 'Point-to-Point', fontsize=9, ha='center',
        bbox=dict(boxstyle='round', fc='lightgreen', ec='k'))
ax.annotate('', xy=(2, 7), xytext=(2, 8),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(2, 6.5, 'Series Rs', fontsize=10, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round', fc='lightgreen', ec='k', pad=0.8))
ax.text(2, 5, 'Rs+Ro = Z0\nLow power\nClean signal', fontsize=7, ha='center')

# Multi-load
ax.annotate('', xy=(10, 9), xytext=(7, 10.5),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(10, 8.5, 'Multi-load', fontsize=9, ha='center',
        bbox=dict(boxstyle='round', fc='lightsalmon', ec='k'))

# Daisy chain
ax.annotate('', xy=(8, 7), xytext=(9.5, 8),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(8, 6.5, 'Daisy Chain\n/ Fly-by', fontsize=8, ha='center',
        bbox=dict(boxstyle='round', fc='lightsalmon', ec='k'))
ax.annotate('', xy=(8, 5), xytext=(8, 6),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(8, 4.5, 'Thevenin\nat end', fontsize=9, ha='center',
        bbox=dict(boxstyle='round', fc='lightsalmon', ec='k'))

# Bus
ax.annotate('', xy=(12, 7), xytext=(10.5, 8),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(12, 6.5, 'Bus / Star', fontsize=8, ha='center',
        bbox=dict(boxstyle='round', fc='lightsalmon', ec='k'))
ax.annotate('', xy=(12, 5), xytext=(12, 6),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(12, 4.5, 'Thevenin\nboth ends', fontsize=9, ha='center',
        bbox=dict(boxstyle='round', fc='lightsalmon', ec='k'))

# Low power option
ax.text(17, 10, 'Low power\noption?', fontsize=8, ha='center',
        bbox=dict(boxstyle='round', fc='plum', ec='k'))
ax.annotate('', xy=(17, 8.5), xytext=(17, 9.5),
            arrowprops=dict(arrowstyle='->', lw=1.5))
ax.text(17, 8, 'AC Termination\nC + Rt = Z0', fontsize=8, ha='center',
        bbox=dict(boxstyle='round', fc='plum', ec='k'))

plt.tight_layout()
save(fig, '04-termination-decision.png')

print('All Day 4 diagrams generated.')
