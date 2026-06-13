#!/usr/bin/env python3
"""Generate diagrams for Day 03 - Transmission Line Theory."""
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
CYAN = '#00BCD4'

# ============================================================
# 1. Critical Length - When trace becomes transmission line
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Left: short trace = lumped
t = np.linspace(0, 4, 500)
ax = axes[0]
# Input and output signals on short trace (in-phase)
vin = np.zeros_like(t)
vout = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 0.5:
        vin[i] = 0
        vout[i] = 0
    elif ti < 1.2:
        vin[i] = 3.3 * (ti - 0.5) / 0.7
        vout[i] = 3.3 * (ti - 0.5) / 0.7
    elif ti < 2.0:
        vin[i] = 3.3
        vout[i] = 3.3
    elif ti < 2.7:
        vin[i] = 3.3 * (1 - (ti - 2.0) / 0.7)
        vout[i] = 3.3 * (1 - (ti - 2.0) / 0.7)
    else:
        vin[i] = 0
        vout[i] = 0

ax.plot(t, vin, BLUE, lw=2, label='输入端')
ax.plot(t, vout, RED, lw=2, ls='--', label='输出端')
ax.set_title('走线很短：集总模型', fontweight='bold', fontsize=13)
ax.set_ylabel('电压 (V)')
ax.set_ylim(-1, 4.5)
ax.legend(loc='upper right', fontsize=9)
ax.grid(alpha=0.3)
ax.text(2, 4.0, 'L < λ/10\n输入 ≈ 输出', ha='center', color=GREEN, fontweight='bold', fontsize=10)

# Right: long trace = transmission line
ax = axes[1]
vin2 = np.zeros_like(t)
vout2 = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti < 0.5:
        vin2[i] = 0; vout2[i] = 0
    elif ti < 1.2:
        vin2[i] = 3.3 * (ti - 0.5) / 0.7
        vout2[i] = 0  # delay
    elif ti < 1.5:
        vin2[i] = 3.3
        vout2[i] = 0
    elif ti < 2.2:
        vin2[i] = 3.3
        vout2[i] = 3.3 * (ti - 1.5) / 0.7  # delayed arrival
    elif ti < 2.7:
        vin2[i] = 3.3 * (1 - (ti - 2.2) / 0.5)
        vout2[i] = 3.3
    elif ti < 3.2:
        vin2[i] = 0
        vout2[i] = 3.3 * (1 - (ti - 2.7) / 0.5)
    else:
        vin2[i] = 0; vout2[i] = 0

ax.plot(t, vin2, BLUE, lw=2, label='输入端')
ax.plot(t, vout2, RED, lw=2, ls='--', label='输出端')
ax.set_title('走线很长：传输线模型', fontweight='bold', fontsize=13)
ax.set_ylabel('电压 (V)')
ax.set_ylim(-1, 4.5)
ax.legend(loc='upper right', fontsize=9)
ax.grid(alpha=0.3)
# arrow showing delay
ax.annotate('', xy=(1.85, 3.3), xytext=(1.35, 3.3),
            arrowprops=dict(arrowstyle='<->', color=RED, lw=1.5))
ax.text(1.6, 3.6, '传播延迟', ha='center', color=RED, fontsize=9, fontweight='bold')
ax.text(2, 4.0, 'L > λ/6\n延迟不可忽略', ha='center', color=RED, fontweight='bold', fontsize=10)

plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-critical-length.png'))
plt.close()

# ============================================================
# 2. RLCG transmission line model
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))

# Draw RLCG model as a chain of T-sections
n_sections = 5
x_start = 0.5
section_width = 1.7

for i in range(n_sections):
    x = x_start + i * section_width
    
    # Series R and L (horizontal top)
    ax.plot([x, x + 0.4], [4, 4], 'k-', lw=2)
    # R box
    rect_r = patches.FancyBboxPatch((x + 0.05, 3.65), 0.3, 0.7, boxstyle="round,pad=0.1",
                                     facecolor=RED, alpha=0.3, edgecolor=RED, lw=1.2)
    ax.add_patch(rect_r)
    ax.text(x + 0.2, 4, 'RΔz', ha='center', va='center', fontsize=8, fontweight='bold')
    # L coil
    x_l = x + 0.5
    lx = np.linspace(0, 0.5, 30)
    ly = 4 + 0.3 * np.sin(lx * 4 * np.pi)
    ax.plot(x_l + lx, ly, BLUE, lw=1.5)
    ax.text(x_l + 0.25, 3.4, 'LΔz', ha='center', fontsize=8, fontweight='bold', color=BLUE)
    
    # Shunt C and G (vertical to ground)
    # C
    c_x = x + 0.85
    c_y_top = 4
    c_y_bot = 1.5
    ax.plot([c_x, c_x], [c_y_top, c_y_top - 0.5], 'k-', lw=1.5)
    # C plates
    rect_c1 = patches.Rectangle((c_x - 0.25, c_y_top - 0.7), 0.5, 0.15,
                                 facecolor=GREEN, alpha=0.5, edgecolor=GREEN, lw=1.2)
    rect_c2 = patches.Rectangle((c_x - 0.25, c_y_top - 1.05), 0.5, 0.15,
                                 facecolor=GREEN, alpha=0.5, edgecolor=GREEN, lw=1.2)
    ax.add_patch(rect_c1)
    ax.add_patch(rect_c2)
    ax.text(c_x + 0.45, c_y_top - 0.9, 'CΔz', fontsize=8, fontweight='bold', color=GREEN)
    # G
    ax.plot([c_x, c_x], [c_y_top - 1.2, c_y_bot], 'k-', lw=1.5)
    rect_g = patches.FancyBboxPatch((c_x - 0.2, c_y_bot - 0.25), 0.4, 0.5, boxstyle="round,pad=0.1",
                                     facecolor=ORANGE, alpha=0.3, edgecolor=ORANGE, lw=1.2)
    ax.add_patch(rect_g)
    ax.text(c_x + 0.45, c_y_bot, 'GΔz', fontsize=8, fontweight='bold', color=ORANGE)
    
    # Ground line
    ax.plot([x, x + section_width], [c_y_bot, c_y_bot], 'k-', lw=2)
    ax.plot([x, x + section_width], [0.5, 0.5], 'k-', lw=2)
    # Ground symbol
    ax.plot([x + section_width/2 - 0.3, x + section_width/2 + 0.3], [0.5, 0.5], 'k-', lw=2)
    ax.plot([x + section_width/2 - 0.15, x + section_width/2 + 0.15], [0.3, 0.3], 'k-', lw=1.5)
    ax.plot([x + section_width/2, x + section_width/2], [0.15, 0.3], 'k-', lw=1)

