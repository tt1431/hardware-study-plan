# 信号完整性学习笔记 ②｜数字信号的频谱与带宽

> 📚 《信号完整性揭秘：于博士 SI 设计手记》第二章  
> 📅 2026-06-10

---

> 📖 教材原文 + 图：p12~36 | [第2章全部页面](https://github.com/tt1431/hardware-study-plan/tree/main/assets/si_textbook/ch2)

## 2.1 一个前提：同一根线，不同频率，不同态度

做硬件的人每天都在画 PCB 走线。在低速时代，一根线就是一根导体——连上就行。

但到了高速，同一条走线对不同频率的信号分量态度完全不同。四个物理效应决定了一切。

**寄生电感。** 任何导体都有自感，走线也不例外：

$$
X_L = 2\pi f L
$$

频率 $f$ 翻 10 倍，感抗翻 10 倍。10MHz 下走线电感几乎不构成阻碍，到了 1GHz 高频电流要走这根线得克服很大的阻抗。

**寄生电容。** 走线和参考平面之间就是电容：

$$
X_C = \frac{1}{2\pi f C}
$$

频率 $f$ 翻 10 倍，容抗降到 1/10。高频信号更容易通过寄生电容"漏"到参考平面上去。

**趋肤效应。** 直流电流走导体的整个截面，交流电流被"挤"到表面。频率越高，电流走的"皮"越薄——等效截面积变小，电阻变大。

**介质损耗。** FR4 板基本身在交变电场中会消耗能量，频率越高越明显。GHz 级别的高频分量在 FR4 里走不了多远就衰减了。

**一句话总结：** 同一根走线对低频几乎无损，对高频衰减严重。信号里有多少高频分量，就决定了 SI 问题的严重程度。

---

## 2.2 傅里叶在说什么

傅里叶的核心结论：**任何周期信号都可以分解为若干个正弦波之和。**

### 从正弦波到方波

正弦波只有一个频率成分。示波器上看，就是干干净净的一条正弦曲线。

方波呢？一个理想方波（Tr = 0）可以写成一堆正弦波的叠加：

$$
v(t) = \frac{4}{\pi}\left(\sin\omega t + \frac{1}{3}\sin 3\omega t + \frac{1}{5}\sin 5\omega t + \frac{1}{7}\sin 7\omega t + \cdots\right)
$$

几点关键信息：

- **只有奇次谐波。** 2、4、6 次等偶次谐波幅度为零。
- **谐波频率：** 基频 $f_0 = 1/T。3 次谐波 3f_0，5 次 5f_0$……
- **谐波幅度：** 按 $1/n 衰减。3 次谐波幅度是基频的 1/3，5 次是 1/5$.频率越高分量越弱，但永远不为零——理想方波包含从基频到无穷大的所有奇次谐波。

如果你只取基频 + 3 次谐波，波形已经像个方波了。加上 5 次、7 次……谐波越多越接近完美方波。这就是谐波叠加还原波形的原理。

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/02-square-wave-decomposition.png)

**谐波数量越多，合成波形越逼近理想方波：**

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_summary/02-harmonic-reconstruction.png)

---

## 2.3 频谱是什么

**频谱**就是把信号从时域搬到频域来看。

- **时域：** 横轴时间，看电压随时间变化——这是示波器。
- **频域：** 横轴频率，看每个频率分量的大小——这是频谱分析仪。

### 对数坐标

工程上画频谱通常用对数坐标。因为频率范围太宽（Hz ~ GHz 跨 9 个数量级），幅度范围也太宽，线性坐标根本画不下。

在对数坐标系中，理想方波的高频段是一条斜线：**每增加十倍频程（频率 $\times 10），幅度下降 20dB（幅度 \times 0.1$)。**

这个斜率 $-20\text{dB/dec}$ 是本章最重要的基本量。

---

## 2.4 理想方波 vs 真实方波

现实中没有 $T_r = 0$ 的方波。真实信号是**梯形波**——上升和下降需要时间。

### 理想方波的频谱

高频段以 $-20\text{dB/dec}$ 斜率一直衰减下去。不管多高频，总有那么一点点能量。

### 方波 vs 梯形波：频谱对比

方波（Tr=0）的频谱在高端一直以 -20dB/dec 衰减。梯形波（Tr>0）则不同——第二个拐点之后以 -40dB/dec 加速衰减，高频分量被迅速削掉。

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_summary/02-spectrum-comparison.png)

### 梯形波的频谱：两个拐点

梯形波的频谱有两个关键频率拐点：

**第一拐点 $\displaystyle f_1 = \frac{1}{\pi \cdot t_p}**（t_p$ 为脉冲宽度）

频率超过 $f_1 之后，幅度开始以 -20\text{dB/dec}$ 下降。这和理想方波一样。

**第二拐点 $\displaystyle f_2 = \frac{1}{\pi \cdot T_r}$**

频率超过 $f_2 之后，幅度以 **-40\text{dB/dec}$** 加速下降。

- $-20\text{dB/dec} = 频率 \times 10，幅度 \times 0.1$
- $-40\text{dB/dec} = 频率 \times 10，幅度 \times 0.01$

衰减速度差了 10 倍。超过 $f_2$ 后高频分量被迅速削掉。

### Tr 怎么决定一切

变量 $T_r 出现在第二个拐点的分母上。T_r 越小，f_2$ 越大，加速衰减开始得越晚。

