# 信号完整性学习笔记 3 | 传输线理论基础

> 教材: 《信号完整性揭秘: 于博士 SI 设计手记》第3章
> 日期: 2026-06-23

---

> 教材原文+图: p37~74 | [第3章全部页面](https://github.com/tt1431/hardware-study-plan/tree/main/assets/si_textbook/ch3)

## 3.0 本章在 SI 知识体系中的位置

Day 1 回答了"信号完整性是什么", Day 2 回答了"带宽怎么算".

Day 3 回答核心问题: **高速信号在走线里到底怎么走的?**

前面两章你已经掌握了:
- Tr 越小 -> SI 问题越严重 (Day 1)
- BW = 0.5/Tr -> 高频分量有多少 (Day 2)
- 50 Ohm 的来历, 源端串联匹配的原理, 差分对基础 (Day 1 扩展)

这一章把这些串起来: 带宽告诉你"有多少高频分量" -> 传输线告诉你"这些高频分量在走线里会受到什么对待".

---

## 3.1 从"导线"到"传输线" -- 认知的跃迁

### 3.1.1 什么时候一根线不再是导线?

低速时代, PCB 走线就是导线 -- 连上就行. 但频率上去之后, 同一根走线对低频和高频的态度完全不同 (Day 2 Section 2.1 已讲).

有更工程化的判据: **走线的物理长度和信号上升沿的等效物理长度之比.**

### 临界长度公式

$$
L_{critical} \approx \frac{T_r}{6} \times v_p
$$

$v_p$ 是信号在 PCB 上的传播速度.

FR4 微带线: $v_p \approx 15\text{ cm/ns}$ (真空光速的约一半).

**捷径:** $T_r$ 单位取 ns, 临界长度直接心算:

$$
L_{critical}(\text{cm}) \approx T_r(\text{ns}) \times 2.5
$$

| 上升时间 $T_r$ | 临界长度 | 典型走线 | 要当传输线吗? |
|:--|:--|:--|:--|
| 10 ns (老式 TTL) | ~25 cm | 5~15 cm | X 不用管 |
| 1 ns (74LVC 高速) | ~2.5 cm | 5~15 cm | W 大概率要 |
| 0.1 ns (DDR4) | ~2.5 mm | 5~15 cm | V 必须 |
| 0.03 ns (PCIe 4.0) | ~0.75 mm | 随便多长 | V 全程严格控制 |

> W 再次强调: 决定因素不是时钟频率, 是上升时间. 1MHz 的时钟如果是 74LVC 驱动 (Tr=1ns), 临界长度一样是 2.5cm.

### 知识卡片: FR4 是什么

FR4 是 PCB 行业最常用的基板材料, 全称 **Flame Retardant 4** (阻燃等级 4).

**成分:** 玻璃纤维布浸渍环氧树脂, 经高温压合而成. 玻璃纤维提供机械强度, 环氧树脂作为粘合剂和绝缘体.

**关键电性能参数:**

| 参数 | 典型值 | 含义 |
|:--|:--|:--|
| 介电常数 $\epsilon_r$ | 4.0 ~ 4.5 (常用 4.2) | 材料储存电场的能力, 决定信号传播速度 |
| 损耗角正切 $tan\delta$ | 0.015 ~ 0.025 | 材料消耗电磁能量的程度, 值越小损耗越低 |
| 玻璃化转变温度 Tg | 130 C ~ 180 C | 超过此温度材料软化, 尺寸和电性能剧变 |
| 热膨胀系数 CTE | 12~16 ppm/C (XY) | 温度变化时尺寸变化率, 影响过孔可靠性 |

**为什么 FR4 无处不在?**

- V 成本低 -- 每平方米几十块钱, 批量生产成本极低
- V 工艺成熟 -- 全球 PCB 厂都对 FR4 了如指掌, 良率高
- V 机械性能好 -- 刚性够, 钻孔, 切割, 焊接都容易
- V 阻燃 -- 即使过热也不会持续燃烧

**FR4 的局限 (高速设计为什么嫌弃它):**

- X 介电常数不稳定 -- $\epsilon_r$ 随频率和温度变化, GHz 以上波动明显
- X 损耗大 -- $tan\delta \approx 0.02$ 意味着 10GHz 信号每走 10cm 可能衰减 30% 以上
- X 吸湿 -- 吸收空气中的水分后介电常数和损耗角都会增大

**什么时候必须换掉 FR4?**

| 应用 | 推荐板材 | 原因 |
|:--|:--|:--|
| < 3GHz 常规数字 | FR4 | 够用且便宜 |
| 3~10GHz 高速数字 | FR4 (短走线) 或 Megtron 6 | 长走线损耗不可忽略 |
| > 10GHz (PCIe 5.0+, 雷达) | Rogers 4350B, Megtron 7 | FR4 损耗太大, 信号睁不开眼 |
| 射频/微波 | Rogers, Taconic, PTFE | 需要极低且稳定的 $\epsilon_r$ |
| 高温环境 (>150 C) | 高 Tg FR4 或 Polyimide | 普通 FR4 会软化 |

> 记一个数: FR4 微带线信号速度约等于 15 cm/ns (约光速的一半). 做高速设计时, 这个数能帮你快速估算延迟和临界长度.

### 3.1.2 集总模型 vs 分布模型

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-critical-length.png)

**图解读:** 上图展示了从集总模型到分布模型的认知跃迁. 左侧集总模型把整段走线简化为一个 RLC 串联网络 -- 适用于走线长度小于临界长度的情况. 右侧分布模型把走线视为无穷多个微小 RLCG 单元的级联 -- 当走线长度超过临界长度时, 必须使用此模型, 因为信号在走线上不同位置的电压/电流不再同时变化.

- **走线 < 临界长度**: 导线各处电压几乎同时变化 -> **集总模型**够用 (一根导线 + 对地电容 + 串联电感)
- **走线 > 临界长度**: 信号需要**时间**从源端走到负载端 -> **分布模型**必须用 (传输线)

分布模型的核心: 走线不再是"一根"东西, 而是**无穷多个 RLCG 单元串接**.

---

## 3.2 RLCG 传输线模型

### 3.2.1 每单位长度的分布参数

走线不是理想导体. 每毫米都有:

| 分布参数 | 符号 | 单位 | 物理来源 |
|:--|:--|:--|:--|
| 串联电阻 | $R$ | Ohm/m | 铜导体不是超导体, 有欧姆损耗 |
| 串联电感 | $L$ | H/m | 电流流过导体产生磁通 |
| 并联电容 | $C$ | F/m | 走线与参考平面形成平行板电容 |
| 并联电导 | $G$ | S/m | 介质泄漏 (FR4 不是完美绝缘体) |

