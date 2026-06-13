# GitHub MathJax 公式渲染边界测试

> 目标：系统性找出哪些写法会触发渲染失败

---

## 测试 1：$ 同行多对

$A = B$, $C_D$, $E^+$, $\alpha$, $\beta$, $\Gamma$, $\epsilon_r$, $Z_0$

## 测试 2：$ 同行多对 + 中文夹杂

信号 $V_{in}$ 经过电阻 $R_s$ 后，在 $Z_0$ 传输线上传播。到达 $Z_L$ 时产生 $\Gamma$ 的反射。

## 测试 3：中文在 $ 里面（合并写法）

负载阻抗 $Z_L = 50\Omega$ 与特性阻抗不匹配。

参数 $R_1 上拉 VCC，R_2 下拉 GND$ 决定偏置。

## 测试 4：$ 紧贴中文标点

（$V_{peak}$）和（$T_{ring}$）的测量方法。

## 测试 5：$ 在行首

$x = y$ 是一个简单等式。

## 测试 6：$ 在行尾（最后一个字符）

反射系数为 $\Gamma$。

## 测试 7：长公式 inline

$V_{peak} = V_0(1 + \Gamma_L)$，$\Gamma_S \times \Gamma_L$，$|\Gamma| < 1$。

## 测试 8：\text 含中文 in $$

$$
\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0} \quad \text{反射系数公式}
$$

## 测试 9：\text 不含中文 in $$

$$
V_{peak} = V_0(1 + \Gamma_L) \quad \text{(overshoot)}
$$

## 测试 10：$ 含中文标点在公式间

参数 $\epsilon_r \approx 4.2$，$\epsilon_{\text{eff}} \approx 2.6$。

## 测试 11：单个 $ 含多个 \text

$T_r(\text{ns}) \times 2.5$ cm 和 $t_{pd} \approx 5.5 \sim 6.5 \text{ ps/mm}$。

## 测试 12：$ 前后紧贴 Markdown 格式

**$Z_0 = 50\Omega$** 是标准阻抗。

~~不要用 $Z_0 = 75\Omega$~~。

## 测试 13：$ 在列表项行首

- $R_{out} + R = Z_0$
- 正常：$V_{in} = 3.3V$

## 测试 14：$ 含 \left \right

$\ln\left(\frac{5.98H}{0.8W+T}\right)$ 是近似公式。

## 测试 15：$ 含 _ 连续多个

$V_1^+$ 和 $V_1^- = V_1^+ \times \Gamma_L$ 的关系。

## 测试 16：$$ 中公式含 _ 和 ^

$$
L_{critical} \approx \frac{T_r}{6} \times v_p
$$

$$
v_p \approx \frac{3\times10^8}{\sqrt{4.2}} \approx 1.46 \times 10^8 \text{ m/s}
$$

## 测试 17：$$ 中公式含 \left \right

$$
Z_0 \approx \frac{87}{\sqrt{\epsilon_r + 1.41}} \times \ln\left(\frac{5.98 \times H}{0.8W + T}\right)
$$

## 测试 18：$$ 紧贴中文

$$
\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}
$$
其中 $Z_L$ 是负载阻抗。

## 测试 19：列表 + 多 $ 同行

- 参数 $R_1$ 上拉，$R_2$ 下拉，要求 $R_1 \parallel R_2 = Z_0$。
- 电容 $C$ 隔直，电阻 $R_t$ 取值 $Z_0$。

## 测试 20：中文在 $ 内（长句）

反射波 $V_1^- = V_1^+ \times \Gamma_L，从负载端反射回源端，再耗时 T_d$。

## 测试 21：中文在 $ 内（短句）

参数 $R_1 和 R_2$ 并联。

## 测试 22：纯 ASCII 无中文行

The signal $V_{in}$ propagates through $Z_0$ to $Z_L$, generating $\Gamma = (Z_L - Z_0)/(Z_L + Z_0)$.

## 测试 23：$ 含 \parallel

要求 $R_1 \parallel R_2 = Z_0$ 且 $V_{bias} = V_{cc}/2$。

## 测试 24：$ 含 \uparrow \downarrow

当 $W \uparrow$ 时 $Z_0 \downarrow$。

## 测试 25：$ 含 \infty

$Z_L = \infty$ 时 $\Gamma = +1$。

---

> 请逐一标注每个测试的渲染结果：✅ 正常 / ❌ 失败
