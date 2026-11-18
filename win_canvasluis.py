import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        # Formateamos las horas para mostrar solo HH:MM
        horas = [h.split("T")[1] for h in data["hourly"]["time"][:24]]
        temperaturas = data["hourly"]["temperature_2m"][:24]
        return horas, temperaturas
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los datos:\n{e}")
        return [], []


def create_line_chart(horas, temps):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(7, 3.2), facecolor="#121212")
    ax.set_facecolor("#1E1E1E")

    # Línea de neón y área sombreada
    ax.plot(horas, temps, color="#00F5D4", linewidth=2.5, marker="o", markersize=5, markerfacecolor="#FFFFFF")
    ax.fill_between(horas, temps, min(temps) - 2, color="#00F5D4", alpha=0.15)

    ax.set_title("Temperatura en León - Modo Nocturno", color="#FFFFFF", fontsize=12, fontweight="bold", pad=10)
    ax.set_ylabel("Temperatura (°C)", color="#BBBBBB")
    ax.grid(True, linestyle="--", alpha=0.2, color="#FFFFFF")
    ax.tick_params(axis="x", rotation=45, colors="#AAAAAA", labelsize=8)
    ax.tick_params(axis="y", colors="#AAAAAA")

    # Ocultar bordes superior y derecho
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def create_bar_chart(horas, temps):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(7, 3.2), facecolor="#121212")
    ax.set_facecolor("#1E1E1E")

    bars = ax.bar(horas, temps, color="#FF007F", edgecolor="#FF66B2", linewidth=0.8, alpha=0.85, width=0.6)
    
    # Etiquetas de valor encima de cada barra
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f"{yval:.0f}°", ha="center", va="bottom", color="#FFFFFF", fontsize=7)

    ax.set_title("Distribución Horaria (Barras Neón)", color="#FFFFFF", fontsize=12, fontweight="bold", pad=10)
    ax.set_ylabel("°C", color="#BBBBBB")
    ax.tick_params(axis="x", rotation=45, colors="#AAAAAA", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    return fig


def mostrar_graficas(frm, horas, temps):
    for widget in frm.winfo_children():
        if not isinstance(widget, ttk.Button):
            widget.destroy()

    fig1 = create_line_chart(horas, temps)
    canvas1 = FigureCanvasTkAgg(fig1, master=frm)
    canvas1.draw()
    canvas1.get_tk_widget().pack(pady=8, fill="x")

    fig2 = create_bar_chart(horas, temps)
    canvas2 = FigureCanvasTkAgg(fig2, master=frm)
    canvas2.draw()
    canvas2.get_tk_widget().pack(pady=8, fill="x")


def open_win_canvas(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Dashboard Climático - Dark Mode")
    win.geometry("960x850")
    win.configure(bg="#121212")

    frm = tk.Frame(win, bg="#121212", padx=15, pady=15)
    frm.pack(fill="both", expand=True)

    def cargar():
        horas, temps = fetch_data()
        if horas and temps:
            mostrar_graficas(frm, horas, temps)

    ttk.Button(frm, text="Cargar Datos Nocturnos", command=cargar).pack(pady=5)