### 3.2.2 等效电路

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-rlcg-model.png)

**图解读:** 上图展示了一段无限短 $\Delta z$
的传输线等效电路模型. 信号路径上的串联电阻 $R\Delta z$
和串联电感 $L\Delta z$
构成串联支路; 信号路径与返回路径之间的并联电容 $C\Delta z$
和并联电导 $G\Delta z$
构成并联支路. 实际的传输线是无穷多个这种单元级联, 每个单元代表一小段 $\Delta z$ .

### 3.2.3 无损近似

在大多数数字 PCB 场景下:

$R$ 很小.

$G$ 很小.

高频下 $\omega L$ 很大 (感抗远大于电阻).

$\omega C$ 很大 (容抗远大于电导).

可以先当**无损传输线**处理:

$$
R \approx 0,\quad G \approx 0
$$

无损传输线的特性阻抗简化为:

$$
Z_0 = \sqrt{\frac{L}{C}}
$$

> 这就是 Day 1 Section 1.10 详细讲过的 $Z_0 = \sqrt{L/C}$. 复习要点: **特性阻抗不由长度决定, 由截面几何决定.**

### 3.2.4 什么时候必须考虑损耗?

| 场景 | 能否忽略 R 和 G |
|:--|:--|
| FR4 板上 < 5cm 走线, < 3GHz | V 忽略 |
| FR4 板上 10cm 以上, > 5GHz | W 要考虑 |
| 长背板, 线缆 | X 不能忽略 |
| 射频 PCB (Rogers 板材) | X 不能用 FR4 的近似 |

---

## 3.3 信号在传输线上怎么走

### 3.3.1 传播速度

信号在传输线中以**不到光速**传播. 速度由周围介质的介电常数决定:

$$
v_p = \frac{c}{\sqrt{\epsilon_r}}
$$

FR4 的 $\epsilon_r \approx 4.2$:

$$
v_p \approx \frac{3\times10^8}{\sqrt{4.2}} \approx 1.46 \times 10^8 \text{ m/s} \approx 14.6 \text{ cm/ns}
$$

工程上常用**传播延迟** $t_{pd}$ (每单位长度的延迟):

$$
t_{pd} = \frac{1}{v_p} \approx \frac{\sqrt{\epsilon_r}}{c}
$$

FR4 微带线: $t_{pd} \approx 5.5 \sim 6.5 \text{ ps/mm}$ (视有效介电常数而定)

### 3.3.2 信号传输四步曲

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-signal-propagation.png)

**图解读:** 上图展示了信号在传输线上传播的四个阶段. (1) 驱动端发射信号电压进入走线; (2) 电压/电流波以速度 $v_p$
向前传播, 每经过一小段都需要对该段的寄生电容充电并对电感储能; (3) 波前到达负载端; (4) 若负载阻抗与 $Z_0$ 不匹配, 产生反射波返回源端.

**1. 发射:** 驱动端将电压信号注入走线. 如果源端不匹配, 并非全部能量都进入传输线.

**2. 传播:** 电压/电流以速度 $v_p$
沿走线向前推进. 每前进一小段, 都要给这一段的寄生电容充电, 电感储能 -- 这就是 $Z_0$ 的物理感觉.

> **关键理解: 返回电流是瞬时存在的.** 电压施加到传输线入口的瞬间, 信号路径和参考路径之间就产生电位差, 同时伴随电荷积聚, 产生电流. 这不是"信号先到负载再回来" -- 电流在信号传播的每一步都同时存在于信号路径和返回路径中. 外部看起来就像电流从信号路径流入, 从参考路径流回.
>
> **回路越短, 回路电感越小.** 减小回路电感需要将信号线与参考路径靠近, 使互感增大, 回路电感就减小. 高频返回电流之所以集中分布在参考平面的正上方/正下方, 是因为高速信号走阻抗最小的路径, 即回路电感最小的路径.

**3. 到达:** 到达负载端. 如果负载阻抗不等于 $Z_0$, 产生反射.

**4. 响应:** 反射波沿原路返回, 叠加在入射信号上.

往返一次的时间等于 $2 \times T_d$.

其中 $T_d$ 为单向延迟.

---

## 3.4 反射 -- 信号完整性的根源

### 3.4.1 反射系数

负载阻抗和特性阻抗不匹配时, 产生反射.

反射系数:

$$
\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}
$$

几个极端情况:

| 负载情况 | $Z_L$ | $\Gamma$ | 结果 |
|:--|:--|:--|:--|
| 完美匹配 | $Z_0$ | 0 | 无反射 V |
| 开路 | $\infty$ | +1 | 电压翻倍 X |
| 短路 | 0 | -1 | 电压归零 X |
| 轻载 | $> Z_0$ | 正 | 过冲 |
| 重载 | $< Z_0$ | 负 | 下冲 |

**开路时反射最严重:** CMOS 输入端近似高阻 -> 反射系数接近 +1 -> 信号几乎全反射.

### 3.4.2 反射图 (Bounce Diagram)

反射图是分析传输线响应的核心工具. 横轴是距离 (源端到负载端), 纵轴是时间.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-bounce-diagram.png)

**图解读:** 上图是反射图 (Bounce Diagram) 的示意图. 横轴代表从源端到负载端的距离, 纵轴向下代表时间推进. 每条斜线代表一个波前在传输线上的行进路径:

- **第1条线 (入射波 $V_1^+$
)**: 从源端出发, 向右传播到负载端, 耗时 $T_d$ .
- **第2条线 (反射波 $V_1^-$
)**: 在负载端以 $\Gamma_L$
反射, 向左返回源端, 再耗时 $T_d$ .
- **第3条线 (再反射 $V_2^+$
)**: 到达源端后以 $\Gamma_S$ 再次反射, 向右传播.
- 每往返一次 (周期 $2T_d$
), 反射波幅度乘以 $\Gamma_S \times \Gamma_L$
(衰减因子). 当 $|\Gamma| < 1$ 时, 幅度逐次衰减, 最终趋于稳态.

### 实测波形

- 打开示波器, 通道 1 接驱动端, 通道 2 接接收端
- 如果没有端接: 接收端波形有明显过冲 + 振铃

过冲幅度:

$$
V_{peak} = V_0(1 + \Gamma_L)
$$

振铃周期:

$$
T_{ring} = 4 \times T_d
$$

(往返两次为一个周期)

---