# Top horizontal wire between sections
ax.plot([x_start, x_start + n_sections * section_width], [4, 4], 'k-', lw=2)

# Labels
ax.text(0.5, 4.8, '信号路径', ha='center', fontsize=11, fontweight='bold')
ax.text(0.5, 0, '参考地平面', ha='center', fontsize=11, fontweight='bold')

# Title box at bottom
ax.text(5.5, 5.3, '传输线 RLCG 分布参数模型', ha='center', fontsize=14, fontweight='bold')
ax.text(5.5, 4.9, '每单位长度 Δz 的等效电路。实际的传输线是无穷多个这样的单元级联。', 
        ha='center', fontsize=10, color=GRAY)

ax.set_xlim(0, 11)
ax.set_ylim(-0.5, 6)
ax.axis('off')
plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-rlcg-model.png'))
plt.close()

# ============================================================
# 3. Signal propagation step by step
# ============================================================
fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))

phases = ['① 信号发射', '② 沿走线传播', '③ 到达末端', '④ 负载响应']
for idx, (ax, phase) in enumerate(zip(axes, phases)):
    # Draw transmission line
    ax.plot([0.5, 9.5], [4, 4], 'k-', lw=3)
    ax.plot([0.5, 9.5], [1, 1], 'k-', lw=3)
    
    # Driver (source)
    ax.plot([1.5, 1.5], [2, 4], 'b-', lw=2)
    rect_drv = patches.Rectangle((0.8, 2.5), 1.4, 0.8, facecolor=BLUE, alpha=0.3, edgecolor=BLUE)
    ax.add_patch(rect_drv)
    ax.text(1.5, 2.9, '驱动', ha='center', fontsize=9, fontweight='bold')
    
    # Load
    ax.plot([8.5, 8.5], [2, 4], 'r-', lw=2)
    rect_load = patches.Rectangle((7.8, 2.5), 1.4, 0.8, facecolor=RED, alpha=0.3, edgecolor=RED)
    ax.add_patch(rect_load)
    ax.text(8.5, 2.9, '负载', ha='center', fontsize=9, fontweight='bold')
    
    # Signal pulse
    if idx == 0:
        pulse_x = 2.0
        ax.annotate('V₀', xy=(pulse_x, 4.5), fontsize=11, fontweight='bold', 
                    color=BLUE, ha='center')
        circle = patches.Circle((pulse_x, 4), 0.35, facecolor=BLUE, alpha=0.6)
        ax.add_patch(circle)
        ax.annotate('', xy=(pulse_x + 0.5, 4), xytext=(pulse_x + 0.2, 4),
                   arrowprops=dict(arrowstyle='->', color=BLUE, lw=2))
        
    elif idx == 1:
        pulse_x = 5.0
        circle = patches.Circle((pulse_x, 4), 0.35, facecolor=BLUE, alpha=0.6)
        ax.add_patch(circle)
        ax.annotate('', xy=(pulse_x + 0.8, 4), xytext=(pulse_x + 0.2, 4),
                   arrowprops=dict(arrowstyle='->', color=BLUE, lw=2))
        ax.text(pulse_x, 4.7, 'v = 1/√(LC)', ha='center', fontsize=9, color=BLUE, fontweight='bold')
        
    elif idx == 2:
        pulse_x = 8.5
        circle = patches.Circle((pulse_x, 4), 0.35, facecolor=BLUE, alpha=0.6)
        ax.add_patch(circle)
        ax.text(pulse_x, 4.7, '到达!', ha='center', fontsize=9, color=RED, fontweight='bold')
        
    elif idx == 3:
        # Reflection
        pulse_x = 8.5
        circle_fwd = patches.Circle((pulse_x, 4), 0.35, facecolor=BLUE, alpha=0.4)
        ax.add_patch(circle_fwd)
        circle_ref = patches.Circle((7.8, 4), 0.28, facecolor=RED, alpha=0.5)
        ax.add_patch(circle_ref)
        ax.annotate('反射波', xy=(7.5, 4.5), fontsize=9, color=RED, fontweight='bold')
        ax.annotate('', xy=(7.0, 4), xytext=(7.6, 4),
                   arrowprops=dict(arrowstyle='->', color=RED, lw=1.5, ls='--'))
        ax.annotate('入射波', xy=(9.0, 4.5), fontsize=9, color=BLUE, fontweight='bold')
    
    ax.set_title(phase, fontweight='bold', fontsize=10)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

