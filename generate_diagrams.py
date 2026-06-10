#!/usr/bin/env python3
"""Generate all diagrams for Day 01 SI Overview blog post."""
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
GRAY = '#616161'
DARK = '#212121'

# ============================================================
# 1. Low speed vs High speed signal
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

t = np.linspace(0, 4, 500)

# Low speed - smooth edges
lo = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 1 or (2 < ti < 3):
        lo[i] = 0
    elif 1 <= ti <= 2:
        lo[i] = (ti - 1) / 0.8  # slow rise
        if lo[i] > 3.3: lo[i] = 3.3
    elif ti >= 3:
        lo[i] = 3.3 - (ti - 3) / 0.8
        if lo[i] < 0: lo[i] = 0

ax1.plot(t, lo, 'b', lw=2)
ax1.set_title('低速信号 (Tr 大)', fontweight='bold')
ax1.set_ylabel('电压 (V)')
ax1.set_ylim(-1, 4.5)
ax1.set_xlabel('时间')
ax1.grid(alpha=0.3)
ax1.text(2, 4.0, '[OK] 边沿干净', ha='center', color=GREEN, fontweight='bold')

# High speed - ringing
hi = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 1:
        hi[i] = 0
    elif 1 <= ti <= 1.1:
        hi[i] = (ti - 1) * 33  # very fast rise
        if hi[i] > 3.3: hi[i] = 3.3
    elif 1.1 < ti <= 1.3:
        hi[i] = 3.3 + 0.8 * np.sin((ti-1.1)*50) * np.exp(-(ti-1.1)*10)
    elif 1.3 < ti <= 2.0:
        hi[i] = 3.3 + 0.1 * np.sin(ti*20) * np.exp(-(ti-1.3)*2)
    elif ti < 2.5:
        hi[i] = 3.3
    elif 2.5 <= ti <= 2.6:
        hi[i] = 3.3 - (ti-2.5) * 33
        if hi[i] < 0: hi[i] = 0
    elif 2.6 < ti <= 2.8:
        hi[i] = 0 - 0.6 * np.sin((ti-2.6)*40) * np.exp(-(ti-2.6)*8)
    else:
        hi[i] = 0.1 * np.sin(ti*15) * np.exp(-(ti-2.8)*3)

ax2.plot(t, hi, 'r', lw=1.5)
ax2.set_title('高速信号 (Tr 小)', fontweight='bold')
ax2.set_ylim(-1, 4.5)
ax2.set_xlabel('时间')
ax2.grid(alpha=0.3)
ax2.text(2, 4.0, '[NG] 振铃/过冲', ha='center', color=RED, fontweight='bold')

fig.suptitle('数字信号的质量变化', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig(f'{OUT}/01-low-vs-high-speed.png')
plt.close()

# ============================================================
# 2. SI Four Domains
# ============================================================
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Root node
root = patches.FancyBboxPatch((3.5, 6.5), 3, 1, boxstyle='round,pad=0.15',
                               facecolor=DARK, edgecolor='none')
ax.add_patch(root)
ax.text(5, 7, '信号完整性 SI', ha='center', va='center', color='white',
        fontweight='bold', fontsize=14)

# Branches
branches = [
    (0.5, 3.5, 2, 2.5, BLUE, '反射 SI', '过冲\n下冲\n振铃\n台阶'),
    (2.7, 3.5, 2, 2.5, RED, '串扰 SI', '噪声耦合\n边沿抖动'),
    (4.9, 3.5, 2, 2.5, ORANGE, '电源完整性 PI', '地弹\n同步开关噪声'),
    (7.1, 3.5, 2, 2.5, GREEN, '时序 SI', '建立时间\n保持时间\n延时'),
]

for x, y, w, h, color, title, desc in branches:
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.12',
                                  facecolor=color, edgecolor='white', alpha=0.9)
    ax.add_patch(box)
    ax.text(x+w/2, y+h-0.5, title, ha='center', va='center', fontweight='bold',
            fontsize=11, color='white')
    ax.text(x+w/2, y+h-1.5, desc, ha='center', va='center', fontsize=9, color='white')