## 3.5 阻抗不连续 -- 不止是负载端才反射

很多工程师以为只有线末端会反射. 其实, **任何阻抗变化点都会产生反射.**

### 3.5.1 三种常见不连续

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-impedance-discontinuities.png)

**图解读:** 上图展示了 PCB 设计中三种常见的阻抗不连续场景:
- **过孔 (Via)**: 过孔 Stub (多余的未用段) 引入额外电感 (约 0.5~2 nH 每 0.5mm 长度), 焊盘增加对地电容. 高速 (>5Gbps) 需要做**背钻 (Back Drilling)** 去除 Stub.
- **分支/Stub**: 主传输线上分叉出去一段开路走线, 开路 Stub 等效为一个并联谐振回路. DDR 多颗粒的 Fly-by 拓扑本身就有一串 Stub, 靠端接来抑制反射.
- **连接器**: 连接器的引脚电感 + 信号回流路径变化. SMA 连接器设计为 50 Ohm, 但 PCB 上的过渡段需要仔细处理.

### 3.5.2 不连续的后果

不连续产生反射 -> 反射波与入射波叠加 -> 接收端看到的是**经过了多次反射的复合波形**. 眼图张开度下降, 时序抖动增加.

---

## 3.6 端接技术全解

Day 1 Section 1.8 已经详细讲了源端串联匹配的原理. 这里把四种端接方案做一个完整对比, 并给出选择决策.

### 3.6.1 四种方案总览

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-termination-types.png)

**图解读:** 四种端接方案拓扑对比. (a) 源端串联: Rs 串在驱动端输出; (b) 末端并联: Rt 并联在负载端对地; (c) 戴维南: R1 上拉到 VCC, R2 下拉到 GND, 等效并联阻抗等于 $Z_0$; (d) AC 端接: 电容 C 串联 Rt 到地.

| 方案 | 功耗 | 适用拓扑 | 局限 |
|:--|:--|:--|:--|
| **1. 源端串联** | 极低 | 点对点 | 不适用多负载 |
| **2. 末端并联** | 高 $P=V^2/Z_0$ | 任何 | 直流功耗大 |
| **3. 戴维南** | 中 | 总线, 多负载 | 两个电阻 |
| **4. AC 端接** | 极低 | 低占空比信号 | 低频效果差 |

### 3.6.2 各方案详解

**1. 源端串联匹配 (复习)**

> Day 1 Section 1.8 已详细讲, 这里回顾要点:
> - Rs + Rout = $Z_0$ (驱动端阻抗匹配)
> - 信号以半幅发射 -> 末端全反射叠到满幅 -> 返回源端被吸收
> - 仅适用于**单驱单收**的点对点拓扑
> - 往返延迟内接收端处于中间电平, 走线过长影响时序

**2. 末端并联匹配**

负载端并联 $R_t = Z_0$ 到地.

- V 最大优点: 彻底消除反射, 任何拓扑都适用
- X 最大缺点: $P = V^2/R_t$. 3.3V / 50 Ohm = 0.22W, 一个信号就 0.22W, 32 位总线就是 7W
- 实际很少用于数字信号 (功耗扛不住)
- 射频末端常用 (射频功率本来就要被吸收)

**3. 戴维南端接**

上拉电阻 $R_1$
接 VCC, 下拉电阻 $R_2$
接 GND. 要求 $R_1 \parallel R_2 = Z_0$ .

- V 能驱动总线 (多负载)
- V 功耗比纯并联低 (两个电阻分压降低了等效电压)
- X 还是要消耗直流功耗
- **典型场景: DDR 地址/命令总线, VTT 端接**

**4. AC 端接**

串联电容 C 起隔直作用, 并联电阻 $R_t = Z_0$ 到地. 电容隔直, 只对反射产生的高频分量起作用.

- V 无直流功耗
- V 反射抑制效果好 (高频)
- X 电容需要足够大: $C > \frac{3 \times T_d}{Z_0}$ (保证时间常数 > 往返延迟)
- X 低频/直流分量无抑制
- **典型场景: 射频前端, 时钟分配**

### 3.6.3 二极管钳位 (补充方案)

负载端用肖特基二极管钳位到 VCC 和 GND:
- V 功耗极低
- X 不能消除反射, 只是限制幅度不出供电轨
- **典型场景: 热插拔接口保护, ESD 保护**

### 3.6.4 端接方案选择决策树

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-termination-decision.png)

**图解读:** 端接方案选择决策树. 从左向右: 点对点拓扑 -> 源端串联最省事; 多负载/总线 -> 戴维南; 低占空比/射频 -> AC 端接; 仅需限幅保护 -> 钳位二极管. 90% 的高速数字设计场景用源端串联匹配就够了.

---

## 3.7 微带线 vs 带状线

Day 1 Section 1.6 简单提了"时钟走内层"的好处, 这里讲物理本质.

### 3.7.1 结构对比

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-microstrip-stripline.png)

**图解读:** 上图对比了微带线和带状线的截面结构. 微带线位于 PCB 表层, 下方一个参考平面, 电磁场一部分在 FR4 介质中, 一部分在空气中. 带状线位于 PCB 内层, 上下各有一个参考平面, 电磁场全部在 FR4 介质中.

### 微带线 (Microstrip)
- 走线在 PCB **表层**, 下面一个参考平面
- 电磁场: 一部分在 FR4 介质中 ($\epsilon_r \approx 4.2$
), 一部分在空气中 ( $\epsilon_r \approx 1$ )
- **有效介电常数**取值范围: $1 < \epsilon_{\text{eff}} < 4.2$
- 常用近似值: $\epsilon_{\text{eff}} \approx (\epsilon_r + 1)/2 \approx 2.6$
- 传播速度: $v_p = c/\sqrt{\epsilon_{\text{eff}}}$, 比带状线快

### 带状线 (Stripline)
- 走线在 PCB **内层**, 上下各一个参考平面
- 电磁场**全部**在 FR4 介质中
- 有效介电常数 $= \epsilon_r \approx 4.2$
- 传播速度更慢, 但信号质量更好

### 3.7.2 关键区别

| 特性 | 微带线 | 带状线 |
|:--|:--|:--|
| 传播速度 | 快 (~15 cm/ns) | 慢 (~14 cm/ns) |
| EMI 辐射 | 大 (裸露) | 极小 (屏蔽) |
| 远端串扰 (FEXT) | 有 | **零** (对称结构) |
| 加工精度 | 好控制 | 依赖层压对准 |
| 阻抗控制 | 较简单 | 较复杂 |
| 成本 | 低 (不需要额外层) | 高 (需要完整的上下平面) |