plt.suptitle('信号在传输线上的传播过程', fontweight='bold', fontsize=13, y=1.02)
plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-signal-propagation.png'))
plt.close()

# ============================================================
# 4. Bounce diagram (reflection lattice diagram)
# ============================================================
fig, ax = plt.subplots(figsize=(9, 6))

# Transmission line - horizontal axis = distance, vertical = time
# Source at x=0, Load at x=L
L = 8
Td = 1  # one-way delay

# Draw the transmission line zone
ax.fill_between([0, L], 0, 6, color='lightyellow', alpha=0.3)

# Voltage levels and reflection coefficients
Z0 = 50
Rs = 25  # source impedance
ZL = 200  # load impedance (mismatched for illustration)
Vin = 3.3

# Reflection coefficients
Gamma_S = (Rs - Z0) / (Rs + Z0)  # ≈ -0.333
Gamma_L = (ZL - Z0) / (ZL + Z0)  # ≈ 0.6

# Initial voltage on line
V_init = Vin * Z0 / (Z0 + Rs)  # ≈ 2.2V

# Build bounce diagram
times = []
positions = []
voltages = []
labels = []

# Incident wave
times.append([0, Td])
positions.append([0, L])
voltages.append(V_init)
labels.append(f'V₁⁺ = {V_init:.2f}V')

# First reflection at load
V_refl1 = V_init * Gamma_L
times.append([Td, 2*Td])
positions.append([L, 0])
voltages.append(V_refl1)
labels.append(f'V₁⁻ = {V_refl1:.2f}V (Γ_L={Gamma_L:.2f})')

# Second reflection at source
V_refl2 = V_refl1 * Gamma_S
times.append([2*Td, 3*Td])
positions.append([0, L])
voltages.append(V_refl2)
labels.append(f'V₂⁺ = {V_refl2:.2f}V (Γ_S={Gamma_S:.2f})')

# Third reflection
V_refl3 = V_refl2 * Gamma_L
times.append([3*Td, 4*Td])
positions.append([L, 0])
voltages.append(V_refl3)
labels.append(f'V₂⁻ = {V_refl3:.2f}V')