# Lines from root to branches
for x_pos in [1.5, 3.7, 5.9, 8.1]:
    ax.plot([5, x_pos], [6.5, 6], 'gray', lw=1.5, alpha=0.6)

plt.savefig(f'{OUT}/01-si-four-domains.png')
plt.close()

# ============================================================
# 3. Same frequency, different Tr
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

t = np.linspace(0, 100, 800)

# Fast Tr = 1ns
freq = 1e7  # 10MHz
period_ns = 1e9 / freq  # 100ns
t_ns = t  # already in ns for display

fast = np.zeros_like(t)
for i in range(len(t)):
    cycle = (t_ns[i] % period_ns) / period_ns
    if cycle < 0.02:
        fast[i] = 3.3 * (cycle / 0.02)
    elif cycle < 0.5:
        fast[i] = 3.3
    elif 0.5 <= cycle < 0.52:
        fast[i] = 3.3 * (1 - (cycle - 0.5) / 0.02)
    else:
        fast[i] = 0

ax1.plot(t_ns[:200], fast[:200], 'b', lw=2)
ax1.set_title('Tr = 1ns', fontweight='bold', fontsize=13)
ax1.set_ylabel('电压 (V)')
ax1.set_ylim(-1, 5)
ax1.grid(alpha=0.3)
ax1.set_xlabel('时间 (ns)')
ax1.text(50, 4.7, '⚠ 高频分量多\nSI 问题严重', ha='center', color=RED, fontweight='bold', fontsize=10)

# Slow Tr = 20ns
slow = np.zeros_like(t)
for i in range(len(t)):
    cycle = (t_ns[i] % period_ns) / period_ns
    if cycle < 0.4:
        slow[i] = 3.3 * min(1, cycle / 0.4)
    elif cycle < 0.5:
        slow[i] = 3.3
    elif 0.5 <= cycle < 0.9:
        slow[i] = 3.3 * (1 - (cycle - 0.5) / 0.4)
    else:
        slow[i] = 0

ax2.plot(t_ns[:200], slow[:200], 'g', lw=2)
ax2.set_title('Tr = 20ns', fontweight='bold', fontsize=13)
ax2.set_ylim(-1, 5)
ax2.grid(alpha=0.3)
ax2.set_xlabel('时间 (ns)')
ax2.text(50, 4.7, '[OK] 高频分量少\nSI 基本不用管', ha='center', color=GREEN, fontweight='bold', fontsize=10)

fig.suptitle('同一频率 (10MHz)，不同上升时间', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig(f'{OUT}/01-same-freq-different-tr.png')
plt.close()

# ============================================================
# 4. SI Triangle (Quality / Cost / Area)
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5.5))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.3, 1.5)
ax.axis('off')

triangle = patches.Polygon([(0, 1.5), (-1.3, -1), (1.3, -1)],
                            facecolor='none', edgecolor=DARK, lw=2.5)
ax.add_patch(triangle)

ax.text(0, 1.65, '信号质量', ha='center', fontsize=14, fontweight='bold', color=BLUE)
ax.text(0, 1.25, '阻抗匹配\n端接', ha='center', fontsize=9, color=DARK)

ax.text(-1.65, -1.1, '成本', ha='center', fontsize=14, fontweight='bold', color=RED)
ax.text(-1.3, -1.4, '少加层\n少加器件', ha='center', fontsize=9, color=DARK)

ax.text(1.65, -1.1, '面积', ha='center', fontsize=14, fontweight='bold', color=GREEN)
ax.text(1.3, -1.4, '走线短\n器件小', ha='center', fontsize=9, color=DARK)

# Center text
ax.text(0, -0.1, '← 优化任何一角\n另外两角受损', ha='center', fontsize=10, color=DARK,
        style='italic')

