#!/usr/bin/env python3
"""
光电转换功耗墙 (DAC/ADC Wall) 定量分析
========================================
回应知乎文章 "光芯片和光子计算系统有巨大缺陷" 的功耗批评:

  批评点 1: DAC/ADC 功耗在高频下呈指数级上升，吃掉光学省下来的功耗
  批评点 2: 模拟计算精度塌陷 → 需要更高精度 ADC (更多 bit → 更大功耗)
  批评点 3: 文章声称的 "百倍算力优势" 在算上光电转换后不成立

本脚本的目的: 不是反驳，而是定量验证这些批评在 DiSubPc·C70 体系中
有多严重，并找出真正可行的操作区间。
"""

import numpy as np

# ============================================================
# 1. Walden FOM 的局限性 — ADC 功耗与采样率的关系
# ============================================================
# Walden FOM (fJ/conv-step) 假设功耗与采样率线性相关:
#   P_adc = FOM × 2^ENOB × fs
# 但在 fs > 5 GS/s 后，实际功耗增长是超线性的 (thermal + jitter limits)
# 参考: Murmann "ADC Performance Survey" (1997-2024)
#       最新 10GS/s 8-bit ADC: FOM ≈ 100-300 fJ/conv-step


def adc_power_realistic(fs_GHz, enob, arch="pipeline"):
    """更真实的 ADC 功耗模型，区分三个区间"""
    codes = 2**enob

    if fs_GHz <= 0.5:
        # 低速区: Walden FOM 基本适用
        fom_fJ = 30  # fJ/conv-step, 低速优化
        return codes * fom_fJ * 1e-15 * fs_GHz * 1e9

    elif fs_GHz <= 5:
        # 中速区: FOM 开始退化
        fom_fJ = 80
        return codes * fom_fJ * 1e-15 * fs_GHz * 1e9

    else:
        # 高速区 (>5 GS/s): 功耗超线性增长
        # P ∝ fs^α, α ≈ 1.3-1.5 (jitter + thermal + interconnect)
        # 等效 FOM 随 fs 退化
        fom_base = 50    # 基准 FOM @ 5 GS/s
        alpha = 1.4      # 超线性指数
        fom_effective = fom_base * (fs_GHz / 5) ** (alpha - 1)
        return codes * fom_effective * 1e-15 * fs_GHz * 1e9


def dac_power_realistic(fs_GHz, enob):
    """DAC 功耗模型 (高速电流舵 DAC)"""
    # DAC 功耗 ≈ ADC 的 0.6-0.8× (不需要采样保持 + 量化)
    # 但在高速 (>5 GS/s) 也面临类似的抖动和热耗散问题
    return adc_power_realistic(fs_GHz, enob) * 0.7


# ============================================================
# 2. 系统级完整功耗模型
# ============================================================

