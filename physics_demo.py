# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- 页面标题 ----------
st.set_page_config(page_title="University Physics Optics Lab", layout="wide")

# ---------- 标题（用 Streamlit 原生组件显示中文，不依赖 matplotlib 字体）----------
st.title("✨ 大学物理光学干涉虚拟仿真器")
st.caption("基于学生竞赛作品《物演智启》核心算法提取 | 可调节参数实时观测")

# ---------- 侧边栏：实验选择 ----------
experiment = st.sidebar.selectbox(
    "请选择实验内容",
    ("牛顿环 (等厚干涉)", "劈尖干涉 (等厚干涉)", "双缝干涉 (分波前干涉)")
)

# ---------- 侧边栏：公共参数 ----------
wavelength_nm = st.sidebar.slider("入射光波长 λ (nm)", 380, 780, 550, step=5)
wavelength_um = wavelength_nm / 1000.0

col1, col2 = st.columns([3, 1])

with col1:
    fig, ax = plt.subplots(figsize=(8, 6))

    # ---------- 1. 牛顿环 ----------
    if experiment == "牛顿环 (等厚干涉)":
        R = st.sidebar.slider("曲率半径 R (mm)", 500, 5000, 2000, step=100)
        d0 = st.sidebar.slider("初始空气隙 d₀ (nm)", 0, 500, 100, step=10) / 1000.0

        size = 400
        x = np.linspace(-5, 5, size)
        y = np.linspace(-5, 5, size)
        X, Y = np.meshgrid(x, y)
        r = np.sqrt(X**2 + Y**2)

        d_r = (r**2) / (2 * R) + d0
        intensity = np.sin(2 * np.pi * d_r / wavelength_um) ** 2

        ax.imshow(intensity, cmap='gray', extent=[-5, 5, -5, 5])
        # ⚠️ 关键修改：标题和坐标轴全部用英文/拼音
        ax.set_title(f'Newton Rings (λ={wavelength_nm}nm, R={R}mm)', fontsize=14)
        ax.set_xlabel('Radial distance r (mm)')
        ax.set_ylabel('Radial distance r (mm)')

        with col2:
            st.metric("波长", f"{wavelength_nm} nm")
            st.metric("曲率半径", f"{R} mm")
            st.write("💡 **观察要点**：波长增大→环纹变疏；R增大→环纹变疏。")

    # ---------- 2. 劈尖干涉 ----------
    elif experiment == "劈尖干涉 (等厚干涉)":
        alpha_deg = st.sidebar.slider("劈尖夹角 α (度)", 0.5, 5.0, 1.5, step=0.1)
        d0 = st.sidebar.slider("初始空气隙 d₀ (nm)", 0, 500, 50, step=10) / 1000.0
        alpha_rad = np.radians(alpha_deg)

        size = 400
        x = np.linspace(-4, 4, size)
        y = np.linspace(-4, 4, size)
        X, Y = np.meshgrid(x, y)

        d_x = X * np.tan(alpha_rad) + d0
        intensity = np.sin(2 * np.pi * d_x / wavelength_um) ** 2

        ax.imshow(intensity, cmap='gray', extent=[-4, 4, -4, 4])
        ax.set_title(f'Interference Wedge (λ={wavelength_nm}nm, α={alpha_deg}°)', fontsize=14)
        ax.set_xlabel('Position x (mm)')
        ax.set_ylabel('Position y (mm)')

        with col2:
            st.metric("波长", f"{wavelength_nm} nm")
            st.metric("劈尖夹角", f"{alpha_deg}°")
            st.write("💡 **观察要点**：波长增大→条纹变疏；角度增大→条纹变密。")

    # ---------- 3. 双缝干涉 ----------
    else:
        d_slit = st.sidebar.slider("双缝间距 d (mm)", 0.1, 1.0, 0.5, step=0.05)
        a_slit = st.sidebar.slider("单缝宽度 a (mm)", 0.05, 0.3, 0.1, step=0.01)
        L = st.sidebar.slider("屏幕距离 L (mm)", 500, 2000, 1000, step=100)

        size = 600
        x_max = 10
        x = np.linspace(-x_max, x_max, size)
        y = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x, y)

        sin_theta = X / L
        delta = np.pi * d_slit * sin_theta / wavelength_um
        beta = np.pi * a_slit * sin_theta / wavelength_um

        interference = np.cos(delta) ** 2
        diffraction = np.ones_like(beta)
        mask = np.abs(beta) > 1e-8
        diffraction[mask] = (np.sin(beta[mask]) / beta[mask]) ** 2
        intensity = interference * diffraction

        ax.imshow(intensity, cmap='gray', extent=[-x_max, x_max, -2, 2], aspect='auto')
        ax.set_title(f'Double-Slit Interference (λ={wavelength_nm}nm, d={d_slit}mm)', fontsize=14)
        ax.set_xlabel('Screen position x (mm)')
        ax.set_ylabel('Vertical position (mm)')

        with col2:
            st.metric("波长", f"{wavelength_nm} nm")
            st.metric("双缝间距", f"{d_slit} mm")
            st.write("💡 **观察要点**：波长增大→条纹变宽；缝距d增大→条纹变密。")

    # 隐藏坐标轴刻度，画面更干净
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    st.pyplot(fig)

st.divider()
st.caption("📚 基于《物演智启》竞赛作品核心物理公式开发 | 公式来源：大学物理光学（等厚/分波前干涉）")