# Arrow cycles
ax.annotate('', xy=(0.3, 0.4), xytext=(0.6, 0.8),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.2))
ax.annotate('', xy=(-0.8, -0.3), xytext=(-0.5, 0.5),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.2))
ax.annotate('', xy=(0.8, -0.3), xytext=(0.3, 0.6),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.2))

plt.savefig(f'{OUT}/01-si-triangle.png')
plt.close()

# ============================================================
# 5. Level trigger vs Edge trigger
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 4.5))

t = np.linspace(0, 200, 800)

# Level trigger
level_data = np.zeros_like(t)
for i in range(len(t)):
    if 20 <= t[i] < 140:
        level_data[i] = 3.3
ax1.plot(t, level_data, 'b', lw=2)
ax1.axhline(y=1.65, color=ORANGE, ls='--', lw=1.5, alpha=0.7)
ax1.fill_between(t, 0, level_data,
                 where=(level_data > 1.65),
                 alpha=0.15, color=GREEN)
ax1.text(80, 3.8, '采样窗口（整个高电平期间）', ha='center', fontsize=11,
         color=GREEN, fontweight='bold')
ax1.set_title('电平有效（如片选 CS）', fontweight='bold')
ax1.set_ylabel('电压 (V)')
ax1.set_ylim(-0.5, 4.5)
ax1.grid(alpha=0.3)
ax1.legend(['信号', '判决门限'], loc='lower right', fontsize=9)

# Edge trigger
clk = np.zeros_like(t)
for i in range(len(t)):
    cycle_pos = t[i] % 40
    if cycle_pos < 2:
        clk[i] = 3.3 * (cycle_pos / 2)
    elif cycle_pos < 20:
        clk[i] = 3.3
    elif 20 <= cycle_pos < 22:
        clk[i] = 3.3 * (1 - (cycle_pos - 20) / 2)
    else:
        clk[i] = 0

ax2.plot(t, clk, 'r', lw=2)
# Mark rising edges
for edge_t in [40, 80, 120, 160]:
    ax2.axvline(x=edge_t, color=GREEN, ls='-', lw=8, alpha=0.25)
    ax2.annotate('采样', xy=(edge_t, 3.5), ha='center', fontsize=9,
                 color=GREEN, fontweight='bold')

# Add jitter zone
for edge_t in [80]:
    ax2.fill_betweenx([-0.5, 4.5], edge_t-0.5, edge_t+0.5, alpha=0.15, color=RED)
ax2.text(80, 4.2, '抖动区域', ha='center', color=RED, fontsize=9)

ax2.set_title('边沿有效（如 SPI 时钟）', fontweight='bold')
ax2.set_ylabel('电压 (V)')
ax2.set_xlabel('时间')
ax2.set_ylim(-0.5, 4.5)
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/01-level-vs-edge.png')
plt.close()

# ============================================================
# 6. Source termination 33Ω
# ============================================================
fig, (ax_top, ax_tx, ax_rx) = plt.subplots(3, 1, figsize=(9, 5),
                                            gridspec_kw={'height_ratios': [0.8, 2, 2]})

# Top: schematic
ax_top.set_xlim(0, 10)
ax_top.set_ylim(0, 3)
ax_top.axis('off')

# Driver
driver = patches.Rectangle((0.5, 0.5), 1.5, 1.5, facecolor=BLUE, alpha=0.7,
                            edgecolor=DARK, lw=1.5)
ax_top.add_patch(driver)
ax_top.text(1.25, 1.25, '驱动端\nRout=17Ω', ha='center', va='center', fontsize=8, color='white')

# Resistor
resistor = patches.Rectangle((2.5, 0.8), 1, 1, facecolor=RED, alpha=0.7,
                              edgecolor=DARK, lw=1.5)
ax_top.add_patch(resistor)
ax_top.text(3, 1.3, '33Ω', ha='center', va='center', fontsize=10, color='white', fontweight='bold')