> **远端串扰为零**是带状线最重要的特性. 微带线因为介质不对称, 奇模和偶模传播速度不同, 必然有远端串扰; 带状线上下介质对称, 奇偶模速度相等, FEXT 理论上为零.

### 3.7.3 什么时候用哪个

| 场景 | 选择 |
|:--|:--|
| 普通高速数字 (DDR, SPI, I2S) | 微带线, 除非有 EMI 问题 |
| 时钟信号 (>50MHz) | **带状线**, 消除远端串扰 |
| 射频信号 (>1GHz) | 带状线, 但需用高频板材 |
| 差分高速 (LVDS, PCIe) | 带状线 > 微带线 |
| 两层板 | 只能微带线 (没有内层) |

---

## 3.8 瞬态阻抗与特性阻抗

教材中明确区分了两个容易混淆的概念: **瞬态阻抗**和**特性阻抗**.

### 3.8.1 概念区分

- **瞬态阻抗 (Transient Impedance $Z_i$)**: 信号在传输线上某一点瞬时"感受到"的阻抗. 对于任何传输线 (均匀或非均匀), 瞬态阻抗都存在. 它是电压波前和电流波前在该点的比值.
- **特性阻抗 (Characteristic Impedance $Z_0$)**: 仅存在于**均匀**传输线的固有属性. 只有当传输线截面几何完全一致时, 各点的瞬态阻抗才相等, 这个恒定值就是特性阻抗.

### 3.8.2 非均匀传输线

如果走线宽度在一个区域内变化, 不同位置的瞬态阻抗不同, 此时不存在一个唯一的"特性阻抗".

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-18_nonuniform_tl.png)

**图 3-18 解读:** 上图展示了非均匀传输线的示意图. 走线宽度从左到右不断变化 -- 中间窄, 两端宽. 信号从左向右传播时, 在宽度不同的位置感受到不同的瞬态阻抗. 因为线宽影响单位长度电感和电容 (见 3.9 节), 所以瞬态阻抗随位置变化. 这种非均匀性本身就是阻抗不连续的来源, 会在每个宽度变化点产生反射.

### 3.8.3 影响特性阻抗的四大因素

特性阻抗 $Z_0 = \sqrt{L/C}$
, 因此凡是影响 $L$
和 $C$
的因素都会改变 $Z_0$ .

**(a) 线宽 (W)**

线宽增大 -> 单位长度电感 $L$
减小, 单位长度电容 $C$
增大 -> $Z_0$ 减小.

线宽减小 -> $L$
增大, $C$
减小 -> $Z_0$ 增大.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-20_linewidth_LC.png)

**图 3-20 解读:** 上图展示了 FR4 板材 ($\epsilon_r=4.4$), 介质厚度 3.6 mil 的条件下, 表层微带线的单位长度电感和电容随线宽的变化. 横轴为线宽 (mil), 纵轴分别为电感 (nH) 和电容 (pF). 线宽从 4 mil 增加到 12 mil 时, 电感从约 9.0 nH/inch 下降到约 7.2 nH/inch, 电容从约 1.8 pF/inch 上升到约 3.2 pF/inch.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-21_linewidth_Z0.png)

**图 3-21 解读:** 上图展示了特性阻抗随线宽的变化关系. 横轴为线宽 (mil), 纵轴为特性阻抗 (Ohm). 线宽 4 mil 时阻抗约 61.5 Ohm, 线宽 12 mil 时降至约 33 Ohm. 可见线宽对特性阻抗的影响非常显著 -- 线宽增减 1 mil, 阻抗变化约 3.5 Ohm.

**(b) 介质厚度 (H)**

走线与参考平面之间的距离. H 越大 -> $L$
增大, $C$
减小 -> $Z_0$ 增大.

H 越小 -> $L$
减小, $C$
增大 -> $Z_0$ 减小.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-22_thickness_LCZ.png)

**图 3-22 解读:** 上图展示了在 $\epsilon_r=4.4$, 线宽 6 mil 条件下, 介质厚度从 4 mil 增加到 12 mil 时, 单位长度电感, 电容和特性阻抗的变化. (a) 电感从约 6.5 nH/inch 增至约 9 nH/inch; (b) 电容从约 3.2 pF/inch 降至约 2.2 pF/inch; (c) 特性阻抗从约 42 Ohm 升至约 60 Ohm.

**(c) 介电常数 ($\epsilon_r$)**

$\epsilon_r$
增大 -> 单位长度电感 $L$
基本不变 (磁场不受介质影响), 电容 $C$
增大 -> $Z_0$ 减小.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-23_dielectric_effect.png)

**图 3-23 解读:** 上图展示了介电常数从 3.2 变化到 4.6 时 (线宽 6 mil, 介质厚度 3.6 mil): (a) 电感基本恒定在 7.8 nH/inch 左右; (b) 电容从约 1.9 pF/inch 增至约 2.7 pF/inch; (c) 特性阻抗从约 62 Ohm 降至约 51 Ohm. 更换板材时, 介电常数变化会直接影响阻抗.

**(d) 铜箔厚度 (T)**

铜箔厚度 T 增大 -> $L$
减小, $C$
增大 (边缘场增强) -> $Z_0$ 减小. 铜箔越厚, 电感越小.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-24_copper_full.png)

**图 3-24 解读:** 上图展示了铜箔厚度从 0.7 mil (0.5 oz) 增加到 2.8 mil (2.0 oz) 时 ($\epsilon_r=4.4$, 线宽 6 mil, 介质厚度 3.6 mil): (a) 电感从约 8.0 nH/inch 降至约 7.5 nH/inch; (b) 电容从约 2.3 pF/inch 增至约 2.6 pF/inch; (c) 特性阻抗从约 56 Ohm 降至约 52 Ohm. 铜箔厚度增加 4 倍, 阻抗变化约 4 Ohm.

---

## 3.9 参考平面

### 3.9.1 参考平面的定义与作用

与走线处于不同层, 以平面形式出现的"参考路径". 它的核心作用是与信号走线一起构成完整的**传输线结构**.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-25_field_distribution.png)

**图 3-25 解读:** 上图展示了两种传输线的电磁场分布. (a) 微带线: 信号线在上表面, 参考平面在下. 电场 (E) 从信号线指向参考平面, 磁场 (H) 围绕信号线呈环形闭合. (b) 带状线: 信号线在上下两个参考平面之间, 电场从信号线指向两侧平面, 磁场也围绕信号线对称分布.