用两个具体数字感受：

| | $T_r = 1\text{ns}$ | $T_r = 0.1\text{ns}$ |
|:--|:--|:--|
| $f_2$ | $\approx 318\text{MHz}$ | $\approx 3.18\text{GHz}$ |
| $< 318\text{MHz}$ | $-20\text{dB/dec}$ 温和衰减 | $-20\text{dB/dec}$ 温和衰减 |
| $318\text{MHz} \sim 3.18\text{GHz}$ | $-40\text{dB/dec}$ **加速衰减** | $-20\text{dB/dec}$ **仍在温和衰减** |
| $> 3.18\text{GHz}$ | — | $-40\text{dB/dec}$ 加速衰减 |

看 1GHz 处：

- $T_r = 1\text{ns}$ 的信号在 1GHz 时已进入加速衰减段，幅度被压得很低。
- $T_r = 0.1\text{ns}$ 的信号在 1GHz 时仍在温和衰减段，幅度还很可观。

> **$T_r 减小 \rightarrow 拐点 f_2 推高 \rightarrow 更宽频率范围保留高频能量 \rightarrow$ SI 问题更严重。** 这就是第一章 "Tr 减小是 SI 根源" 的数学证明。

---

## 2.5 信号带宽：哪些频率可以不管

理想方波要完美还原需要无穷大带宽——不现实。

工程上定义：**高频分量的幅度小到对波形几乎没有影响时，就可以忽略。这个截止频率就是信号带宽。**

### 核心公式

$$
BW = \frac{k}{T_r}
$$

两个系数，不同场景：

- $k = 0.35 → 仪器/放大器的 -3\text{dB}$ 带宽（近似单极点响应）
- $k = 0.5$ → 高速数字 SI 设计时用（多留了裕度）

用实际芯片跑一下：

| 信号 | $T_r$ | $BW\ (k=0.5)$ | 意味着什么 |
|:--|:--|:--|:--|
| 74HC 老式逻辑 | 10ns | 50MHz | 基本不用管 SI |
| 74LVC 高速逻辑 | 1ns | 500MHz | 走线超 3cm 就得端接 |
| DDR4 数据线 | 0.08ns | 6.25GHz | 全程控阻抗、严格等长 |
| PCIe 4.0 | 0.03ns | ~17GHz | 高速板材、严格损耗预算 |

面试被问"信号带宽怎么算"——回答 $BW = 0.35/T_r$ 没错。再加一句"做 SI 设计我按 $BW = 0.5/T_r$ 留裕度"，面试官就知道你是干过活的。

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/02-bandwidth-vs-tr.png)

### $k=0.35$ 的物理来源：单极点低通滤 波

$k=0.35$ 来自单极点 RC 低通滤波器的 -3dB 带宽。幅频特性在截止频率后以 -20dB/dec 滚降：

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_summary/02-filter-response.png)

高阶系统（实际电路通常更复杂）在高频段会有更陡峭的滚降和多处衰减陷波：

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_summary/02-high-order-filter.png)

**工程选择：**
- 看仪器/放大器带宽，用 $k=0.35$(近似单极点 -3dB）
- 做高速数字 SI 设计，用 $k=0.5$(留足裕度，确保波形还原）

---

## 2.6 实践：拿到信号三步判断

实际工作中不需要背证明过程，掌握这三步：

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/02-practical-workflow.png)

### 步骤 1：用示波器量 Tr

注意探头带宽——被动探头带宽不够会把 Tr 测大，导致误判。

### 步骤 2：算带宽

公式 $BW = 0.5/T_r，心里过一下。T_r = 1\text{ns} \rightarrow 500\text{MHz}；T_r = 0.3\text{ns} \rightarrow 1.7\text{GHz}$.

### 步骤 3：判断要不要管 SI

经验阈值：

- $BW < 100\text{MHz}$ → 基本不用管，走线就是导 线
- $100\text{MHz} < BW < 500\text{MHz} → 看走线长度。走线延时 > T_r/6 就得端接。FR4 信号速度约 15\text{cm/ns}，T_r = 1\text{ns} 时临界长度 \approx 2.5\text{cm}$
- $BW > 500\text{MHz}$ → 必须认真对待，控阻抗、端接、等 长

### 反过来用：选仪器

想量 $T_r = 0.5\text{ns}$ 的时钟：

- 示波器带宽至少 $0.5/0.5\text{n} = 1\text{GHz}，买 1.5\text{GHz}$ 留裕 度
- 探头带宽也要满足（被动探头通常 $200\sim500\text{MHz}$,得用有源探头）
- 采样率至少 $5 \times BW$(Nyquist 大法好）

---

## 本章小结

这一章的核心就一条线：

$$
T_r \;\longrightarrow\; BW = \frac{k}{T_r} \;\longrightarrow\; \text{高频分量多少} \;\longrightarrow\; \text{SI 问题程度}
$$

- 傅里叶分解：方波 = 一堆正弦波叠加
- 梯形波有两个拐点,$f_2 = 1/(\pi \cdot T_r)$ 由 Tr 决 定
- $BW = 0.5/T_r$ 是做 SI 设计最常用的公 式
- 拿到信号：量 $T_r → 算 BW$ → 判断需不需要控阻 抗

---

> 下一章：传输线——高速信号眼里，走线不是导线，是电磁波通道.$Z_0 = \sqrt{L/C}$ 怎么来的？