# T-line
line = patches.FancyBboxPatch((4, 1), 2.5, 0.6, boxstyle='round,pad=0.05',
                               facecolor=ORANGE, alpha=0.7, edgecolor=DARK, lw=1.5)
ax_top.add_patch(line)
ax_top.text(5.25, 1.3, '50Ω 传输线', ha='center', va='center', fontsize=9, color='white')

# Receiver
rx_box = patches.Rectangle((7, 0.5), 1.5, 1.5, facecolor=GREEN, alpha=0.7,
                            edgecolor=DARK, lw=1.5)
ax_top.add_patch(rx_box)
ax_top.text(7.75, 1.25, '接收端\nRin>>Z₀', ha='center', va='center', fontsize=8, color='white')

# Connection lines
ax_top.plot([2, 2.5], [1.25, 1.3], 'gray', lw=2)
ax_top.plot([3.5, 4], [1.3, 1.3], 'gray', lw=2)
ax_top.plot([6.5, 7], [1.3, 1.25], 'gray', lw=2)

# Label
ax_top.text(3, 2.5, 'Rout + R = Z₀  →  17 + 33 = 50Ω ✓', ha='center',
            fontsize=11, fontweight='bold', color=DARK,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor=GRAY))

# TX waveform
t = np.linspace(0, 12, 600)
tx = np.zeros_like(t)
for i in range(len(t)):
    if t[i] < 0.5:
        tx[i] = 0
    elif t[i] < 0.7:
        tx[i] = 1.65 * (t[i] - 0.5) / 0.2
    elif t[i] < 3:
        tx[i] = 1.65
    elif 3 <= t[i] < 3.2:
        tx[i] = 1.65 + 1.65 * (t[i] - 3) / 0.2
    else:
        tx[i] = 3.3

ax_tx.plot(t, tx, 'b', lw=2)
ax_tx.axhline(y=1.65, color=GRAY, ls='--', lw=1, alpha=0.5)
ax_tx.axhline(y=3.3, color=GRAY, ls='--', lw=1, alpha=0.5)
# Annotate step
ax_tx.annotate('台阶 (半幅度)', xy=(1.5, 1.65), xytext=(2.5, 2.2),
               arrowprops=dict(arrowstyle='->', color=RED),
               fontsize=10, color=RED, fontweight='bold')
ax_tx.annotate('满幅度', xy=(8, 3.3), xytext=(9, 3.5),
               arrowprops=dict(arrowstyle='->', color=GREEN),
               fontsize=10, color=GREEN, fontweight='bold')
ax_tx.set_title('发送端波形', fontweight='bold', fontsize=11)
ax_tx.set_ylabel('电压 (V)')
ax_tx.set_ylim(-0.5, 5)
ax_tx.grid(alpha=0.3)
ax_tx.legend(['Vtx'], loc='upper left', fontsize=9)

# RX waveform
rx = np.zeros_like(t)
for i in range(len(t)):
    if t[i] < 1.5:
        rx[i] = 0
    elif t[i] < 1.7:
        rx[i] = 3.3 * (t[i] - 1.5) / 0.2
    elif t[i] < 6:
        rx[i] = 3.3
    elif 6 <= t[i] < 6.2:
        rx[i] = 3.3 * (1 - (t[i] - 6) / 0.2)
    else:
        rx[i] = 0

ax_rx.plot(t, rx, 'g', lw=2)
ax_rx.axhline(y=3.3, color=GRAY, ls='--', lw=1, alpha=0.5)
ax_rx.annotate('干净满幅度', xy=(3.5, 3.3), xytext=(5, 3.8),
               arrowprops=dict(arrowstyle='->', color=GREEN),
               fontsize=10, color=GREEN, fontweight='bold')
ax_rx.set_title('接收端波形', fontweight='bold', fontsize=11)
ax_rx.set_ylabel('电压 (V)')
ax_rx.set_xlabel('时间')
ax_rx.set_ylim(-0.5, 5)
ax_rx.grid(alpha=0.3)
ax_rx.legend(['Vrx'], loc='upper left', fontsize=9)