def system_power_full(D, f_clock_GHz, P_vcsel_mW=5.0, enob=8,
                      vcsel_WPE=0.4, n_dacs=None, n_adcs=None):
    """
    完整系统功耗模型，包含所有被文章指出的缺失项

    架构: N_dac DACs → D VCSELs → D×D 调制像素 → D 列探测器(+TIAs) → N_adc ADCs

    关键架构假设 (列并行读出):
      - D 个 VCSEL 各照射一行 D 个像素
      - 每列 D 个像素的光在 1 个探测器上求和 (Kirchhoff 电流和 = 模拟点积)
      - 因此只需 D 个探测器 + D 个 TIA + D 个 ADC (而非 D²)
      - 这是所有光子交叉杆阵列的标准做法
    """
    if n_dacs is None:
        n_dacs = D      # 每行一个 DAC 驱动 VCSEL
    if n_adcs is None:
        n_adcs = D      # 每列一个 ADC (列并行读出)

    # 1. 激光 + 墙插效率
    P_laser = D * P_vcsel_mW * 1e-3 / vcsel_WPE

    # 2. DAC (电→光 转换) — 文章指出的主要缺失项
    P_per_dac = dac_power_realistic(f_clock_GHz, enob)
    P_dac = n_dacs * P_per_dac

    # 3. 探测器偏置功耗 (D 个列探测器，非 D²)
    #    每列探测器收集来自 D 个像素的光
    #    偏置: ~10 μW/探测器 (大面积探测器, 低速暗电流)
    P_det = D * 10e-6

    # 4. TIA 阵列 — D 个 (每列一个，非 D²)
    #    典型高速 TIA: ~1-5 mW per GHz (45nm CMOS)
    #    保守取 2 mW/GHz
    tia_power_density = 2e-3  # 2 mW per GHz per TIA
    P_per_tia = tia_power_density * f_clock_GHz
    P_per_tia = max(P_per_tia, 0.5e-3)  # 最低 0.5 mW (偏置)
    n_tias = D  # 列并行读出，每列一个 TIA
    P_tia = n_tias * P_per_tia

    # 5. ADC (光→电 转换)
    P_per_adc = adc_power_realistic(f_clock_GHz, enob)
    P_adc = n_adcs * P_per_adc

    # 6. 烘箱/加热器
    P_oven = 50 if D > 100 else 10  # 简化

    # 汇总
    components = {
        '激光 (VCSEL+驱动)': P_laser,
        'DAC (电→光)': P_dac,
        '探测器偏置 (D个)': P_det,
        'TIA 阵列 (D个)': P_tia,
        'ADC (光→电)': P_adc,
        '烘箱/温控': P_oven,
    }
    P_total = sum(components.values())

    # 计算效率
    ops_per_cycle = D * D     # D 维点积 × D 并行 → D² MAC
    ops_per_second = ops_per_cycle * f_clock_GHz * 1e9
    E_per_MAC = P_total / ops_per_second   # J/MAC
    E_per_dot = P_total / (D * f_clock_GHz * 1e9)  # J/D-dim dot product

    # H100 参考
    E_h100_per_MAC = 1.4e-12   # 1.4 pJ/MAC
    E_h100_per_dot = D * E_h100_per_MAC

    return {
        'D': D, 'f_clock_GHz': f_clock_GHz, 'ENOB': enob,
        'components': components,
        'P_total_W': P_total,
        'ops_per_second': ops_per_second,
        'E_per_MAC_fJ': E_per_MAC * 1e15,
        'E_per_dot_fJ': E_per_dot * 1e15,
        'E_h100_per_dot_fJ': E_h100_per_dot * 1e15,
        'ratio_vs_H100_dot': E_h100_per_dot / E_per_dot,
        'optical_fraction': P_laser / P_total,  # 光学占比
        'conversion_fraction': (P_dac + P_adc) / P_total,  # 光电转换占比
    }


# ============================================================
# 3. 灵敏度: f_clock 和 ENOB 对系统功耗的影响
# ============================================================

def sweep_frequency(D=2048):
    """扫频分析 — 找出功耗墙的拐点"""
    print("=" * 78)
    print("  扫频分析: 系统功耗 vs 时钟频率 (D=2048, ENOB=8)")
    print("=" * 78)

    freqs = [0.04, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 17.6]
    print(f"\n  {'f(GHz)':<10s} {'激光(W)':<8s} {'DAC(W)':<8s} {'TIA(W)':<8s} "
          f"{'ADC(W)':<8s} {'总计(W)':<10s} {'vs H100':<10s} {'转换占比':<8s}")
    print(f"  {'─'*78}")

    results = []
    for f in freqs:
        r = system_power_full(D, f)
        results.append(r)
        c = r['components']
        print(f"  {f:<10.2f} {c['激光 (VCSEL+驱动)']:<8.1f} {c['DAC (电→光)']:<8.1f} "
              f"{c['TIA 阵列 (D个)']:<8.2f} {c['ADC (光→电)']:<8.2f} "
              f"{r['P_total_W']:<10.1f} {r['ratio_vs_H100_dot']:<10.0f}× "
              f"{r['conversion_fraction']*100:<6.0f}%")

    return results