### 3.9.2 关键认知

- 不一定必须是 GND 平面. **任何与走线相邻的平面导体** (如 VCC, 独立铜层) 都可作为参考平面.
- 参考平面不一定要连接电源或地网络, 但必须是**连续, 完整的导体平面**.
- 参考平面的连续性直接影响阻抗控制和信号质量.

---

## 3.10 返回电流的分布

### 3.10.1 返回电流不是均匀分布的

返回电流在参考平面上**不是均匀分布**的, 而是集中在走线正下方附近. 距离走线中心水平距离为 $d$ 处的电流密度:

$$
i(d) = \frac{I_0}{\pi h} \cdot \frac{1}{1 + (d/h)^2}
$$

其中 $I_0$
为信号电流, $h$
为走线与参考平面之间的介质厚度, $d$ 为评估点到走线中心的水平距离.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-26_return_current.png)

**图 3-26 解读:** 上图展示了微带线返回电流在参考平面上的分布. 横轴为归一化距离 $d/h$
, 纵轴为归一化电流密度 $i(d)/i_{max}$
. 在走线正下方 ( $d=0$
) 电流密度最大; 当 $d = 3h$
时, 电流密度降至最大值的 10%; $d = 7h$
时降至 2%; $d = 10h$ 时仅剩 1%. 这表明: 返回电流的绝大部分都集中在走线正下方一个很窄的带状区域内.

**工程意义:**
- 走线下方约 $3h$ 宽度的区域必须保留完整的参考平面 (不挖空, 不分割)
- 如果参考平面在此区域有缝隙, 返回电流路径被迫绕行, 等效回路电感剧增, 产生严重的 EMI 和信号质量恶化

### 3.10.2 带状线的返回电流

带状线有上下两个参考平面, 返回电流分布在走线正上方和正下方两个平面上.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-27_stripline_return.png)

**图 3-27 解读:** 上图展示了带状线返回电流在两个平面上的分布. 和微带线类似, 电流集中在走线正上方和正下方. 由于上下对称, 上下平面的电流分布对称.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-28_return_ratio.png)

**图 3-28 解读:** 上图展示了当走线与下方平面间距 $H$
变化时, 上方平面上返回电流占总返回电流的比例. 横轴为间距 $H$
(mil), 纵轴为比例 (%). 间距越大, 返回电流越集中在更近的平面上. 例如 $H=40$ mil 时, 上方平面占比 20%, 下方平面占比 80%. 典型分配比例为 1:4 (近:远).

### 3.10.3 走线同层铜皮上的返回电流

除了参考平面, 走线同层的铜皮也会承载一小部分返回电流.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-29_adjacent_return.png)

**图 3-29 解读:** 上图展示了一个 50 Ohm 阻抗控制的表层微带线, 信号电流 10 mA 时: 参考平面返回电流最大 8 mA (80%), 走线两侧同层铜皮各承载约 1 mA (各 10%). 大部分返回电流从参考平面返回, 走线两侧铜皮返回电流占比很小.

---

## 3.11 理想传输线的集总参数模型

### 3.11.1 分段建模的原理

对于长传输线, 可以用多个 LC 单元级联来近似模拟. 每一段 $\Delta z$
用一个串联电感 $L_{\Delta z}$
和一个并联电容 $C_{\Delta z}$ 表示.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-30_lumped_model.png)

**图 3-30 解读:** 理想传输线的集总参数模型示意图. 整段传输线被分割成多段, 每段包含一个串联电感 $L_{\Delta z}$
和并联电容 $C_{\Delta z}$ . 信号从左向右传播, 每经过一段都要给该段的电容充电并使电感储能.

**分段长度的经验法则:**

$$
\Delta z \leq \frac{\lambda_{max}}{10}
$$

其中 $\lambda_{max}$ 是信号中最高感兴趣频率对应的波长. 例如信号带宽 350 MHz 对应波长约 17 inch, 则每段长度应小于 1.7 inch.

### 3.11.2 开短路输入阻抗法测 $Z_0$

传输线的特性阻抗可以通过测量开路和短路输入阻抗来间接得到:

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-33_open_short_impedance.png)

**图 3-33 解读:** 上图展示了短传输线的开短路等效电路模型. (a) 末端开路时, 低频下输入阻抗近似为电容的阻抗: $Z_{in\_open} \approx 1/(j\omega C)$
. (b) 末端短路时, 输入阻抗近似为电感的阻抗: $Z_{in\_short} = j\omega L$ . 两者相乘取平方根即得特性阻抗:

$$
Z_0 = \sqrt{Z_{in\_open} \times Z_{in\_short}}
$$

这一关系在高频下也精确成立.

---

## 3.12 耦合传输线与奇偶模分析

### 3.12.1 相邻走线之间的耦合

两条相邻的平行走线之间存在互容 ($C_m$
) 和互感 ( $L_m$ ), 导致信号耦合 (串扰).

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-34_coupled_tl.png)

**图 3-34 解读:** 上图展示了两条平行信号线 (1 和 2) 与参考平面 (0) 之间的寄生参数. 每条线对地有自容 $C_0$
和自感 $L_0$
, 两条线之间有互容 $C_m$
和互感 $L_m$ . 这些寄生参数构成了串扰的物理基础.

### 3.12.2 三种工作模态的阻抗

对于耦合传输线, 根据邻近信号线的跳变方向, 可分为三种工作模态:

- **奇模 (Odd Mode)**: 两条线信号反向跳变 (一个上升, 一个下降, 如差分信号). 等效电感 $L = L_0 - L_m$
(减小), 等效电容 $C = C_0 + C_m$
(增大), 因此 $Z_{odd} < Z_0$ .
- **偶模 (Even Mode)**: 两条线信号同向跳变 (同时上升或同时下降). 等效电感 $L = L_0 + L_m$
(增大), 等效电容 $C = C_0$
(互容无影响), 因此 $Z_{even} > Z_0$ .
- **静态 (Quiet Mode)**: 邻近线静止不动. 接近孤立线阻抗 $Z_0$.

阻抗大小关系恒成立:

$$
Z_{odd} < Z_{quiet} < Z_0 < Z_{even}
$$

### 3.12.3 线间距对阻抗的影响

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-35_modal_impedance.png)

**图 3-35 解读:** 上图展示了基于 50 Ohm 阻抗控制的表层微带线 (线宽 6 mil, 介质厚度 3.6 mil, $\epsilon_r=4.4$
, 铜厚 1.2 mil) 的各模态阻抗值: $Z_{odd}=44.6$
Ohm, $Z_{quiet}=49.7$
Ohm, $Z_0=50.6$
Ohm, $Z_{even}=54.8$
Ohm. 验证了 $Z_{odd} < Z_0 < Z_{even}$ 的关系.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-36_gap_impedance.png)