# Draw arrows
colors_wave = [BLUE, RED, GREEN, ORANGE]
for i, (t, p, v) in enumerate(zip(times, positions, voltages)):
    ax.annotate('', xy=(p[1], t[1]), xytext=(p[0], t[0]),
               arrowprops=dict(arrowstyle='->', color=colors_wave[i], lw=1.8,
                              connectionstyle='arc3,rad=0'))
    # Label midpoint
    mx = (p[0] + p[1]) / 2
    my = (t[0] + t[1]) / 2 - 0.1
    if i % 2 == 0:
        ax.text(mx, my, labels[i], fontsize=8, color=colors_wave[i], ha='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    else:
        ax.text(mx, my + 0.2, labels[i], fontsize=8, color=colors_wave[i], ha='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

# Source and load markers
ax.axvline(x=0, color=BLUE, lw=2, ls='--', alpha=0.5)
ax.axvline(x=L, color=RED, lw=2, ls='--', alpha=0.5)
ax.text(-0.3, 0.8, '源端\nRs=25Ω', fontsize=9, color=BLUE, ha='center', fontweight='bold')
ax.text(L + 0.3, 0.8, '负载端\nZL=200Ω', fontsize=9, color=RED, ha='center', fontweight='bold')

ax.set_xlabel('距离 (源端 → 负载端)', fontsize=11)
ax.set_ylabel('时间 (Td = 单向延迟)', fontsize=11)
ax.set_title('反射图（Bounce / Lattice Diagram）', fontweight='bold', fontsize=13)
ax.set_xlim(-1, L + 1)
ax.set_ylim(6.5, -0.5)
ax.grid(alpha=0.3)

# Annotation
ax.text(L/2, 5.5, '每经过 2Td（往返一次）\n反射波幅度递减\n最终趋于稳态', 
        ha='center', fontsize=9, color=DARK, fontstyle='italic',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-bounce-diagram.png'))
plt.close()

# ============================================================
# 5. Four termination types comparison
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(11, 7))

# --- Source series ---
ax = axes[0, 0]
x_wire = np.linspace(0.5, 9.5, 20)
ax.plot(x_wire, [3.5]*20, 'k-', lw=2)
ax.plot(x_wire, [0.5]*20, 'k-', lw=2)
# Driver
rect_d = patches.Rectangle((0.3, 1.0), 1.2, 2.0, facecolor=BLUE, alpha=0.2, edgecolor=BLUE)
ax.add_patch(rect_d)
ax.text(0.9, 2.0, '驱动', ha='center', fontsize=9, fontweight='bold')
# Series resistor
rect_r = patches.Rectangle((1.8, 3.0), 0.8, 1.0, facecolor=ORANGE, alpha=0.5, edgecolor=ORANGE, lw=1.5)
ax.add_patch(rect_r)
ax.text(2.2, 3.5, 'Rs', ha='center', fontsize=10, fontweight='bold')
# Connect
ax.plot([1.5, 1.8], [3.5, 3.5], 'k-', lw=1.5)
ax.plot([2.6, x_wire[0]], [3.5, 3.5], 'k-', lw=1.5)
# Load
ax.plot([8.5, 8.5], [1.0, 3.5], 'r-', lw=2)
rect_l = patches.Rectangle((7.8, 1.0), 1.4, 2.0, facecolor=RED, alpha=0.2, edgecolor=RED)
ax.add_patch(rect_l)
ax.text(8.5, 2.0, '负载\n高阻', ha='center', fontsize=9, fontweight='bold')
ax.text(1.5, 4.2, 'Rs + Rout = Z₀', fontsize=8, color=ORANGE, fontweight='bold')
ax.set_title('① 源端串联匹配', fontweight='bold', fontsize=11, color=ORANGE)
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

# --- Parallel/load termination ---
ax = axes[0, 1]
x_wire2 = np.linspace(0.5, 8.0, 15)
ax.plot(x_wire2, [3.5]*15, 'k-', lw=2)
ax.plot(x_wire2, [0.5]*15, 'k-', lw=2)
# Driver
rect_d2 = patches.Rectangle((0.3, 1.0), 1.2, 2.0, facecolor=BLUE, alpha=0.2, edgecolor=BLUE)
ax.add_patch(rect_d2)
ax.text(0.9, 2.0, '驱动', ha='center', fontsize=9, fontweight='bold')
ax.plot([1.5, x_wire2[0]], [3.5, 3.5], 'k-', lw=1.5)
# Load with parallel resistor
ax.plot([8.5, 8.5], [1.0, 3.5], 'r-', lw=2)
rect_l2 = patches.Rectangle((7.8, 1.5), 1.4, 1.5, facecolor=RED, alpha=0.2, edgecolor=RED)
ax.add_patch(rect_l2)
ax.text(8.5, 2.2, '负载', ha='center', fontsize=9, fontweight='bold')
# Parallel resistor to gnd
rect_r2 = patches.Rectangle((8.3, 1.0), 0.4, 0.5, facecolor=GREEN, alpha=0.6, edgecolor=GREEN, lw=1.5)
ax.add_patch(rect_r2)
ax.plot([8.5, 8.5], [1.5, 1.5], 'k-', lw=1.5)
ax.plot([8.5, 8.5], [1.0, 0.5], 'k-', lw=1.5)
ax.text(9.3, 1.2, 'Rt = Z₀', fontsize=9, color=GREEN, fontweight='bold')
ax.text(5, 4.3, '⚠ 直流功耗大 P = V²/Z₀', fontsize=8, color=RED, fontweight='bold')
ax.set_title('② 末端并联匹配', fontweight='bold', fontsize=11, color=GREEN)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5)
ax.axis('off')

# --- Thevenin termination ---
ax = axes[1, 0]
x_wire3 = np.linspace(0.5, 8.0, 15)
ax.plot(x_wire3, [3.5]*15, 'k-', lw=2)
ax.plot(x_wire3, [0.5]*15, 'k-', lw=2)
rect_d3 = patches.Rectangle((0.3, 1.0), 1.2, 2.0, facecolor=BLUE, alpha=0.2, edgecolor=BLUE)
ax.add_patch(rect_d3)
ax.text(0.9, 2.0, '驱动', ha='center', fontsize=9, fontweight='bold')
ax.plot([1.5, x_wire3[0]], [3.5, 3.5], 'k-', lw=1.5)
# Load with Thevenin
ax.plot([8.5, 8.5], [1.0, 3.5], 'r-', lw=2)
rect_l3 = patches.Rectangle((7.8, 1.5), 1.4, 1.5, facecolor=RED, alpha=0.2, edgecolor=RED)
ax.add_patch(rect_l3)
ax.text(8.5, 2.2, '负载', ha='center', fontsize=9, fontweight='bold')
# R1 to VCC (top)
ax.plot([8.5, 8.5], [3.5, 4.3], 'k-', lw=1)
rect_r1 = patches.Rectangle((8.3, 4.3), 0.4, 0.5, facecolor=PURPLE, alpha=0.6, edgecolor=PURPLE, lw=1.5)
ax.add_patch(rect_r1)
ax.text(9.3, 4.5, 'R1', fontsize=9, color=PURPLE, fontweight='bold')
ax.text(9.7, 4.5, 'VCC', fontsize=8, color=GRAY)
# R2 to GND
rect_r2b = patches.Rectangle((8.3, 1.0), 0.4, 0.5, facecolor=PURPLE, alpha=0.6, edgecolor=PURPLE, lw=1.5)
ax.add_patch(rect_r2b)
ax.plot([8.5, 8.5], [1.5, 1.0], 'k-', lw=1)
ax.plot([8.5, 8.5], [1.0, 0.5], 'k-', lw=1.5)
ax.text(9.3, 1.2, 'R2', fontsize=9, color=PURPLE, fontweight='bold')
ax.text(5, 4.5, 'R1∥R2 = Z₀', fontsize=8, color=PURPLE, fontweight='bold')
ax.set_title('③ 戴维南端接', fontweight='bold', fontsize=11, color=PURPLE)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.5)
ax.axis('off')

