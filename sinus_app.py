import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

st.set_page_config(page_title="Symulator Sygnału Sinusoidalnego", layout="centered")

st.title("🎵 Symulator Sygnału Sinusoidalnego")

# Parametry wejściowe wspólne dla wszystkich zakładek
freq = st.sidebar.slider("Częstotliwość (Hz)", 0.1, 10.0, 1.0, 0.1)
amp = st.sidebar.slider("Amplituda", 0.1, 5.0, 1.0, 0.1)
phase = st.sidebar.slider("Faza (rad)", 0.0, 2 * np.pi, 0.0, 0.1)
y_min = st.sidebar.slider("Y min", -10.0, 0.0, -2.0, 0.1)
y_max = st.sidebar.slider("Y max", 0.0, 10.0, 2.0, 0.1)

# Zakładki
tab1, tab2, tab3 = st.tabs(["📈 Wykres sinusa", "⚡ Analiza FFT", "🎞️ Animacja"])

# Zakładka 1 – Wykres sinusa
with tab1:
    st.subheader("📈 Wykres sygnału sinusoidalnego")
    t = np.linspace(0, 2, 1000)
    y = amp * np.sin(2 * np.pi * freq * t + phase)

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(t, y, label="sinus")
    ax1.set_title("Sygnał Sinusoidalny")
    ax1.set_xlabel("Czas [s]")
    ax1.set_ylabel("Amplituda")
    ax1.set_ylim(y_min, y_max)
    ax1.grid(True)
    st.pyplot(fig1)

# Zakładka 2 – Analiza FFT
with tab2:
    st.subheader("⚡ Analiza częstotliwościowa (FFT)")

    N = 1000
    t = np.linspace(0, 2, N)
    y = amp * np.sin(2 * np.pi * freq * t + phase)
    fft_vals = np.fft.fft(y)
    fft_freqs = np.fft.fftfreq(N, d=(t[1] - t[0]))

    # Tylko dodatnie częstotliwości
    pos_mask = fft_freqs >= 0
    fft_vals = np.abs(fft_vals[pos_mask])
    fft_freqs = fft_freqs[pos_mask]

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.stem(fft_freqs, fft_vals, use_line_collection=True)
    ax2.set_xlim(0, 20)
    ax2.set_title("FFT – widmo amplitudowe")
    ax2.set_xlabel("Częstotliwość [Hz]")
    ax2.set_ylabel("Amplituda")
    ax2.grid(True)
    st.pyplot(fig2)

# Zakładka 3 – Animacja
with tab3:
    st.subheader("🎞️ Animacja sygnału w czasie")

    st.write("Animowany przebieg fali sinusoidalnej:")

    # Ustawienia
    duration = st.slider("Czas trwania animacji (s)", 2, 10, 5)
    frame_rate = 30
    total_frames = duration * frame_rate
    t = np.linspace(0, 2, 1000)

    chart = st.line_chart(np.zeros_like(t))

    for frame in range(total_frames):
        current_phase = phase + 2 * np.pi * freq * (frame / frame_rate)
        y = amp * np.sin(2 * np.pi * freq * t + current_phase)
        chart.line_chart(y)
        time.sleep(1.0 / frame_rate)