**图 3-36 解读:** 上图展示了表层微带线间距对奇模/偶模/静态阻抗的影响. 横轴为线间距 (归一化为介质厚度 $h$ 的倍数), 纵轴为阻抗 (Ohm). 三条曲线:
- $Z_{odd}$
(实线): 间距越小, 耦合越强, $Z_{odd}$
越低; 间距 > 10h 时接近 $Z_0$ .
- $Z_{even}$
(虚线): 间距越小, $Z_{even}$
越高; 间距 > 10h 时接近 $Z_0$ .
- $Z_{quiet}$ (点划线): 基本稳定在 50 Ohm 附近, 受间距影响较小.

**工程意义:**
- 差分对设计: 要利用奇模特性, 需要将线间距控制在小范围, 使 $Z_{odd}$ 等于目标差分阻抗的一半
- 串扰控制: 间距 > 3h 时耦合已显著减弱, > 10h 时可忽略
- 阻抗设计: 计算单端阻抗时, 需考虑邻近线的影响; 设计工具应使用偶模/奇模参数而非孤立线参数

---

## 3.13 TDR -- 时域反射计

### 3.13.1 TDR 是什么?

TDR 是测量传输线阻抗沿长度分布的仪器.

**原理:** 发射一个上升沿极快的脉冲 (Tr 通常是皮秒级) 到待测传输线 -> 测量反射回来的波形 -> 根据反射系数反算出各位置的阻抗.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-tdr-principle.png)

**图解读:** TDR 工作原理示意图. 阶跃脉冲发生器向待测传输线发射一个陡峭的上升沿, 同时采样器监测反射电压. 反射电压 $V_{reflected} = \Gamma \times V_{incident}$
, 通过 $\Gamma$
反算出阻抗 $Z = Z_0 \times (1+\Gamma)/(1-\Gamma)$
. 时间轴映射到距离轴 $d = v_p \times t/2$ .

### 3.13.2 TDR 能干什么?

- **测量 PCB 走线阻抗**: 板厂用 TDR 做阻抗测试, 确保 50 Ohm +/- 10%
- **定位不连续点**: 连接器, 过孔处的阻抗跳变在 TDR 上清清楚楚
- **测差分阻抗**: TDR 有差分模式, 可以直接测出 $Z_{diff}$
- **检查电缆质量**: 断点, 压接不良处表现为阻抗尖峰

### 3.13.3 读 TDR 波形

- **平台** -> 均匀阻抗段 (正常)
- **向上台阶** -> 阻抗突然变大 (走线变窄, 过孔电感)
- **向下台阶** -> 阻抗突然变小 (走线变宽, 对地电容大)
- **向上尖峰** -> 感性不连续 (过孔 stub, 连接器引脚)
- **向下凹陷** -> 容性不连续 (大焊盘, 测试点)

```
阻抗↑ = 容性负载? 还是窄线? -> 看波形形状判断
阻抗↓ = 感性负载? 还是宽线? -> 感性是尖峰, 宽线是平台
```

---

## 3.14 阻抗控制实践

### 3.14.1 阻抗由什么决定 (再复习)

$$
Z_0 \approx \frac{87}{\sqrt{\epsilon_r + 1.41}} \times \ln\left(\frac{5.98 \times H}{0.8W + T}\right)
$$

| 参数变化 | $Z_0$ 变化 | 直觉 |
|:--|:--|:--|
| 线宽 $W \uparrow$ | $\downarrow$ | 线宽了, 电容大了, 阻抗低 |
| 介质厚度 $H \uparrow$ | $\uparrow$ | 离地远了, 电容小了, 阻抗高 |
| 介电常数 $\epsilon_r \uparrow$ | $\downarrow$ | 电容大, 阻抗低 |
| 铜厚 $T \uparrow$ | $\downarrow$ | 影响很弱 |

### 3.14.2 叠层设计

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/03-stackup-4layer.png)

**图解读:** 典型 4 层板叠层 (S-G-P-S). L1 (TOP) 和 L4 (BOTTOM) 为信号层, L2 (GND) 为地层, L3 (PWR) 为电源层. L1 到 L2 的介质厚度 H 决定顶层走线的特性阻抗. 这个距离在 PP 片选型和压合工艺时就确定了.

**典型 4 层板叠层 (S-G-P-S):**

| 层 | 材料 | 典型厚度 |
|:--|:--|:--|
| L1 - TOP | 铜箔 | 35um (1oz) |
| PP 半固化片 | FR4 预浸料 | ~0.1mm |
| L2 - GND | 铜箔 | 35um |
| Core 芯板 | FR4 | ~1.0mm |
| L3 - PWR | 铜箔 | 35um |
| PP 半固化片 | FR4 预浸料 | ~0.1mm |
| L4 - BOTTOM | 铜箔 | 35um |

### 3.14.3 实际工作流

**你不需要手算阻抗.** 你只需要告诉板厂:

1. 叠层结构 (几层板, 每层干啥)
2. 阻抗要求 (50 Ohm 单端, 100 Ohm 差分等)
3. 板厂回复你需要的线宽和线间距

你会用 Polar SI9000 或板厂的在线工具预先估算, 但最终以板厂的回答为准.

### 3.14.4 实战 tips

- **参考平面必须连续**: 高速信号下方不能跨过电源层的分割
- **换层时伴随参考平面**: L1 换到 L3 (都参考 L2 GND) 比 L1 换到 L4 (参考平面变了) 安全
- **阻抗控制线走 50 Ohm 之前**, 先确认你的板厂能不能做 (一般都能, 但公差 +/- 10% 要心里有数)
- **差分对间距**: 告诉板厂你要 100 Ohm 差分, 他们会告诉你线宽和线间距的值

---

## 3.15 有损传输线 -- 损耗机制详解

前面都假设传输线是无损的 ($R=G=0$). 对于 >5Gbps 或长距离的情况, 损耗不能忽略. 教材详细分析了四种损耗机制.

### 3.15.1 导体损耗 -- 趋肤效应

高频电流只在导体表面薄层流动, 这一现象称为**趋肤效应**.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-38_skin_effect.png)

**图 3-38 解读:** 上图展示了 8 mil 线宽, 2 oz (2.8 mil) 厚的矩形铜导体在 100 MHz 时的电流分布. 颜色越亮表示电流密度越大. 可以看到电流几乎全部集中在导体表面的薄层内, 中心部分电流密度极小.

