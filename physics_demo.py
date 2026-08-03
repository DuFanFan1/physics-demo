# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 设置 matplotlib 使用支持中文的字体
# Windows 系统通常有 SimHei（黑体），macOS 有 PingFang SC
try:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'PingFang SC', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
except:
    pass

# ---------- 页面标题 ----------
st.set_page_config(page_title="大学物理光学演示器", layout="wide")
st.title("✨ 大学物理光学干涉虚拟仿真器")
st.caption("基于学生竞赛作品《物演智启》核心算法提取 | 可调节参数实时观测")

# ---------- 侧边栏：实验选择 ----------
experiment = st.sidebar.selectbox(
    "请选择实验内容",
    ("🔵 牛顿环 (等厚干涉)", "🟢 劈尖干涉 (等厚干涉)", "🔴 双缝干涉 (分波前干涉)")
)

# ---------- 侧边栏：公共参数（波长） ----------
# 提取自报告公式 (12) (19) (37)
wavelength_nm = st.sidebar.slider("入射光波长 λ (nm)", 380, 780, 550, step=5)
# 将纳米转换为微米（便于计算，1 um = 1000 nm）
wavelength_um = wavelength_nm / 1000.0 

# ---------- 图像显示区域 ----------
col1, col2 = st.columns([3, 1]) # 左侧放图，右侧放参数说明

with col1:
    # 创建一个画布
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # ---------- 1. 牛顿环仿真 (报告 2.1.1) ----------
    if experiment == "🔵 牛顿环 (等厚干涉)":
        # 提取自报告公式 (11) d(r) = r^2/(2R) + d0, 公式 (12) I = sin^2(2πd/λ)
        R = st.sidebar.slider("曲率半径 R (mm)", 500, 5000, 2000, step=100)
        d0 = st.sidebar.slider("初始空气隙 d₀ (nm)", 0, 500, 100, step=10) / 1000.0 # 转为微米
        
        # 生成网格坐标 (像素矩阵)
        size = 400
        x = np.linspace(-5, 5, size) # 坐标范围 -5mm 到 5mm
        y = np.linspace(-5, 5, size)
        X, Y = np.meshgrid(x, y)
        r = np.sqrt(X**2 + Y**2)
        
        # 核心物理公式：膜厚 d(r) = r^2/(2R) + d0
        d_r = (r**2) / (2 * R) + d0
        # 反射光强：I = sin^2( 2π * d(r) / λ )  (半波损失导致中心暗斑)
        intensity = np.sin(2 * np.pi * d_r / wavelength_um) ** 2
        
        ax.imshow(intensity, cmap='gray', extent=[-5, 5, -5, 5])
        ax.set_title(f'牛顿环仿真 (λ={wavelength_nm}nm, R={R}mm)', fontsize=14)
        ax.set_xlabel('径向距离 r (mm)')
        ax.set_ylabel('径向距离 r (mm)')
        
        with col2:
            st.metric("当前波长", f"{wavelength_nm} nm")
            st.metric("曲率半径", f"{R} mm")
            st.write("💡 **观察要点**：波长增大→环纹变疏；R增大→环纹变疏。")

    # ---------- 2. 劈尖干涉仿真 (报告 2.1.2) ----------
    elif experiment == "🟢 劈尖干涉 (等厚干涉)":
        # 提取自报告公式 (16) d(x) = x*tan(α) + d0, 公式 (19) I = sin^2(2πd/λ)
        alpha_deg = st.sidebar.slider("劈尖夹角 α (度)", 0.5, 5.0, 1.5, step=0.1)
        d0 = st.sidebar.slider("初始空气隙 d₀ (nm)", 0, 500, 50, step=10) / 1000.0 # 转为微米
        
        alpha_rad = np.radians(alpha_deg) # 角度转弧度
        
        size = 400
        x = np.linspace(-4, 4, size) # 横向范围 -4mm 到 4mm
        y = np.linspace(-4, 4, size)
        X, Y = np.meshgrid(x, y)
        
        # 核心物理公式：沿X方向膜厚线性增加，Y方向不变
        d_x = X * np.tan(alpha_rad) + d0
        # 干涉光强
        intensity = np.sin(2 * np.pi * d_x / wavelength_um) ** 2
        
        ax.imshow(intensity, cmap='gray', extent=[-4, 4, -4, 4])
        ax.set_title(f'劈尖干涉仿真 (λ={wavelength_nm}nm, α={alpha_deg}°)', fontsize=14)
        ax.set_xlabel('水平位置 x (mm)')
        ax.set_ylabel('垂直方向 y (mm)')
        
        with col2:
            st.metric("当前波长", f"{wavelength_nm} nm")
            st.metric("劈尖夹角", f"{alpha_deg}°")
            st.write("💡 **观察要点**：波长增大→条纹变疏；角度增大→条纹变密。")

    # ---------- 3. 双缝干涉仿真 (报告 2.1.3) ----------
    else:
        # 提取自报告公式 (37) I = cos^2(π*d*sinθ/λ) * sinc^2(π*a*sinθ/λ)
        d_slit = st.sidebar.slider("双缝间距 d (mm)", 0.1, 1.0, 0.5, step=0.05)
        a_slit = st.sidebar.slider("单缝宽度 a (mm)", 0.05, 0.3, 0.1, step=0.01)
        L = st.sidebar.slider("屏幕距离 L (mm)", 500, 2000, 1000, step=100)
        
        size = 600
        # 屏幕上的观察范围 (x方向)
        x_max = 10 # mm
        x = np.linspace(-x_max, x_max, size)
        y = np.linspace(-2, 2, 100) # Y方向只取一小段，呈现条纹的纵深感
        
        X, Y = np.meshgrid(x, y)
        
        # 小角度近似 sinθ ≈ x/L (报告公式 31)
        sin_theta = X / L
        
        # 相位差计算
        delta = np.pi * d_slit * sin_theta / wavelength_um
        beta = np.pi * a_slit * sin_theta / wavelength_um
        
        # 双缝干涉因子 + 单缝衍射包络 (Sinc函数处理分母为0的情况)
        # 双缝项：cos^2(δ)
        interference = np.cos(delta) ** 2
        # 衍射项：sinc^2(β) ，防止除以0
        diffraction = np.ones_like(beta)
        mask = np.abs(beta) > 1e-8
        diffraction[mask] = (np.sin(beta[mask]) / beta[mask]) ** 2
        
        intensity = interference * diffraction
        
        ax.imshow(intensity, cmap='gray', extent=[-x_max, x_max, -2, 2], aspect='auto')
        ax.set_title(f'双缝干涉仿真 (λ={wavelength_nm}nm, d={d_slit}mm, a={a_slit}mm)', fontsize=14)
        ax.set_xlabel('屏幕位置 x (mm)')
        ax.set_ylabel('垂直方向 (mm)')
        
        with col2:
            st.metric("当前波长", f"{wavelength_nm} nm")
            st.metric("双缝间距", f"{d_slit} mm")
            st.write("💡 **观察要点**：波长增大→条纹变宽；缝距d增大→条纹变密；缝宽a影响亮度包络（缺级）。")

    # 美化图片显示
    ax.set_xticks([]) 
    ax.set_yticks([])
    plt.tight_layout()
    st.pyplot(fig)

# ---------- 底部信息 ----------
st.divider()
st.caption("📚 本程序基于《物演智启》竞赛作品核心物理公式开发 | 公式来源：大学物理光学（等厚/分波前干涉）")