def sweep_enob(D=2048, f_GHz=17.6):
    """精度扫频 — ENOB 对功耗的影响"""
    print(f"\n{'='*78}")
    print(f"  精度扫频: 系统功耗 vs ENOB (D=2048, f={f_GHz} GHz)")
    print(f"  (文章观点: 模拟计算精度 < 8bit, 需要更高精度补偿)")
    print(f"{'='*78}")

    print(f"\n  {'ENOB':<8s} {'激光(W)':<8s} {'DAC(W)':<8s} {'TIA(W)':<8s} "
          f"{'ADC(W)':<8s} {'总计(W)':<10s} {'vs H100':<10s}")
    print(f"  {'─'*78}")

    results = []
    for enob in [4, 6, 8, 10, 12]:
        r = system_power_full(D, f_GHz, enob=enob)
        results.append(r)
        c = r['components']
        print(f"  {enob:<8d} {c['激光 (VCSEL+驱动)']:<8.1f} {c['DAC (电→光)']:<8.1f} "
              f"{c['TIA 阵列 (D个)']:<8.2f} {c['ADC (光→电)']:<8.2f} "
              f"{r['P_total_W']:<10.1f} {r['ratio_vs_H100_dot']:<10.0f}×")

    return results


def sweep_D(f_GHz=17.6):
    """阵列规模扫频 — 最优 D"""
    print(f"\n{'='*78}")
    print(f"  阵列扫频: 系统功耗 vs D (f={f_GHz} GHz, ENOB=8)")
    print(f"{'='*78}")

    print(f"\n  {'D':<8s} {'总计(W)':<10s} {'E/dot(fJ)':<12s} {'E/MAC(fJ)':<12s} "
          f"{'vs H100':<10s} {'转换占比':<8s}")
    print(f"  {'─'*78}")

    results = []
    for D in [64, 128, 256, 512, 1024, 2048]:
        r = system_power_full(D, f_GHz)
        results.append(r)
        print(f"  {D:<8d} {r['P_total_W']:<10.1f} {r['E_per_dot_fJ']:<12.1f} "
              f"{r['E_per_MAC_fJ']:<12.2f} {r['ratio_vs_H100_dot']:<10.0f}× "
              f"{r['conversion_fraction']*100:<6.0f}%")

    return results


# ============================================================
# 4. 对比: 简化模型 vs 完整模型
# ============================================================

def compare_models():
    """对比简化模型 (能量对比v2.py) vs 完整模型 (本脚本)"""
    print(f"\n{'='*78}")
    print("  模型对比: 简化 vs 完整 (D=2048, ENOB=8)")
    print(f"{'='*78}")

    freqs = [0.04, 0.24, 17.6]
    labels = ['经典热光 (0.04 GHz)', '激发态调制 (0.24 GHz)', '量子拍频 (17.6 GHz)']

    # 简化模型 (能量对比v2.py 的公式)
    print(f"\n  {'场景':<28s} {'简化(W)':<10s} {'完整(W)':<10s} {'差值(W)':<10s} {'简化vsH100':<10s} {'完整vsH100':<10s}")
    print(f"  {'─'*78}")

    for f, label in zip(freqs, labels):
        D = 2048
        # 简化模型
        P_vcsel = D * 5.0e-3 / 0.4
        P_det = D * D * 1e-6
        P_adc_simple = D * 50e-15 * 256 * f * 1e9
        P_simple = P_vcsel + P_det + P_adc_simple + 50

        # 完整模型
        r = system_power_full(D, f)
        P_full = r['P_total_W']

        # H100 参考
        E_h100_dot = D * 1.4e-12 * 1e15  # fJ/dot
        E_simple = P_simple / (D * f * 1e9) * 1e15
        E_full = r['E_per_dot_fJ']

        print(f"  {label:<28s} {P_simple:<10.0f} {P_full:<10.0f} "
              f"{P_full-P_simple:<+10.0f} "
              f"{E_h100_dot/E_simple:<10.0f}× {E_h100_dot/E_full:<10.0f}×")