plt.tight_layout()
plt.savefig(f'{OUT}/01-source-termination.png')
plt.close()

# ============================================================
# 7. 3W Spacing
# ============================================================
fig, ax = plt.subplots(figsize=(8, 2.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4)
ax.axis('off')

# Trace 1
t1 = patches.Rectangle((1, 1.5), 0.8, 1, facecolor=BLUE, alpha=0.8, edgecolor=DARK, lw=2)
ax.add_patch(t1)
ax.text(1.4, 2, '攻击线', ha='center', va='center', fontsize=9, color='white', fontweight='bold')

# Trace 2
t2 = patches.Rectangle((4.6, 1.5), 0.8, 1, facecolor=RED, alpha=0.6, edgecolor=DARK, lw=2)
ax.add_patch(t2)
ax.text(5, 2, '受害线', ha='center', va='center', fontsize=9, color='white', fontweight='bold')

# W markers
ax.annotate('', xy=(1, 1.2), xytext=(1.8, 1.2),
            arrowprops=dict(arrowstyle='<->', color=DARK, lw=1.5))
ax.text(1.4, 0.8, 'W', ha='center', fontsize=10, fontweight='bold')

# Distance marker
ax.annotate('', xy=(1.8, 1.2), xytext=(4.6, 1.2),
            arrowprops=dict(arrowstyle='<->', color=DARK, lw=2))
ax.text(3.2, 0.8, '3W（中心间距）', ha='center', fontsize=10, fontweight='bold', color=BLUE)

# Air gap
ax.annotate('', xy=(1.8, 3.2), xytext=(4.6, 3.2),
            arrowprops=dict(arrowstyle='<->', color=GREEN, lw=1.5))
ax.text(3.2, 3.5, '空气间隙 = 2W', ha='center', fontsize=10, fontweight='bold', color=GREEN)

# Coupling arrows
ax.annotate('', xy=(3.5, 2.5), xytext=(2.9, 2.5),
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2, ls='--'))
ax.annotate('', xy=(2.9, 1.5), xytext=(3.5, 1.5),
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.2, ls='--'))
ax.text(3.2, 2.8, '串扰耦合', ha='center', fontsize=8, color=RED)

# Bars on right
for idx, (label, val, color_bar) in enumerate([
    ('1W', 30, RED), ('2W', 12, ORANGE), ('3W', 4, GREEN)
]):
    y = 3.8 - idx * 0.9
    ax.barh(y, val/3, left=8, height=0.35, color=color_bar, alpha=0.7)
    ax.text(7.7, y, label, ha='right', va='center', fontsize=9, fontweight='bold')
    ax.text(8 + val/3 + 0.1, y, f'~{val}%', va='center', fontsize=9)

ax.text(9.5, 4.2, '串扰量级', ha='center', fontsize=10, fontweight='bold')
ax.set_xlim(0, 12)

plt.tight_layout()
plt.savefig(f'{OUT}/01-3w-spacing.png')
plt.close()

# ============================================================
# 8. 20H Principle
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

# Left: without 20H (edges flush)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 5)
ax1.axis('off')

