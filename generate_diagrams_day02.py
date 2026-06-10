#!/usr/bin/env python3
"""Generate diagrams for Day 02 - Spectrum and Bandwidth."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), 'assets')
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Noto Sans CJK SC', 'AR PL UKai CN', 'DejaVu Sans'],
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'axes.unicode_minus': False,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

BLUE = '#2196F3'
RED = '#F44336'
GREEN = '#4CAF50'
ORANGE = '#FF9800'
PURPLE = '#9C27B0'
GRAY = '#757575'
DARK = '#212121'

# ============================================================
# 1. Square wave decomposition
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(10, 7))

# Top-left: square wave
t = np.linspace(0, 4*np.pi, 1000)
sq = np.zeros_like(t)
for i, ti in enumerate(t):
    cycle = ti % (2*np.pi)
    sq[i] = 1 if cycle < np.pi else -1

axes[0, 0].plot(t, sq, 'k', lw=2)
axes[0, 0].set_title('方波（时域）', fontweight='bold')
axes[0, 0].set_ylabel('幅度')
axes[0, 0].set_ylim(-1.5, 1.5)
axes[0, 0].grid(alpha=0.3)
axes[0, 0].set_xticks([])

# Top-right: spectrum bars
harmonics = [1, 3, 5, 7, 9, 11, 13, 15]
amps = [4/(np.pi*n) for n in harmonics]
colors = [BLUE, RED, GREEN, ORANGE, PURPLE, '#E91E63', '#00BCD4', '#795548']

axes[0, 1].bar(harmonics, amps, width=0.6, color=colors, alpha=0.8, edgecolor=DARK)
axes[0, 1].set_title('频谱（频域）', fontweight='bold')
axes[0, 1].set_ylabel('幅度')
axes[0, 1].set_xlabel('谐波次数')
axes[0, 1].grid(alpha=0.3, axis='y')
for h, a in zip(harmonics, amps):
    axes[0, 1].text(h, a + 0.05, f'{1/h:.2f}', ha='center', fontsize=8, color=DARK)

# Bottom-left: step-by-step reconstruction
axes[1, 0].set_title('谐波叠加还原方波', fontweight='bold')
ns = [1, 3, 5, 15]
for idx, n_max in enumerate(ns):
    y = np.zeros_like(t)
    for n in range(1, n_max+1, 2):
        y += (4/(np.pi*n)) * np.sin(n * t)
    axes[1, 0].plot(t, y + idx*2.5, lw=1.5, color=[BLUE, RED, GREEN, PURPLE][idx],
                     alpha=0.8, label=f'1~{n_max}次谐波')
axes[1, 0].set_yticks([])
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(alpha=0.3)

# Bottom-right: log-log spectrum
freqs = np.array([1, 3, 5, 7, 10, 30, 50, 70, 100])
ideal = 4/(np.pi * freqs)
# trapezoidal with corner at f=30
trap = np.copy(ideal)
for i, f in enumerate(freqs):
    if f > 30:
        trap[i] = ideal[i] * (30/f)**2  # -40dB/dec beyond corner

axes[1, 1].loglog(freqs, ideal, 'b-', lw=2, label='理想方波 (-20dB/dec)')
axes[1, 1].loglog(freqs, trap, 'r-', lw=2, label='梯形波 Tr>0')
axes[1, 1].axvline(x=30, color=RED, ls='--', lw=1, alpha=0.7)
axes[1, 1].text(35, 0.06, '拐点\nf₂=1/(π·Tr)', fontsize=9, color=RED)
axes[1, 1].set_title('对数频谱对比', fontweight='bold')
axes[1, 1].set_xlabel('频率 (对数)')
axes[1, 1].set_ylabel('幅度 (对数)')
axes[1, 1].legend(fontsize=9)
axes[1, 1].grid(alpha=0.3)

plt.suptitle('方波的傅里叶分解', fontweight='bold', fontsize=15)
plt.tight_layout()
plt.savefig(f'{OUT}/02-square-wave-decomposition.png')
plt.close()

# ============================================================
# 2. Bandwidth vs Tr relationship
# ============================================================
fig, ax = plt.subplots(figsize=(9, 4.5))

tr_vals = np.array([0.1, 0.2, 0.5, 1, 2, 5, 10])
bw_035 = 0.35 / tr_vals
bw_05 = 0.5 / tr_vals

ax.plot(tr_vals, bw_035, 'b-o', lw=2, markersize=8, label='BW = 0.35/Tr (仪器带宽)')
ax.plot(tr_vals, bw_05, 'r-s', lw=2, markersize=8, label='BW = 0.5/Tr (SI设计)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('上升时间 Tr (ns)', fontsize=12)
ax.set_ylabel('带宽 BW (GHz)', fontsize=12)
ax.set_title('信号带宽与上升时间的关系', fontweight='bold', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, which='both')

# Region annotations
ax.fill_between(tr_vals, bw_05, bw_035, alpha=0.1, color=ORANGE)
ax.text(0.15, 0.8, 'SI 设计裕度区域', fontsize=9, color=ORANGE, rotation=25)

# Real-world examples
examples = [
    (10, 0.05, '74HC 老式逻辑\nTr=10ns → BW=50MHz', GREEN),
    (0.5, 1.0, '74LVC 高速逻辑\nTr=1ns → BW=500MHz', ORANGE),
    (0.08, 6.0, 'DDR4 数据\nTr=0.1ns → BW=5GHz', RED),
]
ex_tr = [0.08, 0.5, 10]
for tr, bw, label, c in examples:
    ax.annotate(label, xy=(tr, bw), fontsize=8, color=c, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor=c))

# Add regions
ax.axvspan(0.06, 0.3, alpha=0.05, color=RED)
ax.text(0.09, 12, '高速\n必须控阻抗', fontsize=9, color=RED, fontweight='bold')

ax.axvspan(0.3, 2, alpha=0.05, color=ORANGE)
ax.text(0.6, 12, '中速\n看走线长度定', fontsize=9, color=ORANGE, fontweight='bold')

ax.axvspan(2, 15, alpha=0.05, color=GREEN)
ax.text(5, 12, '低速\n基本不管', fontsize=9, color=GREEN, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/02-bandwidth-vs-tr.png')
plt.close()

# ============================================================
# 3. Practical workflow
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

# Step 1
ax1 = axes[0]
ax1.set_xlim(0, 5)
ax1.set_ylim(0, 5)
ax1.axis('off')
step1 = patches.FancyBboxPatch((0.5, 1.5), 4, 2, boxstyle='round,pad=0.15',
                                facecolor=BLUE, alpha=0.8, edgecolor=DARK, lw=2)
ax1.add_patch(step1)
ax1.text(2.5, 3, '[1] 示波器量 Tr', ha='center', fontsize=13, color='white', fontweight='bold')
ax1.text(2.5, 2, '例: Tr = 1ns', ha='center', fontsize=10, color='white')

# Step 2
ax2 = axes[1]
ax2.set_xlim(0, 5)
ax2.set_ylim(0, 5)
ax2.axis('off')
step2 = patches.FancyBboxPatch((0.5, 1.5), 4, 2, boxstyle='round,pad=0.15',
                                facecolor=ORANGE, alpha=0.8, edgecolor=DARK, lw=2)
ax2.add_patch(step2)
ax2.text(2.5, 3, '[2] 算带宽', ha='center', fontsize=13, color='white', fontweight='bold')
ax2.text(2.5, 2, 'BW = 0.5/1ns\n= 500MHz', ha='center', fontsize=10, color='white')

# Step 3
ax3 = axes[2]
ax3.set_xlim(0, 5)
ax3.set_ylim(0, 5)
ax3.axis('off')

step3a = patches.FancyBboxPatch((0.5, 2.5), 4, 1.8, boxstyle='round,pad=0.15',
                                 facecolor=RED, alpha=0.8, edgecolor=DARK, lw=2)
ax3.add_patch(step3a)
ax3.text(2.5, 3.8, '[3] 判断', ha='center', fontsize=13, color='white', fontweight='bold')
ax3.text(2.5, 2.9, 'BW > 100MHz\n走线> 2.5cm\n→ 必须端接控阻抗', ha='center', fontsize=9, color='white')

fig.suptitle('实际工作中的三步判断法', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig(f'{OUT}/02-practical-workflow.png')
plt.close()

print(f'[OK] Generated 3 diagrams in {OUT}')
for f in sorted(os.listdir(OUT)):
    if f.startswith('02-'):
        print(f'  {f}')