# --- AC termination ---
ax = axes[1, 1]
x_wire4 = np.linspace(0.5, 8.0, 15)
ax.plot(x_wire4, [3.5]*15, 'k-', lw=2)
ax.plot(x_wire4, [0.5]*15, 'k-', lw=2)
rect_d4 = patches.Rectangle((0.3, 1.0), 1.2, 2.0, facecolor=BLUE, alpha=0.2, edgecolor=BLUE)
ax.add_patch(rect_d4)
ax.text(0.9, 2.0, '驱动', ha='center', fontsize=9, fontweight='bold')
ax.plot([1.5, x_wire4[0]], [3.5, 3.5], 'k-', lw=1.5)
# Load with AC term
ax.plot([8.5, 8.5], [1.0, 3.5], 'r-', lw=2)
rect_l4 = patches.Rectangle((7.8, 1.5), 1.4, 1.5, facecolor=RED, alpha=0.2, edgecolor=RED)
ax.add_patch(rect_l4)
ax.text(8.5, 2.2, '负载', ha='center', fontsize=9, fontweight='bold')
# C + R to gnd
# C first
ax.plot([8.5, 8.5], [1.5, 1.2], 'k-', lw=1)
rect_c = patches.Rectangle((8.15, 0.7), 0.3, 0.5, facecolor=CYAN, alpha=0.5, edgecolor=CYAN, lw=1.5)
ax.add_patch(rect_c)
rect_c2 = patches.Rectangle((8.55, 0.7), 0.3, 0.5, facecolor=CYAN, alpha=0.5, edgecolor=CYAN, lw=1.5)
ax.add_patch(rect_c2)
ax.text(9.5, 0.95, 'C', fontsize=9, color=CYAN, fontweight='bold')
# R to gnd
rect_rac = patches.Rectangle((7.3, 0.7), 0.4, 0.5, facecolor=GREEN, alpha=0.5, edgecolor=GREEN, lw=1.5)
ax.add_patch(rect_rac)
ax.plot([7.5, 8.5], [0.95, 0.95], 'k-', lw=1)
ax.plot([7.5, 7.5], [0.7, 0.5], 'k-', lw=1)
ax.text(6.7, 0.95, 'Rt=Z₀', fontsize=8, color=GREEN, fontweight='bold')
ax.text(5, 4.3, 'C隔直 → 无直流功耗 ✅', fontsize=8, color=CYAN, fontweight='bold')
ax.set_title('④ AC 端接', fontweight='bold', fontsize=11, color=CYAN)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.5)
ax.axis('off')

plt.suptitle('四种端接方案对比', fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-termination-types.png'))
plt.close()

# ============================================================
# 6. Microstrip vs Stripline cross section
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# Microstrip
ax1.set_xlim(0, 8)
ax1.set_ylim(0, 5)

# Air
ax1.fill_between([0, 8], 3.2, 5, color='lightblue', alpha=0.3)
ax1.text(0.5, 4.5, '空气 (εᵣ≈1)', fontsize=9, color=GRAY)

# Substrate
ax1.fill_between([0, 8], 2.2, 3.2, color='tan', alpha=0.5)
ax1.text(0.5, 2.7, 'FR4 介质 (εᵣ≈4.2)', fontsize=9, color=DARK)

# Copper trace on surface
trace = patches.Rectangle((3.0, 3.2), 2.0, 0.15, facecolor=ORANGE, edgecolor='darkorange', lw=1.5)
ax1.add_patch(trace)
ax1.text(4, 3.55, f'铜走线 (W)', ha='center', fontsize=9, color=ORANGE, fontweight='bold')

# Ground plane
gnd = patches.Rectangle((0.5, 2.0), 7, 0.2, facecolor=GRAY, edgecolor=DARK, lw=1)
ax1.add_patch(gnd)
ax1.text(4, 1.7, '参考地平面', ha='center', fontsize=9, color=GRAY)

# Dimension arrows
ax1.annotate('', xy=(2.5, 3.2), xytext=(2.5, 2.2),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.5))
ax1.text(1.8, 2.7, 'H', fontsize=11, color=BLUE, fontweight='bold')

# E-field lines (curved, going through air and substrate)
for x_pos in [3.3, 4.0, 4.7]:
    # field from trace to gnd (in substrate)
    ax1.annotate('', xy=(x_pos, 2.3), xytext=(x_pos, 3.25),
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=0.8, alpha=0.5))
    # field from trace to air
    if x_pos == 4.0:
        ax1.annotate('', xy=(x_pos, 3.8), xytext=(x_pos, 3.35),
                    arrowprops=dict(arrowstyle='->', color=BLUE, lw=0.8, alpha=0.3))