**趋肤深度 $\delta$:**

$$
\delta = \sqrt{\frac{1}{\pi f \mu \sigma}}
$$

对铜导体: $\mu = 4\pi \times 10^{-7}$
H/m, $\sigma = 5.8 \times 10^7$ S/m

$$
\delta(\mu m) = \frac{66}{\sqrt{f(GHz)}}
$$

例如 1 GHz 时 $\delta \approx 2.1 \mu m$
, 10 GHz 时 $\delta \approx 0.66 \mu m$ .

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-39_skin_depth.png)

**图 3-39 解读:** 上图展示了铜导体的趋肤深度随频率的变化关系. 横轴为频率, 纵轴为趋肤深度. 低频时趋肤深度很大 (电流布满整个截面), 高频时迅速减小. 注意纵轴为对数坐标.

**直流电阻 vs 交流电阻:**

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-40_dc_resistance.png)

**图 3-40 解读:** 不同线宽铜走线的直流电阻. 横轴为线宽, 纵轴为直流电阻. 线宽越宽, 直流电阻越小. 这只是基线, 高频时交流电阻会远大于此.

$$
R_{dc} = \frac{1}{\sigma A},\quad R_{ac} = \frac{1}{\sigma \delta p} \propto \sqrt{f}
$$

其中 $p = 2(w+t)$
为截面周长. $R_{ac} \propto \sqrt{f}$ 意味着频率每增加 10 倍, 交流电阻增加约 3.16 倍.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-41_ac_resistance.png)

**图 3-41 解读:** 上图展示了交流电阻随频率的变化. 低频时电阻接近 $R_{dc}$
, 高频时 $R_{ac}$
以 $\sqrt{f}$
的斜率增加. 宽走线由于周长大, $R_0$ 小, 整体损耗较低.

### 3.15.2 邻近效应

信号线与参考平面靠近时, 高频电流进一步重新分布: 信号线上的电流集中分布在靠近参考平面的一侧, 参考平面上的电流也靠近信号线分布.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-42_proximity_effect.png)

**图 3-42 解读:** 上图展示了邻近效应下的电流分布. 信号线上的高频电流 (红色箭头) 集中在靠近参考平面的下表面; 参考平面上的返回电流 (蓝色箭头) 集中在靠近信号线的上表面. 两者彼此"吸引", 这是电磁场相互耦合的结果.

引入系数 $K_p$ 表示邻近效应的影响:

$$
R_{AC} = \frac{K_p R_0}{\sqrt{f_0}} \cdot \sqrt{f},\quad \alpha_c = \frac{1}{2} \cdot \frac{K_p R_0}{Z_0} \cdot \sqrt{\frac{f}{f_0}}
$$

走线距参考平面越近, $K_p$ 越大, 损耗越严重.

### 3.15.3 表面粗糙度

实际 PCB 铜箔表面并非光滑, 存在微小突起 (毛刺).

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-43_surface_roughness.png)

**图 3-43 解读:** (a) PCB 切片中信号线和铜平面的横截面放大图, 显示铜导体表面有很多毛刺; (b) 表面显微结构. 这些毛刺的 RMS 通常在 0.3~5.8 um 之间. 当趋肤深度 $\delta$ 与粗糙度 RMS 值相当时, 粗糙表面对损耗的影响显著增加.

**粗糙度修正系数 $K_{SR}$:**

$$
K_{SR} = 1 + \frac{2}{\pi} \arctan\left[1.4 \left(\frac{\Delta}{\delta}\right)^2\right]
$$

其中 $\Delta$
为表面粗糙度 RMS 值. 直流下 $K_{SR}=1$ , 高频时最大可达 2.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-45_KSR_plot.png)

**图 3-45 解读:** 四种不同 RMS 粗糙度下 $K_{SR}$
随频率的变化. 横轴为频率 (GHz), 纵轴为 $K_{SR}$
. RMS 越大, $K_{SR}$
增长越快. RMS=2 um 时, 10 GHz 下 $K_{SR}$ 接近 2 (损耗翻倍).

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-46_loss_roughness.png)

**图 3-46 解读:** 一条 10 inch 走线在不同表面粗糙度下的衰减. 横轴为频率 (GHz), 纵轴为衰减 (dB). 5 GHz 处, RMS=2 um 的粗糙表面比光滑表面额外增加约 2 dB 衰减. 10 Gbps 以上设计必须关注铜箔表面粗糙度.

### 3.15.4 介质损耗

介质在交变电场中消耗能量的现象.

**极化机制:**
- **取向极化**: 极性分子 (如水分子) 在外电场作用下转向电场方向, 需要消耗能量来"拖动"分子转向
- **位移极化**: 非极性分子的正负电荷中心在外电场作用下发生位移, 形成偶极子

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-47_orientation_polarization.png)

**图 3-47 解读:** 取向极化示意图. (a) 未加外电场时, 极性分子随机取向; (b) 施加外电场后, 极性分子沿电场方向重新排列. 电场改变方向时需要能量来"拖动"分子跟上变化, 这部分能量以热量形式耗散.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-48_displacement_polarization.png)

**图 3-48 解读:** 位移极化示意图. 非极性分子在无外电场时正负电荷中心重合; 施加外电场后, 正负电荷中心发生相对位移, 形成偶极子. 电场变化时也需要做功来持续改变偶极子的方向.

### 3.15.5 复介电常数与有损传输线模型

介质损耗用复介电常数描述:

$$
\epsilon = \epsilon' - j\epsilon''
$$

其中 $\epsilon'$
决定信号速度 (储能), $\epsilon''$ 表示损耗 (耗能).

工程参数: $Dk = \epsilon_r = \epsilon'/\epsilon_0$
(介电常数), $Df = \epsilon''/\epsilon'$ (损耗因子).

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-49_loss_tangent.png)

**图 3-49 解读:** 损耗角示意图. $\delta$
是损耗角, $\tan\delta = \epsilon''/\epsilon' = Df$
就是通常说的损耗角正切. FR4 的 $\tan\delta \approx 0.02$ , Rogers 4350B 约 0.0037.

有损传输线的完整模型包含 $R$
和 $G$ :

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-50_lossy_RLCG.png)

**图 3-50 解读:** 有损传输线的集总参数模型. 相比无损模型的 LC 单元, 增加了串联电阻 $R\Delta z$
(导体损耗) 和并联电导 $G\Delta z$ (介质损耗).

有损传输线的特性阻抗与频率相关:

