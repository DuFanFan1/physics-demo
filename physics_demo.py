# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- 页面设置 ----------
st.set_page_config(page_title="University Physics Optics Lab", layout="wide")

st.title("✨ 大学物理光学干涉虚拟仿真器")
st.caption("基于学生竞赛作品《物演智启》核心算法提取 | 可调节参数实时观测")

# ---------- 缓存计算函数 ----------
@st.cache_data
def compute_intensity(experiment, wavelength_nm, param1, param2, param3=None, param4=None):
    """
    根据实验类型和参数计算干涉图样的强度矩阵和坐标范围。
    """
    wavelength_um = wavelength_nm / 1000.0

    if experiment == "牛顿环 (等厚干涉)":
        R = param1
        d0 = param2 / 1000.0
        size = 300              # 降低分辨率，加速计算和传输
        x = np.linspace(-5, 5, size)
        y = np.linspace(-5, 5, size)
        X, Y = np.meshgrid(x, y)
        r = np.sqrt(X**2 + Y**2)
        d_r = (r**2) / (2 * R) + d0
        intensity = np.sin(2 * np.pi * d_r / wavelength_um) ** 2
        extent = [-5, 5, -5, 5]
        title = f"Newton Rings (λ={wavelength_nm}nm, R={R}mm)"
        xlabel, ylabel = "r (mm)", "r (mm)"

    elif experiment == "劈尖干涉 (等厚干涉)":
        alpha_deg = param1
        d0 = param2 / 1000.0
        alpha_rad = np.radians(alpha_deg)
        size = 300
        x = np.linspace(-4, 4, size)
        y = np.linspace(-4, 4, size)
        X, Y = np.meshgrid(x, y)
        d_x = X * np.tan(alpha_rad) + d0
        intensity = np.sin(2 * np.pi * d_x / wavelength_um) ** 2
        extent = [-4, 4, -4, 4]
        title = f"Interference Wedge (λ={wavelength_nm}nm, θ={alpha_deg}°)"
        xlabel, ylabel = "x (mm)", "y (mm)"

    else:  # 双缝干涉
        d_slit = param1
        a_slit = param2
        L = param3
        size = 400
        x_max = 10
        x = np.linspace(-x_max, x_max, size)
        y = np.linspace(-2, 2, 80)
        X, Y = np.meshgrid(x, y)
        sin_theta = X / L
        delta = np.pi * d_slit * sin_theta / wavelength_um
        beta = np.pi * a_slit * sin_theta / wavelength_um
        interference = np.cos(delta) ** 2
        diffraction = np.ones_like(beta)
        mask = np.abs(beta) > 1e-8
        diffraction[mask] = (np.sin(beta[mask]) / beta[mask]) ** 2
        intensity = interference * diffraction
        extent = [-x_max, x_max, -2, 2]
        title = f"Double-Slit (λ={wavelength_nm}nm, d={d_slit}mm)"
        xlabel, ylabel = "x (mm)", "y (mm)"

    return intensity, extent, title, xlabel, ylabel

# ---------- 侧边栏 ----------
experiment = st.sidebar.selectbox(
    "选择实验",
    ("牛顿环 (等厚干涉)", "劈尖干涉 (等厚干涉)", "双缝干涉 (分波前干涉)")
)

wavelength_nm = st.sidebar.slider("入射光波长 λ (nm)", 380, 780, 550, step=5)

if experiment == "牛顿环 (等厚干涉)":
    R = st.sidebar.slider("曲率半径 R (mm)", 500, 5000, 2000, step=100)
    d0 = st.sidebar.slider("初始空气隙 d₀ (nm)", 0, 500, 100, step=10)
    intensity, extent, title, xlabel, ylabel = compute_intensity(experiment, wavelength_nm, R, d0)
    with st.sidebar:
        st.metric("波长", f"{wavelength_nm} nm")
        st.metric("曲率半径", f"{R} mm")
        st.write("💡 **观察**：波长增大→环纹变疏；R增大→环纹变疏。")

elif experiment == "劈尖干涉 (等厚干涉)":
    alpha_deg = st.sidebar.slider("劈尖夹角 θ (度)", 0.5, 5.0, 1.5, step=0.1)
    d0 = st.sidebar.slider("初始空气隙 d₀ (nm)", 0, 500, 50, step=10)
    intensity, extent, title, xlabel, ylabel = compute_intensity(experiment, wavelength_nm, alpha_deg, d0)
    with st.sidebar:
        st.metric("波长", f"{wavelength_nm} nm")
        st.metric("劈尖夹角", f"{alpha_deg}°")
        st.write("💡 **观察**：波长增大→条纹变疏；角度增大→条纹变密。")

else:  # 双缝干涉
    d_slit = st.sidebar.slider("双缝间距 d (mm)", 0.1, 1.0, 0.5, step=0.05)
    a_slit = st.sidebar.slider("单缝宽度 a (mm)", 0.05, 0.3, 0.1, step=0.01)
    L = st.sidebar.slider("屏幕距离 L (mm)", 500, 2000, 1000, step=100)
    intensity, extent, title, xlabel, ylabel = compute_intensity(experiment, wavelength_nm, d_slit, a_slit, L)
    with st.sidebar:
        st.metric("波长", f"{wavelength_nm} nm")
        st.metric("双缝间距", f"{d_slit} mm")
        st.write("💡 **观察**：波长增大→条纹变宽；缝距d增大→条纹变密。")

# ---------- 显示图像 ----------
col1, col2 = st.columns([3, 1])
with col1:
    # 图像尺寸调小，适合手机预览
    fig, ax = plt.subplots(figsize=(5, 4))   # 原来为 (8,6)，现在缩小
    ax.imshow(intensity, cmap='gray', extent=extent)
    ax.set_title(title, fontsize=12)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    # 保留坐标轴刻度，显示数值
    ax.set_xticks(np.linspace(extent[0], extent[1], 5))
    ax.set_yticks(np.linspace(extent[2], extent[3], 5))
    plt.tight_layout()
    st.pyplot(fig)

st.divider()
st.caption("📚 基于《物演智启》竞赛作品核心物理公式 | 大学物理光学")