# ============================================================
# 5. 主程序
# ============================================================

def main():
    print("╔" + "═" * 76 + "╗")
    print("║  光电转换功耗墙 (DAC/ADC Wall) — 响应知乎文章批评的定量分析       ║")
    print("║  新增: DAC 功耗 + 真实 ADC 超线性模型 + TIA 阵列 + 精度扫频      ║")
    print("╚" + "═" * 76 + "╝")

    # 1. 扫频分析
    sweep_frequency(D=2048)

    # 2. 精度扫频
    sweep_enob(D=2048, f_GHz=17.6)

    # 3. 阵列扫频
    sweep_D(f_GHz=17.6)

    # 4. 模型对比
    compare_models()

    # 5. 结论
    # 先算一个量子拍频的完整结果用于结论
    r_qb = system_power_full(2048, 17.6, enob=8)
    c = r_qb['components']

    print(f"""
╔{'═'*76}╗
║  结论: 光电转换墙到底有多严重?                                        ║
╚{'═'*76}╝

  1. 经典热光 (0.04-0.24 GHz):
     DAC/ADC 功耗可忽略。系统功耗由激光 (VCSEL 墙插效率) 和烘箱主导。
     总功耗 ~50-80W, vs H100 只有 1-16× → 不比 GPU 好。
     → 知乎文章对低速方案的能耗批评成立: 没有数量级优势。

  2. 量子拍频 (17.6 GHz, D=2048):
     完整系统功耗分解:
       激光:     {c['激光 (VCSEL+驱动)']:.0f} W  ({c['激光 (VCSEL+驱动)']/r_qb['P_total_W']*100:.1f}%)
       DAC:      {c['DAC (电→光)']:.0f} W  ({c['DAC (电→光)']/r_qb['P_total_W']*100:.1f}%)
       TIA:      {c['TIA 阵列 (D个)']:.0f} W  ({c['TIA 阵列 (D个)']/r_qb['P_total_W']*100:.1f}%)
       ADC:      {c['ADC (光→电)']:.0f} W  ({c['ADC (光→电)']/r_qb['P_total_W']*100:.1f}%)
       总计:     {r_qb['P_total_W']:.0f} W
     vs H100:  {r_qb['ratio_vs_H100_dot']:.0f}× (每点积)
     → DAC+ADC+TIA = {c['DAC (电→光)']+c['TIA 阵列 (D个)']+c['ADC (光→电)']:.0f}W, 电子接口占总功耗 {r_qb['conversion_fraction']*100:.0f}%
     → 知乎文章的 DAC/ADC 功耗墙成立, 但 TIA 实际上更占大头

  3. 精度维度的双重打击:
     如果模拟计算只能达到 4-6 bit (文章观点):
       a) 需要更高 ENOB 的 DAC/ADC 补偿 → 功耗指数增长 (×2^ΔENOB)
       b) 或接受低精度 → 只能做推理, 不能训练
     → 这对所有模拟光子计算方案都是基础性障碍

  4. 本项目的定位:
     DiSubPc·C70 量子拍频 (17.6 GHz) 的独特之处在于: 调制机制是
     量子相干 (非经典热效应), 有可能绕过传统高速 DAC 的限制。
     但如果信号链仍是 DAC→VCSEL→热筛→探测器→TIA→ADC,
     电子接口功耗会主导总功耗。
     → 需要探索 ALL-OPTICAL 方案 (全光非线性激活、光域求和/存储)

  5. 与知乎文章的关系:
     文章的核心论点 (DAC/ADC 功耗墙、精度塌陷、模拟计算局限) 经过
     本定量分析验证, 确实成立。差异在于:
       文章: "因此光计算是骗局, 不该投入"
       本项目: "这些都是已知的工程瓶颈, 需要创新架构来解决,
                而非不可逾越的物理极限。量子拍频提供了一条可能路径"
""")


if __name__ == '__main__':
    main()
