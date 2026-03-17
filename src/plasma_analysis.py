"""等离子体数据分析工具"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, integrate


def generate_tokamak_profile(n_points=100):
    """模拟托卡马克等离子体参数分布"""
    r = np.linspace(0, 1, n_points)  # 归一化半径
    
    # 温度剖面（近似经验公式）
    T_e = 5.0 * (1 - r**2)**2  # keV, 电子温度
    T_i = 4.0 * (1 - r**2)**2  # keV, 离子温度
    
    # 密度剖面
    n_e = 5e19 * (1 - r**2)**1.5  # m^-3, 电子密度
    
    # 电流密度
    j = 2e6 * (1 - r**2)**1.0  # A/m^2
    
    return {
        'r': r,
        'T_e': T_e,
        'T_i': T_i,
        'n_e': n_e,
        'j': j
    }


def compute_fusion_power(n_i, T_i, volume=100.0):
    """
    计算聚变功率 (D-T reaction)
    P = n_D * n_T * <σv> * E_fusion * V
    """
    # D-T 反应截面拟合（简化）
    T_keV = T_i
    if T_keV < 1:
        sigma_v = 1e-27 * T_keV**2
    elif T_keV < 20:
        sigma_v = 1e-24 * T_keV**2 * np.exp(-20.0 / T_keV)
    else:
        sigma_v = 1e-22 * np.sqrt(T_keV)
    
    E_fusion = 17.6e3 * 1.602e-19  # 17.6 MeV → Joules
    n_D = n_i / 2
    n_T = n_i / 2
    
    P = n_D * n_T * sigma_v * E_fusion * volume
    return P


if __name__ == "__main__":
    print("=" * 50)
    print("⚛️  FusionAI-Lab - Plasma Analysis Demo")
    print("=" * 50)
    
    profile = generate_tokamak_profile()
    
    print("\n📊 Tokamak Plasma Profile:")
    print(f"  Center T_e: {profile['T_e'][0]:.2f} keV")
    print(f"  Center T_i: {profile['T_i'][0]:.2f} keV")
    print(f"  Center n_e: {profile['n_e'][0]:.2e} m^-3")
    
    # 计算聚变功率
    P_fusion = compute_fusion_power(5e19, 15.0, volume=800.0)
    P_fusion_MW = P_fusion / 1e6
    
    print(f"\n⚡ Fusion Power (D-T):")
    print(f"  P = {P_fusion_MW:.2f} MW")
    print(f"  (ITER target: ~500 MW)")
    
    print("\n✅ Analysis complete!")
