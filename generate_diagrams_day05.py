#!/usr/bin/env python3
"""Generate Day 5 diagrams — Crosstalk."""
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
# 05-crosstalk-overview.png — Overview with aggressor/victim
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
fig.suptitle('Crosstalk — Mechanisms and Effects', fontsize=13, fontweight='bold')

# (a) Geometry
ax = axes[0]
# Aggressor
ax.plot([1, 8], [5, 5], 'r-', lw=4, alpha=0.5, label='Aggressor')
ax.text(4.5, 5.5, 'Aggressor (dv/dt, di/dt)', fontsize=8, ha='center', color='red')
# Victim
ax.plot([1, 8], [3, 3], 'b-', lw=4, alpha=0.5, label='Victim')
ax.text(4.5, 2.3, 'Victim (receives noise)', fontsize=8, ha='center', color='blue')
# Coupling arrows
for x in [3, 5, 7]:
    ax.annotate('', xy=(x, 3.3), xytext=(x, 4.7),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
ax.text(4.5, 4, 'Cm, Lm', fontsize=9, ha='center', color='purple')
# Driver
ax.plot(0.5, 5, 'r^', markersize=12)
ax.text(0.2, 5, 'Driver', fontsize=7, ha='right')
# Near/Far end
ax.plot(0.5, 3, 'bv', markersize=10)
ax.text(0.5, 2, 'Near End', fontsize=7, ha='center')
ax.plot(8.5, 3, 'b^', markersize=10)
ax.text(8.5, 2, 'Far End', fontsize=7, ha='center')

ax.set_title('(a) Coupled Lines', fontsize=10)
ax.set_xlim(0, 9)
ax.set_ylim(1, 7)
ax.axis('off')

# (b) Capacitive coupling
ax = axes[1]
t = np.linspace(0, 10, 200)
# Aggressor step
v_agg = 1.0 * (t > 1.5) * (1 - np.exp(-(t-1.5)*4))
ax.plot(t, 2 + v_agg, 'r-', lw=2.5, label='Aggressor')
# Victim far-end noise (capacitive - narrow pulse)
v_fext = 0.15 * np.exp(-(t-1.8)**2/0.05)
ax.plot(t, 1 + v_fext, 'b-', lw=2, label='Victim (FEXT)')
ax.axhline(y=1.5, color='gray', linestyle=':', alpha=0.3)
ax.axhline(y=2.5, color='gray', linestyle=':', alpha=0.3)
ax.text(3, 2.5, 'Agressor dv/dt', fontsize=7, color='red')
ax.text(2.2, 0.8, 'Coupled noise\npulse', fontsize=7, color='blue')
ax.set_title('(b) Capacitive: dv/dt → I_noise', fontsize=10)
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.legend(fontsize=7)
ax.set_ylim(0.5, 3.5)
ax.grid(True, alpha=0.3)

# (c) Inductive coupling
ax = axes[2]
i_agg = 2 * (t > 1.5) * (1 - np.exp(-(t-1.5)*3))
ax.plot(t, 2 + i_agg*0.3, 'r-', lw=2.5, label='Aggressor current')
v_ind = -0.25 * np.gradient(i_agg)
ax.plot(t, 1 + v_ind, 'b-', lw=2, label='Victim (induced)')
ax.axhline(y=1.5, color='gray', linestyle=':', alpha=0.3)
ax.text(5, 2.6, 'Agressor di/dt', fontsize=7, color='red')
ax.text(2, 1.3, 'Induced\nvoltage spike', fontsize=7, color='blue')
ax.set_title('(c) Inductive: di/dt → V_noise', fontsize=10)
ax.set_xlabel('Time')
ax.set_ylabel('Voltage')
ax.legend(fontsize=7)
ax.set_ylim(0.5, 3.5)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save(fig, '05-crosstalk-overview.png')

# ============================================================
# 05-crosstalk-spacing.png — Spacing impact
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
fig.suptitle('Crosstalk vs. Spacing — The 3W Rule', fontsize=13, fontweight='bold')

spacing = np.array([1, 1.5, 2, 2.5, 3, 4, 5, 7, 10])
xtalk = 100 * np.exp(-spacing/1.8)
ax.semilogy(spacing, xtalk, 'b-o', lw=2.5, markersize=10, label='Crosstalk %')
ax.axvline(x=3, color='r', linestyle='--', lw=2, alpha=0.6)
ax.text(3.15, 30, '3W Rule', fontsize=10, color='red', fontweight='bold')
ax.axhline(y=5, color='green', linestyle=':', lw=1.5, alpha=0.5)
ax.text(9, 5.5, '~5% @ 3W', fontsize=9, color='green')

# Annotate zones
ax.fill_between([0.5, 2], 0.1, 60, alpha=0.08, color='red')
ax.text(1.3, 0.2, 'Danger\nZone', fontsize=8, color='red', ha='center', fontweight='bold')
ax.fill_between([2, 3], 0.1, 15, alpha=0.08, color='orange')
ax.text(2.5, 0.15, 'Marginal', fontsize=8, color='orange', ha='center')
ax.fill_between([3, 10.5], 0.1, 5, alpha=0.08, color='green')
ax.text(6, 0.12, 'Safe Zone', fontsize=8, color='green', ha='center')

ax.set_xlabel('Center-to-Center Spacing (× W)', fontsize=11)
ax.set_ylabel('Crosstalk (%)', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(0.5, 10.5)
ax.set_ylim(0.08, 100)

# Corner annotation
ax.text(8, 30, 'Crosstalk ∝ 1/distance²\n(approximate)', fontsize=8,
        ha='center', style='italic', bbox=dict(boxstyle='round', fc='white', alpha=0.7))

plt.tight_layout()
save(fig, '05-crosstalk-spacing.png')

# ============================================================
# 05-edge-vs-broadside.png — Edge vs Broadside coupling
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Edge Coupling vs Broadside Coupling', fontsize=13, fontweight='bold')

# (a) Edge coupling (same layer)
ax = axes[0]
for i, (x, label) in enumerate([(2, 'Aggressor'), (5, 'Victim')]):
    rect = plt.Rectangle((x-0.6, 3.5), 1.2, 0.6, fill=True, facecolor='darkorange' if i==0 else 'steelblue', edgecolor='k', lw=1.5)
    ax.add_patch(rect)
    ax.text(x, 2.8, label, fontsize=8, ha='center')
# Dielectric
rect_d = plt.Rectangle((0.5, 1.5), 6, 2, fill=True, facecolor='tan', edgecolor='k', lw=1, alpha=0.5)
ax.add_patch(rect_d)
# Ground plane
rect_g = plt.Rectangle((0, 0.5), 7, 1, fill=True, facecolor='silver', edgecolor='k', lw=1.5)
ax.add_patch(rect_g)
ax.text(3.5, 1, 'Ground Plane', fontsize=9, ha='center')
# Dimensions
ax.annotate('', xy=(1.4, 4.5), xytext=(4.4, 4.5),
            arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax.text(2.9, 4.8, 'S (edge-to-edge)', fontsize=9, ha='center', color='red')
ax.text(6.5, 2, 'FR4', fontsize=9, ha='right')
ax.set_title('(a) Edge Coupling — Same Layer', fontsize=11)
ax.set_xlim(0, 8)
ax.set_ylim(0, 6)
ax.axis('off')

# (b) Broadside coupling (adjacent layers)
ax = axes[1]
# Top trace
rect1 = plt.Rectangle((2, 4.5), 3, 0.5, fill=True, facecolor='darkorange', edgecolor='k', lw=1.5)
ax.add_patch(rect1)
ax.text(3.5, 5.3, 'Aggressor (L2)', fontsize=8, ha='center', color='darkorange')
# Bottom trace
rect2 = plt.Rectangle((1.5, 3.5), 3, 0.5, fill=True, facecolor='steelblue', edgecolor='k', lw=1.5)
ax.add_patch(rect2)
ax.text(3.5, 2.8, 'Victim (L3)', fontsize=8, ha='center', color='steelblue')
# Dielectric between
rect_d2 = plt.Rectangle((0.5, 1.5), 6, 2.5, fill=True, facecolor='tan', edgecolor='k', lw=1, alpha=0.4)
ax.add_patch(rect_d2)
ax.text(6.7, 4, 'PP\n(~0.1mm)', fontsize=7, ha='center')
# Ground
rect_g2 = plt.Rectangle((0, 0.5), 7, 1, fill=True, facecolor='silver', edgecolor='k', lw=1.5)
ax.add_patch(rect_g2)
# Warning
ax.annotate('⚠ Overlap = serious crosstalk', xy=(3.5, 4.0), fontsize=10, ha='center',
            color='red', fontweight='bold',
            bbox=dict(boxstyle='round', fc='white', ec='red', alpha=0.8))
# Cross-section marker
ax.annotate('', xy=(6.2, 5.5), xytext=(6.2, 2.5),
            arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
ax.text(6.8, 4, 'Broadside\ncoupling\n(×10 edge)', fontsize=7, color='red')

ax.set_title('(b) Broadside Coupling — Adjacent Layers', fontsize=11)
ax.set_xlim(0, 8)
ax.set_ylim(0, 6.5)
ax.axis('off')

plt.tight_layout()
save(fig, '05-edge-vs-broadside.png')

# ============================================================
# 05-guard-trace.png — Guard trace effectiveness
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Guard Trace — When It Works and When It Doesn\'t', fontsize=13, fontweight='bold')

# (a) Surface — guard trace works (with dense vias)
ax = axes[0]
rects = [
    (1.5, 'Aggr', 'darkorange'),
    (2.8, 'GND', 'gray'),
    (4.1, 'Vict', 'steelblue'),
]
for x, label, color in rects:
    rect = plt.Rectangle((x-0.5, 4), 1, 0.6, fill=True, facecolor=color, edgecolor='k', lw=1.2)
    ax.add_patch(rect)
    ax.text(x, 3.3, label, fontsize=8, ha='center')
# Vias on guard trace
for yi in [1.5, 2.5, 5.5, 6.5]:
    ax.plot(2.8, yi, 'kD', markersize=6)
ax.text(2.8, 1, 'GND vias\n(λ/10 spacing)', fontsize=7, ha='center')
# Dielectric + ground
rect_d = plt.Rectangle((0.3, 1.5), 5.4, 2, fill=True, facecolor='tan', edgecolor='k', lw=1, alpha=0.4)
ax.add_patch(rect_d)
rect_g = plt.Rectangle((0, 0.5), 6, 1, fill=True, facecolor='silver', edgecolor='k', lw=1.5)
ax.add_patch(rect_g)
ax.text(3, 0.3, '✅ Surface: guard trace can help (with dense vias)', fontsize=10,
        ha='center', color='green', fontweight='bold')
ax.set_title('(a) Surface Layer', fontsize=11)
ax.set_xlim(0, 6.5)
ax.set_ylim(0, 7)
ax.axis('off')

# (b) Inner layer — guard trace useless for FEXT, helps NEXT slightly
ax = axes[1]
rects2 = [
    (1.5, 'Aggr', 'darkorange'),
    (2.8, 'GND', 'gray'),
    (4.1, 'Vict', 'steelblue'),
]
for x, label, color in rects2:
    rect = plt.Rectangle((x-0.5, 4), 1, 0.6, fill=True, facecolor=color, edgecolor='k', lw=1.2)
    ax.add_patch(rect)
    ax.text(x, 3.3, label, fontsize=8, ha='center')
# Top and bottom reference planes
rect_top = plt.Rectangle((0, 5.5), 6, 1, fill=True, facecolor='silver', edgecolor='k', lw=1.5)
ax.add_patch(rect_top)
rect_bot = plt.Rectangle((0, 0.5), 6, 1, fill=True, facecolor='silver', edgecolor='k', lw=1.5)
ax.add_patch(rect_bot)
rect_d2 = plt.Rectangle((0.3, 1.5), 5.4, 4, fill=True, facecolor='tan', edgecolor='k', lw=1, alpha=0.4)
ax.add_patch(rect_d2)
ax.text(3, 0.3, '⚠ Stripline: guard trace does little\n    FEXT already zero, NEXT: just increase spacing', fontsize=9,
        ha='center', color='red', fontweight='bold')
ax.set_title('(b) Inner Layer (Stripline)', fontsize=11)
ax.set_xlim(0, 6.5)
ax.set_ylim(0, 7)
ax.axis('off')

plt.tight_layout()
save(fig, '05-guard-trace.png')

# ============================================================
# 05-9-methods-summary.png — 9 methods to reduce crosstalk
# ============================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 7))
fig.suptitle('9 Methods to Reduce Crosstalk', fontsize=14, fontweight='bold')
ax.set_xlim(0, 20)
ax.set_ylim(0, 18)
ax.axis('off')

methods = [
    (2, 16, '①', '增大线间距\n(3W+)', '★×5', '最有效，代价是面积'),
    (7, 16, '②', '减小平行\n走线长度', '★×4', 'Layout 优化'),
    (12, 16, '③', '内层布线\n消除 FEXT', '★×5', '需要完整参考平面'),
    (17, 16, '④', '端接减少\n反射噪声', '★×3', '配合使用效果好'),
    (2, 13, '⑤', '相邻层\n正交走线', '★×3', '避免宽边耦合'),
    (7, 13, '⑥', '增加信号\n上升时间', '★×2', '仅限时序允许'),
    (12, 13, '⑦', '保护地线\n(低频模拟)', '★×2', '高速谨慎使用'),
    (17, 13, '⑧', '低 εr 板材\n间接减串扰', '★×2', '效果间接，成本高'),
    (10, 10, '⑨', '控阻抗\n间接减串扰', '★×2', '阻抗好则反射少'),
]

for x, y, num, title, stars, note in methods:
    color = 'lightgreen' if '★×5' in stars else ('lightskyblue' if '★×4' in stars else ('lightyellow' if '★×3' in stars else 'lightgray'))
    rect = plt.Rectangle((x-1.5, y-1.2), 4.2, 2.4, fill=True, facecolor=color, edgecolor='k', lw=1.2, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x+0.6, y+0.8, num, fontsize=10, fontweight='bold')
    ax.text(x-0.2, y, title, fontsize=8, ha='center', va='center')
    ax.text(x+0.6, y-0.3, stars, fontsize=7, ha='center', color='darkred')
    ax.text(x+0.6, y-0.8, note, fontsize=6, ha='center', color='gray', style='italic')

plt.tight_layout()
save(fig, '05-9-methods.png')

print('All Day 5 diagrams generated.')