$$
Z_0 = \sqrt{\frac{R + j\omega L}{G + j\omega C}}
$$

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-51_lossy_Z0.png)

**图 3-51 解读:** 有损传输线特性阻抗随频率变化的趋势. 低频时 $|Z_0|$
较大 (因为 $R$
和 $G$
的影响显著), 高频时趋近于无损线阻抗 $\sqrt{L/C}$
. 在 GHz 以上, 实际 $Z_0$ 与无损近似基本一致, 这正是数字 SI 分析中常采用无损近似的依据.

![](https://raw.githubusercontent.com/tt1431/hardware-study-plan/main/assets/si_textbook_diagrams/ch3_fig3-52_lossy_velocity.png)

**图 3-52 解读:** 有损传输线中信号传播速度随频率的变化. 不同频率分量以不同速度传播, 导致**色散** (波形展宽). 这是高速长距离互连 (如背板) 中信号恶化的重要原因之一.

### 3.15.6 FR4 的极限

| 信号速率 | FR4 还能用吗? |
|:--|:--|
| < 1Gbps | V 没问题 |
| 1~5Gbps | V 可以, 长度 < 50cm 问题不大 |
| 5~10Gbps | W 短走线还行, 长了要考虑损耗 |
| 10~25Gbps | X 需要低损耗板材 (Megtron 6, Rogers) |
| > 25Gbps | X 必须用超低损耗板材 + 精密设计 |

---

## 3.16 本章小结

传输线理论的核心链条:

```
Tr -> BW (Day2) -> 高频分量在走线里的行为 (Day3) -> 反射/端接/SI 问题
```

**必须记住的几个数字:**

| 量 | 值 | 用途 |
|:--|:--|:--|
| $Z_0$ 标准 | 50 Ohm | 单端信号默认阻抗 |
| $Z_{diff}$ 标准 | 100 Ohm | 差分信号默认阻抗 |
| FR4 $\epsilon_r$ | 4.0~4.5 | 阻抗/延迟计算 |
| FR4 微带线 $v_p$ | ~15 cm/ns | 延迟估算 |
| FR4 微带线 $t_{pd}$ | ~5.5~6.5 ps/mm | 走线长度 -> 延迟 |
| 临界长度 | $T_r(\text{ns}) \times 2.5$ cm | 判断是否需要端接 |
| 趋肤深度 (1 GHz) | ~2.1 um | 判断是否需要考虑导体损耗 |
| FR4 $\tan\delta$ | ~0.02 | 判断是否需要考虑介质损耗 |

**必须记住的几个原则:**

1. 临界长度判据: $L > T_r \times v_p / 6$ -> 走线已是传输线
2. 反射系数: $\Gamma = (Z_L - Z_0)/(Z_L + Z_0)$
3. 源端串联: 点对点场景最省事的方案
4. 微带线 vs 带状线: 表层快但有干扰, 内层干净但慢
5. 参考平面连续性: 高速信号下方地平面不能断
6. 返回电流分布: 集中在走线正下方约 $3h$ 宽度内
7. 奇偶模阻抗: $Z_{odd} < Z_0 < Z_{even}$, 差分对设计的基础
8. 有损传输线: 三种损耗 (趋肤, 介质, 粗糙度) 按 $\sqrt{f}$ 增长
9. 阻抗交给板厂算: 你定目标, 定叠层 -> 板厂给线宽

---

## 面试/工程问题

**1. 面试题: 什么时候必须把 PCB 走线当作传输线来处理?**

答: 当走线物理长度超过临界长度 $L_{critical} \approx T_r \times v_p / 6$
时. 对 FR4 微带线 ( $v_p \approx 15$
cm/ns), 临界长度可简化为 $T_r(\text{ns}) \times 2.5$ cm. 例如 Tr=1 ns 时, 走线超过 2.5 cm 就要当传输线处理. 关键不是时钟频率, 而是**上升时间**.

**2. 面试题: 什么是奇模阻抗和偶模阻抗? 为什么差分对要用奇模阻抗?**

答: 两条邻近走线信号反向跳变时为奇模, 此时等效电感减小 ($L_0 - L_m$
), 等效电容增大 ( $C_0 + C_m$
), 因此 $Z_{odd} < Z_0$
. 信号同向跳变时为偶模, $Z_{even} > Z_0$
. 差分信号的本质就是奇模传输, 差分阻抗 $Z_{diff} = 2 \times Z_{odd}$
. 因此差分对设计的目标是实现特定的 $Z_{odd}$
(如 50 Ohm 单端 -> $Z_{diff}=100$ Ohm).

**3. Layout 常见坑: 高速信号换层时, 返回电流路径被切断, 会有什么后果?**

答: 如果高速信号从 L1 换到 L4, 但 L1 参考 L2 GND, L4 参考 L3 PWR, 返回电流必须通过过孔在参考平面之间跳转. 如果两个参考平面之间没有足够的旁路电容提供低阻抗路径, 返回电流被迫绕行, 回路电感增大, 造成: (1) 信号完整性问题 (过冲, 振铃); (2) EMI 辐射增大. 正确做法: 换层时确保伴随同一参考平面, 或在换层位置附近放置去耦电容.

**4. 调试题: 用 TDR 测一条 PCB 走线, 波形先有一个向上的尖峰, 然后是一个平台, 这是什么情况?**

答: 向上的尖峰表示该处阻抗突然增大 -> 感性不连续, 很可能是过孔 Stub 或连接器的引脚电感. 之后的平台表示走线阻抗均匀 (正常段). 如果尖峰之后还有明显下降, 可能是容性不连续 (焊盘, 测试点). 通过 TDR 波形可以精确定位阻抗不连续点的位置和性质.

**5. 工程实践: 10 Gbps 信号在 50 cm 长的 FR4 走线上传输, 你预计会遇到什么问题?**

答: 主要问题: (1) 趋肤效应: 10 GHz 时趋肤深度 < 1 um, 交流电阻远大于直流电阻; (2) 介质损耗: FR4 的 $\tan\delta \approx 0.02$, 50 cm 长走线累积衰减可能达到 5~10 dB; (3) 表面粗糙度: 若铜箔 RMS > 1 um, 额外增加 2~3 dB 衰减; (4) 色散: 不同频率分量速度不同, 波形展宽. 总体效果是眼图闭合, 可能需要使用低损耗板材 (如 Megtron 6) 或增加均衡 (Equalization).

---

> 下一章: Day 4 -- 信号完整性实战: 反射与端接, 眼图, 串扰, 过孔效应, 电源完整性入门.
