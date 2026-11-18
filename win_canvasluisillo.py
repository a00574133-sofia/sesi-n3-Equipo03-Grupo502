import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def fetch_data():
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=21.12&longitude=-101.68"
            "&hourly=temperature_2m&past_days=1"
            "&timezone=auto"
        )
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        horas = [h.split("T")[1] for h in data["hourly"]["time"][:24]]
        temperaturas = data["hourly"]["temperature_2m"][:24]
        return horas, temperaturas
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los datos:\n{e}")
        return [], []


def create_scatter_line_chart(horas, temps):
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(7, 3.2))

    # Normalizar temperaturas para asignar colores (Frío = Azul, Calor = Rojo)
    norm = mcolors.Normalize(vmin=min(temps), vmax=max(temps))
    cmap = cm.coolwarm

    # Línea gris de conexión y puntos coloreados según temperatura
    ax.plot(horas, temps, color="#888888", linestyle="-", linewidth=1.5, zorder=1)
    scatter = ax.scatter(horas, temps, c=temps, cmap=cmap, norm=norm, s=60, edgecolors="black", zorder=2)

    # Línea de promedio
    promedio = np.mean(temps)
    ax.axhline(promedio, color="#D90429", linestyle="--", linewidth=1.2, label=f"Promedio: {promedio:.1f}°C")

    ax.set_title("Variación Térmica con Indicador de Promedio", fontsize=11, fontweight="bold")
    ax.set_ylabel("°C")
    ax.legend(loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    fig.colorbar(scatter, ax=ax, label="Escala °C", pad=0.02)
    fig.tight_layout()
    return fig


def create_heatmap_bar_chart(horas, temps):
    fig, ax = plt.subplots(figsize=(7, 3.2))
    norm = mcolors.Normalize(vmin=min(temps), vmax=max(temps))
    colors = cm.coolwarm(norm(temps))

    ax.bar(horas, temps, color=colors, edgecolor="#333333", linewidth=0.7)
    ax.set_title("Intensidad de Temperatura por Hora (Mapa de Calor)", fontsize=11, fontweight="bold")
    ax.set_ylabel("°C")
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def mostrar_graficas(frm, horas, temps):
    for widget in frm.winfo_children():
        if not isinstance(widget, ttk.Button):
            widget.destroy()

    fig1 = create_scatter_line_chart(horas, temps)
    canvas1 = FigureCanvasTkAgg(fig1, master=frm)
    canvas1.draw()
    canvas1.get_tk_widget().pack(pady=8, fill="x")

    fig2 = create_heatmap_bar_chart(horas, temps)
    canvas2 = FigureCanvasTkAgg(fig2, master=frm)
    canvas2.draw()
    canvas2.get_tk_widget().pack(pady=8, fill="x")


def open_win_canvas(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Análisis Térmico por Intensidad")
    win.geometry("960x850")

    frm = ttk.Frame(win, padding=12)
    frm.pack(fill="both", expand=True)

    def cargar():
        horas, temps = fetch_data()
        if horas and temps:
            mostrar_graficas(frm, horas, temps)

    ttk.Button(frm, text="Analizar Temperaturas", command=cargar).pack(pady=5)