ax1.text(4, 1.2, '有效 εᵣ_eff ≈ (εᵣ+1)/2', ha='center', fontsize=9, color=BLUE, fontweight='bold')
ax1.set_title('微带线 (Microstrip)', fontweight='bold', fontsize=12)
ax1.axis('off')

# Stripline
ax2.set_xlim(0, 8)
ax2.set_ylim(0, 5)

# Upper substrate
ax2.fill_between([0, 8], 3.2, 5, color='tan', alpha=0.5)
ax2.text(0.5, 4.5, 'FR4 介质', fontsize=9, color=DARK)

# Lower substrate
ax2.fill_between([0, 8], 2.2, 3.2, color='tan', alpha=0.5)

# Copper trace embedded
trace2 = patches.Rectangle((3.0, 3.0), 2.0, 0.15, facecolor=ORANGE, edgecolor='darkorange', lw=1.5)
ax2.add_patch(trace2)
ax2.text(4, 3.35, f'铜走线 (W)', ha='center', fontsize=9, color=ORANGE, fontweight='bold')

# Upper ground plane
gnd_u = patches.Rectangle((0.5, 4.2), 7, 0.2, facecolor=GRAY, edgecolor=DARK, lw=1)
ax2.add_patch(gnd_u)
ax2.text(4, 4.55, '上参考地平面', ha='center', fontsize=9, color=GRAY)

# Lower ground plane
gnd_l = patches.Rectangle((0.5, 2.0), 7, 0.2, facecolor=GRAY, edgecolor=DARK, lw=1)
ax2.add_patch(gnd_l)
ax2.text(4, 1.7, '下参考地平面', ha='center', fontsize=9, color=GRAY)

# E-field lines (symmetric, bounded)
for x_pos in [3.3, 4.0, 4.7]:
    ax2.annotate('', xy=(x_pos, 3.2), xytext=(x_pos, 4.1),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=0.8, alpha=0.5))
    ax2.annotate('', xy=(x_pos, 2.9), xytext=(x_pos, 2.15),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=0.8, alpha=0.5))

ax2.text(4, 1.2, 'εᵣ_eff = εᵣ（全在介质中）', ha='center', fontsize=9, color=GREEN, fontweight='bold')
ax2.set_title('带状线 (Stripline)', fontweight='bold', fontsize=12)
ax2.axis('off')

plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-microstrip-stripline.png'))
plt.close()

# ============================================================
# 7. Impedance discontinuities
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))

discont = ['过孔 (Via)', '分支/Stub', '连接器 (Connector)']
for idx, (ax, title) in enumerate(zip(axes, discont)):
    ax.plot([0.5, 9.5], [3.5, 3.5], 'k-', lw=2)
    ax.plot([0.5, 9.5], [0.5, 0.5], 'k-', lw=2)
    
    if idx == 0:  # Via
        # Top layer
        ax.text(2, 3.8, 'L1 (顶层)', fontsize=8, color=GRAY)
        ax.text(7, 2.5, 'L3 (内层)', fontsize=8, color=GRAY)
        # Via barrel
        ax.plot([4.5, 4.5], [0.7, 3.5], 'k-', lw=2.5)
        # Annular ring top
        ring = patches.Circle((4.5, 3.5), 0.3, facecolor='none', edgecolor=ORANGE, lw=2)
        ax.add_patch(ring)
        # Annular ring bottom
        ring2 = patches.Circle((4.5, 0.7), 0.3, facecolor='none', edgecolor=ORANGE, lw=2)
        ax.add_patch(ring2)
        # Via pad
        ax.annotate('', xy=(4.7, 1.5), xytext=(8, 1.5),
                   arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
        ax.text(6.5, 1.2, 'L过长→感性\n阻抗跳变', ha='center', fontsize=8, color=RED, fontweight='bold')
        ax.text(4.5, 4.2, '过孔 stub 效应', ha='center', fontsize=9, color=RED, fontweight='bold')
        
    elif idx == 1:  # Stub
        ax.plot([0.5, 9.5], [3.5, 3.5], 'k-', lw=2)
        # Main branch point
        ax.plot([5.0, 5.0], [0.5, 3.5], 'k-', lw=2)
        # Stub
        ax.plot([5.0, 7.5], [2.5, 2.5], 'r-', lw=2, ls='--')
        ax.text(6.5, 2.2, 'Stub（开路分支）', ha='center', fontsize=8, color=RED, fontweight='bold')
        # Signal path
        ax.annotate('信号', xy=(3, 3.8), fontsize=8, color=BLUE, fontweight='bold')
        ax.annotate('', xy=(7, 3.5), xytext=(3, 3.5),
                   arrowprops=dict(arrowstyle='->', color=BLUE, lw=2))
        # Reflection
        ax.annotate('反射', xy=(5.5, 1.0), fontsize=8, color=RED, fontweight='bold')
        ax.plot([5.5, 5.0], [1.0, 1.5], 'r-', lw=1)
        ax.text(5, 0.6, 'Z₀不连续→反射', ha='center', fontsize=9, color=RED, fontweight='bold')
        ax.text(6.5, 4.2, 'Stub = 阻抗不连续点', ha='center', fontsize=9, color=RED, fontweight='bold')
        
    elif idx == 2:  # Connector
        # TL left
        ax.plot([0.5, 4.0], [3.5, 3.5], 'k-', lw=2)
        # Connector
        rect_conn = patches.Rectangle((4.0, 2.0), 1.5, 1.5, facecolor=ORANGE, alpha=0.3, edgecolor=ORANGE, lw=1.5)
        ax.add_patch(rect_conn)
        ax.text(4.75, 2.7, '连接器', ha='center', fontsize=9, fontweight='bold')
        # TL right
        ax.plot([5.5, 9.5], [3.5, 3.5], 'k-', lw=2)
        # Impedance graph overlay
        ax.plot([3.0, 4.0, 4.5, 5.0, 5.5, 6.5], [1.2, 1.2, 1.8, 1.8, 1.2, 1.2], 'r-', lw=2)
        ax.text(3.5, 0.85, 'Z₀变化 ↓', ha='center', fontsize=7, color=RED)
        ax.text(6.0, 4.2, '引脚电感→阻抗尖峰', ha='center', fontsize=9, color=RED, fontweight='bold')
    
    ax.set_title(title, fontweight='bold', fontsize=11)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

plt.suptitle('传输线中的阻抗不连续', fontweight='bold', fontsize=13)
plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-impedance-discontinuities.png'))
plt.close()

# ============================================================
# 8. TDR principle
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5.5), gridspec_kw={'height_ratios': [1, 1.2]})

