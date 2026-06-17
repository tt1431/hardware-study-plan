# 阶段二：硬件接口（第 15-21 天）

> 🎯 **目标**：掌握常用硬件接口协议原理、电气特性、PCB设计要点
> 📖 **主读资料**：`硬件接口总结.docx`

---

## 第 15 天：UART + RS232/RS485 + I2C

**学习内容：**
- UART 三线制、波特率、连接方式
- RS232 负电平逻辑 vs RS485 差分逻辑
- I2C 协议（开漏/上拉/ACK/速率/容性负载）
- 推挽 vs 开漏对比

**产出笔记：** `notes/day15-uart-i2c.md`

---

## 第 16 天：SPI + CAN

**学习内容：**
- SPI 四线制、主从关系、时钟极性和相位
- SPI vs I2C 对比表格
- CAN 差分电平、120Ω匹配电阻、速率

**产出笔记：** `notes/day16-spi-can.md`

---

## 第 17 天：USB 2.0 + USB 3.0

**学习内容：**
- USB 2.0 信号线（D+/D-）、NRZI 编码、位填充
- 低速/全速/高速的识别方式（上拉电阻）
- USB 2.0 PCB 设计要点（90Ω差分/等长5mil）
- USB 3.0 架构变化（全双工、独立TX/RX对）
- AC 耦合电容 100nF

**产出笔记：** `notes/day17-usb2-usb3.md`

---

## 第 18 天：USB Type-C + PD

**学习内容：**
- CC 检测原理（Rp/Rd/Ra）
- DFP/UFP/DRP 角色
- 正反插识别机制
- USB PD 协议简介
- eMarker 芯片

**产出笔记：** `notes/day18-usb-type-c-pd.md`

---

## 第 19 天：以太网接口（MII/RMII/GMII/RGMII/SGMII）

**学习内容：**
- MAC + PHY + 网络变压器架构
- MDIO 管理接口
- MII（16线）→ RMII（8线）→ GMII（24线）→ RGMII（14线）演进
- SGMII 串行化
- PCB 布局要点（差分100Ω/变压器挖空/等长）

**产出笔记：** `notes/day19-ethernet-rgmii.md`

---

## 第 20 天：PCIe

**学习内容：**
- PCIe 端到端拓扑、Lane 概念
- AC 耦合电容、CDR 时钟恢复
- 三种参考时钟架构（Common/Separate/Data Clock）
- SSC 扩频原理
- 电源管理状态（L0/L0s/L1/L2）
- SerDes 基础概念

**产出笔记：** `notes/day20-pcie.md`

---

## 第 21 天：MIPI + HDMI + DDR

**学习内容：**
- MIPI D-PHY（HS高速/LP低功耗、DDR双沿采样）
- MIPI 状态码（HS-0/HS-1/LP-00~11）
- HDMI TMDS 传输 + 握手流程（5V→HPD→EDID）
- DDR 8 位预取、核心/工作/等效频率
- 阶段二总结

**产出笔记：** `notes/day21-mipi-hdmi-ddr.md`