# Power plane
pwr1 = patches.Rectangle((0.5, 3.5), 9, 0.6, facecolor=RED, alpha=0.6, edgecolor=DARK, lw=1.5)
ax1.add_patch(pwr1)
ax1.text(5, 3.8, '电源平面', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# GND plane
gnd1 = patches.Rectangle((0.5, 2.5), 9, 0.6, facecolor=DARK, alpha=0.8, edgecolor=DARK, lw=1.5)
ax1.add_patch(gnd1)
ax1.text(5, 2.8, '地平面', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# E-field leak
for x_pos in [9.5, 9.8, 10.2, 10.6]:
    ax1.plot([9.5, x_pos], [3.5, 4.5], 'r-', lw=1, alpha=0.5)
    ax1.plot([9.5, x_pos], [2.5, 1.5], 'r-', lw=1, alpha=0.5)

ax1.text(10.2, 4.5, 'EMI\n泄漏', ha='center', fontsize=9, color=RED, fontweight='bold')
ax1.text(10.2, 1.2, 'EMI\n泄漏', ha='center', fontsize=9, color=RED, fontweight='bold')
ax1.set_title('内缩前：边缘齐平', fontweight='bold', fontsize=12, color=RED)

# Right: with 20H
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 5)
ax2.axis('off')

# Power plane (indented)
pwr_h = 0.6
pwr_y = 3.5
margin = 2
pwr2 = patches.Rectangle((0.5 + margin, pwr_y), 9 - 2*margin, pwr_h,
                          facecolor=RED, alpha=0.6, edgecolor=DARK, lw=1.5)
ax2.add_patch(pwr2)
ax2.text(5, 3.8, '电源平面（内缩）', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# GND plane (full width)
gnd2 = patches.Rectangle((0.5, 2.5), 9, 0.6, facecolor=DARK, alpha=0.8, edgecolor=DARK, lw=1.5)
ax2.add_patch(gnd2)
ax2.text(5, 2.8, '地平面', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# H marker
ax2.annotate('', xy=(4.5, 2.5), xytext=(4.5, 3.5),
            arrowprops=dict(arrowstyle='<->', color=DARK, lw=2))
ax2.text(3.8, 3, 'H', ha='right', fontsize=11, fontweight='bold')

# 20H markers
ax2.annotate('', xy=(0.5, 4.3), xytext=(0.5 + margin, 4.3),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=2))
ax2.text(0.5 + margin/2, 4.6, '20H', ha='center', fontsize=11, fontweight='bold', color=BLUE)

ax2.annotate('', xy=(9.5 - margin, 4.3), xytext=(9.5, 4.3),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=2))
ax2.text(9.5 - margin/2, 4.6, '20H', ha='center', fontsize=11, fontweight='bold', color=BLUE)

# Field contained
ax2.text(9.5, 4.5, '边缘场\n被包住', ha='center', fontsize=9, color=GREEN, fontweight='bold')
ax2.text(9.5, 1.2, 'EMI↓70%', ha='center', fontsize=9, color=GREEN, fontweight='bold')
ax2.set_title('内缩后：20H', fontweight='bold', fontsize=12, color=GREEN)

plt.tight_layout()
plt.savefig(f'{OUT}/01-20h-principle.png')
plt.close()

# ============================================================
# 9. Microstrip vs Stripline
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

# Microstrip
ax1.set_xlim(0, 8)
ax1.set_ylim(0, 6)
ax1.axis('off')

# Air
air = patches.Rectangle((0, 4), 8, 2, facecolor='lightblue', alpha=0.3)
ax1.add_patch(air)
ax1.text(4, 5.5, '空气 (Dk≈1)', ha='center', fontsize=10, color=DARK)

# Trace
trace1 = patches.Rectangle((3, 3.5), 2, 0.5, facecolor=BLUE, alpha=0.8, edgecolor=DARK, lw=2)
ax1.add_patch(trace1)
ax1.text(4, 3.75, '信号线', ha='center', fontsize=10, color='white', fontweight='bold')

# Substrate
sub1 = patches.Rectangle((0, 2), 8, 1.5, facecolor=ORANGE, alpha=0.4)
ax1.add_patch(sub1)
ax1.text(4, 2.75, 'FR4 板材 (Dk≈4)', ha='center', fontsize=10, color=DARK)

# Reference plane
ref1 = patches.Rectangle((0, 1), 8, 1, facecolor=DARK, alpha=0.8)
ax1.add_patch(ref1)
ax1.text(4, 1.5, '参考平面', ha='center', fontsize=10, color='white', fontweight='bold')

ax1.set_title('表层走线（微带线）', fontweight='bold', fontsize=12)
ax1.text(4, 0.3, '介质不均匀 → 远端串扰大', ha='center', fontsize=10, color=RED, fontweight='bold')

# Stripline
ax2.set_xlim(0, 8)
ax2.set_ylim(0, 6)
ax2.axis('off')

# Top ref
top_ref = patches.Rectangle((0, 4.5), 8, 1, facecolor=DARK, alpha=0.8)
ax2.add_patch(top_ref)
ax2.text(4, 5, '参考平面（上）', ha='center', fontsize=10, color='white', fontweight='bold')

# Substrate top
sub2_top = patches.Rectangle((0, 3.5), 8, 1, facecolor=ORANGE, alpha=0.4)
ax2.add_patch(sub2_top)

# Trace
trace2 = patches.Rectangle((3, 3.3), 2, 0.4, facecolor=BLUE, alpha=0.8, edgecolor=DARK, lw=2)
ax2.add_patch(trace2)
ax2.text(4, 3.5, '信号线', ha='center', fontsize=10, color='white', fontweight='bold')

# Substrate bottom
sub2_bot = patches.Rectangle((0, 2), 8, 1.3, facecolor=ORANGE, alpha=0.4)
ax2.add_patch(sub2_bot)
ax2.text(4, 2.65, 'FR4 板材 (Dk≈4)', ha='center', fontsize=10, color=DARK)

# Bottom ref
bot_ref = patches.Rectangle((0, 1), 8, 1, facecolor=DARK, alpha=0.8)
ax2.add_patch(bot_ref)
ax2.text(4, 1.5, '参考平面（下）', ha='center', fontsize=10, color='white', fontweight='bold')

ax2.set_title('内层走线（带状线）', fontweight='bold', fontsize=12)
ax2.text(4, 0.3, '介质均匀 → 远端串扰 ≈ 0', ha='center', fontsize=10, color=GREEN, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/01-microstrip-vs-stripline.png')
plt.close()

# ============================================================
# 10. Ground partition comparison
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))