# Top: TDR setup
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 4)
# TDR instrument
rect_tdr = patches.Rectangle((0.5, 1.5), 2.0, 1.5, facecolor=BLUE, alpha=0.2, edgecolor=BLUE, lw=1.5)
ax1.add_patch(rect_tdr)
ax1.text(1.5, 2.25, 'TDR\n脉冲源', ha='center', fontsize=9, fontweight='bold')
# DUT (transmission line)
ax1.plot([2.5, 9.5], [2.8, 2.8], 'k-', lw=2)
ax1.plot([2.5, 9.5], [1.7, 1.7], 'k-', lw=2)
ax1.text(6, 2.5, '待测传输线 (DUT)', ha='center', fontsize=10, fontweight='bold')
# Incident pulse
ax1.annotate('', xy=(4, 3.2), xytext=(2.8, 3.2),
            arrowprops=dict(arrowstyle='->', color=BLUE, lw=2))
ax1.text(3.4, 3.5, '快沿脉冲', fontsize=9, color=BLUE, fontweight='bold')
# Reflected pulse
ax1.annotate('', xy=(2.8, 1.3), xytext=(4.5, 1.3),
            arrowprops=dict(arrowstyle='->', color=RED, lw=2, ls='--'))
ax1.text(3.2, 1.0, '反射波（含阻抗信息）', fontsize=9, color=RED, fontweight='bold')
ax1.set_title('TDR 工作原理', fontweight='bold', fontsize=12)
ax1.axis('off')

# Bottom: TDR waveform
t = np.linspace(0, 10, 500)
z = np.ones_like(t) * 50  # baseline 50Ω
# 50Ω section
z[:80] = 50
# Low Z section (wide trace) at 1-3ns
z[80:160] = 35
# Back to 50Ω
z[160:240] = 50
# High Z section (narrow trace) at 3-5ns
z[240:320] = 75
# Open at end
z[320:400] = 150
# Later
z[400:] = 50

ax2.plot(t, z, BLUE, lw=2)
ax2.axhline(y=50, color=GRAY, ls='--', alpha=0.5, lw=1)
ax2.set_xlabel('时间 (反映距离)', fontsize=11)
ax2.set_ylabel('阻抗 (Ω)', fontsize=11)
ax2.set_title('TDR 阻抗曲线（沿走线方向）', fontweight='bold', fontsize=12)
ax2.set_ylim(20, 180)
ax2.grid(alpha=0.3)

# Annotations
ax2.annotate('宽线:\nZ↓', xy=(2.5, 35), fontsize=8, color=RED, fontweight='bold')
ax2.annotate('窄线:\nZ↑', xy=(5.5, 75), fontsize=8, color=RED, fontweight='bold')
ax2.annotate('开路:\nZ→∞', xy=(7.5, 150), fontsize=8, color=RED, fontweight='bold')
ax2.annotate('标称 50Ω', xy=(8.5, 52), fontsize=8, color=GRAY)

plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-tdr-principle.png'))
plt.close()

# ============================================================
# 9. Example 4-layer stackup
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5.5))

layers = [
    ('L1 - TOP (信号)', 6.5, 'copper', BLUE, '18μm 铜箔\n微带线: Z₀可控'),
    ('PP 半固化片', 6.0, 'dielectric', 'tan', '~0.1mm\n介电常数 εᵣ≈4.0'),
    ('L2 - GND (地平面)', 5.2, 'copper', GRAY, '35μm 铜箔\n完整参考平面'),
    ('Core 芯板', 4.2, 'dielectric', 'tan', '~1.0mm\nFR4 芯板'),
    ('L3 - PWR (电源)', 2.8, 'copper', ORANGE, '35μm 铜箔\n电源平面'),
    ('PP 半固化片', 2.3, 'dielectric', 'tan', '~0.1mm'),
    ('L4 - BOTTOM (信号)', 1.5, 'copper', GREEN, '18μm 铜箔\n微带线: Z₀可控'),
]

