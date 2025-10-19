import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.font_manager import FontProperties

# 设置中文字体，以防显示乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 1. 创建信号 ---
# 我们将创建一个由3个不同频率、不同振幅的正弦波叠加而成的复杂信号
sampling_rate = 100
t = np.linspace(0, 2, 2 * sampling_rate, endpoint=False)

# 组件1: 频率=2Hz, 振幅=1.0
freq1, amp1 = 2, 1.0
wave1 = amp1 * np.sin(2 * np.pi * freq1 * t)

# 组件2: 频率=5Hz, 振幅=0.5
freq2, amp2 = 5, 0.5
wave2 = amp2 * np.sin(2 * np.pi * freq2 * t)

# 组件3: 频率=8Hz, 振幅=0.3
freq3, amp3 = 8, 0.3
wave3 = amp3 * np.sin(2 * np.pi * freq3 * t)

# 合成信号
combined_wave = wave1 + wave2 + wave3

# 频率和组件列表
frequencies = [freq1, freq2, freq3]
amplitudes = [amp1, amp2, amp3]
components = [wave1, wave2, wave3]

# --- 2. 设置3D绘图环境 ---
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# --- 3. 绘制静态图形元素 ---

# a. 绘制合成后的复杂信号 (放在最前面)
# 我们将频率轴的最大值作为它的位置
front_position = max(frequencies) + 2
ax.plot(t, np.full_like(t, front_position), combined_wave, lw=2.5, color='r', label=' f(t)')

# b. 绘制各个简单的正弦波组件
# 它们被放置在各自频率对应的位置上
for freq, component in zip(frequencies, components):
    ax.plot(t, np.full_like(t, freq), component, lw=1, color='b', alpha=0.7)

# c. 绘制从组件到合成信号的投影线 (可选，但能增强理解)
for i in range(0, len(t), 10): # 每隔10个点画一条线
    for freq in frequencies:
        ax.plot([t[i], t[i]], [freq, front_position], [0, 0], color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# d. 绘制频谱图 (真正的“侧视图”)
# 我们在时间轴的起点(t=0)绘制一个平面来展示频谱
# 这是傅里叶变换的结果
ax.stem(np.full_like(frequencies, t[0]), frequencies, amplitudes,
        linefmt='-g', markerfmt='og', basefmt=' ', label=' F(jω)')


# --- 4. 美化图形 ---
ax.set_xlabel('Time (t)', fontsize=12, labelpad=10)
ax.set_ylabel('Frequency (ω)', fontsize=12, labelpad=10)
ax.set_zlabel('Amplitude', fontsize=12, labelpad=10)
ax.set_title('Fourier Transform', fontsize=16, pad=20)
ax.set_ylim(0, front_position + 1)

ax.view_init(elev=25, azim=-140) # 设置一个不错的初始视角
ax.grid(True)

# --- 5. 创建动画 ---
def update(frame):
    # 每一帧都改变摄像机的方位角 (azim)
    ax.view_init(elev=25, azim=-140 + frame)
    return fig,

# 创建动画，帧数设置为360，代表旋转360度
ani = FuncAnimation(fig, update, frames=360, interval=30, blit=True)

# 保存为GIF
print("正在生成 GIF 动画，这可能需要一两分钟...")
ani.save('fourier_synthesis_3d.gif', writer='pillow', fps=30)
print("动画 'fourier_synthesis_3d.gif' 已保存！")

plt.show()