# Wrong: split ground
ax1.set_xlim(0, 8)
ax1.set_ylim(0, 5.5)
ax1.axis('off')
ax1.set_title('错误：切地', fontweight='bold', fontsize=12, color=RED)

# Ground planes
g1 = patches.Rectangle((0.5, 1), 3, 2, facecolor=DARK, alpha=0.6, edgecolor=DARK, lw=2)
ax1.add_patch(g1)
ax1.text(2, 2, '数字地', ha='center', fontsize=10, color='white', fontweight='bold')

g2 = patches.Rectangle((4.5, 1), 3, 2, facecolor=DARK, alpha=0.4, edgecolor=DARK, lw=2)
ax1.add_patch(g2)
ax1.text(6, 2, '模拟地', ha='center', fontsize=10, color='white', fontweight='bold')

# Digital chip
d_chip = patches.Rectangle((1, 4), 1.5, 1, facecolor=BLUE, alpha=0.7, edgecolor=DARK, lw=1.5)
ax1.add_patch(d_chip)
ax1.text(1.75, 4.5, '数字', ha='center', fontsize=9, color='white', fontweight='bold')

# Analog chip
a_chip = patches.Rectangle((5.5, 4), 1.5, 1, facecolor=GREEN, alpha=0.7, edgecolor=DARK, lw=1.5)
ax1.add_patch(a_chip)
ax1.text(6.25, 4.5, '模拟', ha='center', fontsize=9, color='white', fontweight='bold')

# Signal crossing split
ax1.plot([1.75, 6], [4, 3], 'r-', lw=2, ls='--')
ax1.plot([6, 6.25], [3, 4], 'r-', lw=2, ls='--')
ax1.text(4, 3.2, '信号跨分割槽！', ha='center', fontsize=9, color=RED, fontweight='bold')

# Return current blocked
ax1.plot([4, 1.75], [1.5, 1.5], 'r-', lw=2, ls=':', alpha=0.7)
ax1.text(2.5, 0.5, '[NG] 返回电流无路可走', ha='center', fontsize=9, color=RED, fontweight='bold')