for name, y, ltype, color, desc in layers:
    if ltype == 'copper':
        ax.fill_between([0, 10], y-0.3, y+0.3, color=color, alpha=0.7, edgecolor=DARK, lw=1)
    else:
        ax.fill_between([0, 10], y-0.4, y+0.4, color=color, alpha=0.3)
    
    # Label
    if 'TOP' in name or 'BOTTOM' in name:
        ax.text(5, y, name, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    elif 'GND' in name or 'PWR' in name:
        ax.text(5, y, name, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    else:
        ax.text(5, y, name, ha='center', va='center', fontsize=9, fontweight='bold', color=DARK)
    
    # Description on right
    ax.text(10.3, y, desc, fontsize=7, color=GRAY, va='center')

# Total thickness indicator
ax.annotate('', xy=(9.5, 7.0), xytext=(9.5, 1.0),
           arrowprops=dict(arrowstyle='<->', color=DARK, lw=1.5))
ax.text(9.0, 4.0, '总厚\n≈1.6mm', ha='center', fontsize=9, fontweight='bold')

ax.set_title('典型 4 层板叠层结构（阻抗控制示例）', fontweight='bold', fontsize=13)
ax.set_xlim(0, 11.5)
ax.set_ylim(0.5, 7.5)
ax.axis('off')

plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-stackup-4layer.png'))
plt.close()

# ============================================================
# 10. Termination decision flowchart
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

def draw_box(x, y, w, h, text, color=BLUE, fontsize=9, fontweight='normal'):
    rect = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.15",
                                    facecolor=color, alpha=0.15, edgecolor=color, lw=1.5)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight=fontweight)

def draw_arrow(x1, y1, x2, y2, label='', color=DARK):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
               arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.2, my, label, fontsize=7, color=color, fontweight='bold')

# Start
draw_box(5, 11, 4, 0.8, '需要端接吗？', DARK, fontsize=11, fontweight='bold')

# Branch 1: L < critical
draw_box(2, 9.5, 3.2, 0.7, 'L < Tᵣ·v/6 ?\n(走线很短)', GREEN, fontsize=8)
draw_arrow(5, 10.6, 3.5, 9.85, '是')
draw_box(2, 8.5, 2.0, 0.6, '不需要', GREEN, fontsize=9, fontweight='bold')

# Branch 2: No - need termination
draw_box(7.5, 9.5, 3.2, 0.7, 'L > 临界长度\n→ 必须端接', RED, fontsize=8)
draw_arrow(5, 10.6, 6.6, 9.85, '否')

# Point to point?
draw_box(7.5, 8.2, 3.5, 0.7, '点对点?\n(单驱单收)', BLUE, fontsize=8)
draw_arrow(7.5, 9.15, 7.5, 8.55)

# Yes - source series
draw_box(7.5, 6.8, 3.5, 0.7, '源端串联匹配 ✅\nRs + Rout = Z₀', ORANGE, fontsize=9, fontweight='bold')
draw_arrow(7.5, 7.85, 7.5, 7.15, '是')

# No - bus/multi-load
draw_box(2, 6.8, 3.5, 0.7, '总线/多负载?\n→ 不能用源端', RED, fontsize=8)
draw_arrow(6.25, 8.0, 3.5, 7.15, '否')

# Power constrained?
draw_box(2, 5.3, 3.5, 0.7, '功耗敏感?\n(电池/低功耗)', RED, fontsize=8)
draw_arrow(2, 6.45, 2, 5.65)

# Not power sensitive -> Thevenin
draw_box(5.5, 4.0, 3.5, 0.7, '戴维南端接\nR1∥R2 = Z₀', PURPLE, fontsize=9, fontweight='bold')
draw_arrow(2, 4.95, 5.5, 4.35, '否')

# Power sensitive -> AC
draw_box(2, 3.5, 3.5, 0.7, 'AC 端接\nC + Rt = Z₀', CYAN, fontsize=9, fontweight='bold')
draw_arrow(2, 4.95, 2, 3.85, '是')

# Low freq alternative
draw_box(7.5, 5.3, 3.5, 0.7, '频率不高?\n二极管钳位也可', GRAY, fontsize=8)
draw_arrow(7.5, 6.45, 7.5, 5.65)

# Notes
draw_box(5, 1.8, 8, 1.0, 
         '💡 经验: 90% 高速数字场景用源端串联匹配就够了\nDDR/总线 用戴维南 | 射频/低功耗 用 AC | 保护用钳位',
         GRAY, fontsize=8)

ax.set_title('端接方案选择决策树', fontweight='bold', fontsize=13, y=0.98)
plt.tight_layout()
fig.savefig(os.path.join(OUT, '03-termination-decision.png'))
plt.close()

print("✅ Day 03 diagrams generated successfully!")
print(f"   Output directory: {OUT}")