# Right: unified ground
ax2.set_xlim(0, 8)
ax2.set_ylim(0, 5.5)
ax2.axis('off')
ax2.set_title('正确：统一地层 + 布局分区', fontweight='bold', fontsize=12, color=GREEN)

# Unified ground
ug = patches.Rectangle((0.5, 1), 7, 2, facecolor=DARK, alpha=0.6, edgecolor=DARK, lw=2)
ax2.add_patch(ug)
ax2.text(4, 2, '统一地平面', ha='center', fontsize=10, color='white', fontweight='bold')

# Digital chip
d2 = patches.Rectangle((1, 4), 1.5, 1, facecolor=BLUE, alpha=0.7, edgecolor=DARK, lw=1.5)
ax2.add_patch(d2)
ax2.text(1.75, 4.5, '数字', ha='center', fontsize=9, color='white', fontweight='bold')

# Analog chip
a2 = patches.Rectangle((5.5, 4), 1.5, 1, facecolor=GREEN, alpha=0.7, edgecolor=DARK, lw=1.5)
ax2.add_patch(a2)
ax2.text(6.25, 4.5, '模拟', ha='center', fontsize=9, color='white', fontweight='bold')

# Isolation barrier
barrier = patches.Rectangle((3.5, 1), 1, 3.5, facecolor='white', alpha=0.3,
                             edgecolor=GRAY, lw=1, ls='--')
ax2.add_patch(barrier)
ax2.text(4, 3.5, '布局\n隔离', ha='center', fontsize=8, color=GRAY)

# Return current paths
ax2.plot([1.75, 4], [4, 2.5], 'g-', lw=1.5, alpha=0.6)
ax2.plot([6.25, 4], [4, 2.5], 'g-', lw=1.5, alpha=0.6)
ax2.text(2.5, 0.5, '[OK] 返回路径完整', ha='center', fontsize=9, color=GREEN, fontweight='bold')
ax2.text(6, 0.5, '[OK] 返回路径完整', ha='center', fontsize=9, color=GREEN, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/01-ground-partition.png')
plt.close()

# ============================================================
# 11. Tr → SI chain (vertical flowchart)
# ============================================================
fig, ax = plt.subplots(figsize=(7, 5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

boxes = [
    (3.5, 8.5, 3, 1, RED, '芯片工艺进步\n(28nm→14nm→7nm)'),
    (3.5, 7, 3, 1, ORANGE, '晶体管沟道缩短'),
    (3.5, 5.5, 3, 1, ORANGE, '开关时间缩短'),
    (3.5, 4, 3, 1, RED, '★ 上升时间 Tr 减小', True),
    (3.5, 2.5, 3, 1, BLUE, '高频分量增多'),
    (3.5, 1, 3, 1, BLUE, 'PCB 寄生效应暴露\n→ 波形畸变 → SI 问题'),
]

for x, y, w, h, color, label, *bold in boxes:
    is_bold = bold and bold[0]
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.12',
                                  facecolor=color, edgecolor='white',
                                  alpha=0.85 if is_bold else 0.7,
                                  lw=2.5 if is_bold else 1.5)
    ax.add_patch(box)
    ax.text(x+w/2, y+h/2, label, ha='center', va='center',
            color='white', fontweight='bold', fontsize=11 if is_bold else 10)

# Down arrows between boxes
for i in range(len(boxes) - 1):
    ax.annotate('', xy=(5, boxes[i][1] - 0.05),
                xytext=(5, boxes[i+1][1] + boxes[i+1][3] + 0.05),
                arrowprops=dict(arrowstyle='->', color=DARK, lw=2.5))

# Side annotation
ax.annotate('核心\n根源', xy=(7, 4.5), fontsize=11, color=RED, fontweight='bold',
            ha='center')

plt.savefig(f'{OUT}/01-tr-chain.png')
plt.close()

print(f'✅ Generated {len(os.listdir(OUT))} diagrams in {OUT}')
for f in sorted(os.listdir(OUT)):
    print(f'  {f}')
