import tkinter as tk
from tkinter import Canvas, ttk
import serial
import threading
import time

# Configurar el puerto serial (ajustar el puerto según tu sistema)
arduino_port = '/dev/ttyACM0'  # Reemplazar '/dev/ttyACM0' con tu puerto serial correcto
ser = serial.Serial(arduino_port, 9600)

# Coordenadas de los nodos del árbol
node_positions = {
    0: (200, 50),   # Nodo 1 (Raíz)
    1: (100, 150),  # Nodo 2 (Hijo izquierdo)
    2: (300, 150),  # Nodo 3 (Hijo derecho)
    3: (50, 250),   # Nodo 4 (Hijo izquierdo del nodo 2)
    4: (150, 250),  # Nodo 5 (Hijo derecho del nodo 2)
}

# Crear la ventana principal
root = tk.Tk()
root.title("Proyecto Integrado")
root.geometry("700x450")  # Ajustar el ancho y alto de la ventana

# Crear un Frame para contener el Canvas y la etiqueta de secuencia
frame = tk.Frame(root, bg="#f0f0f0")  # Establecer el color de fondo en gris claro
frame.pack(side="left", fill="both", expand=True)  # Rellenar y expandir el Frame

# Canvas para dibujar el árbol
canvas = Canvas(frame, width=400, height=400, bg="#f0f0f0")  # Establecer el color de fondo en gris claro
canvas.pack(fill="both", expand=True)  # Rellenar y expandir el Canvas en el Frame

# Lista de círculos (nodos del árbol)
circles = []

# Colores para cada círculo cuando están encendidos
circle_colors = {
    0: "yellow",
    1: "lime green",
    2: "red",
    3: "red",
    4: "lime green"
}

# Colores para cada círculo cuando están apagados
circle_off_color = "gray"

# Dibujar los círculos (nodos del árbol)
for node_id, (x, y) in node_positions.items():
    circle = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline="black", fill=circle_off_color)
    circles.append(circle)

# Etiqueta para mostrar la secuencia seleccionada
sequence_label = tk.Label(frame, text="Secuencia: ", font=("Arial", 12), bg="#f0f0f0")
sequence_label.pack(side="bottom", pady=(0, 10))

# Crear una barra de progreso para visualizar el valor del potenciómetro
progress_frame = tk.Frame(root, bg="#f0f0f0")
progress_frame.pack(side="right", padx=40, pady=50)
progress_bar = ttk.Progressbar(progress_frame, orient="vertical", length=300, mode="determinate", maximum=1023)  # Ajustar la longitud de la barra
progress_bar.pack(fill="y")
pot_label = tk.Label(progress_frame, text="Valor del potenciómetro: 0" + " " * 80, bg="#f0f0f0", anchor="w")  # Espacios adicionales para longitud extendida
pot_label.pack(pady=(20, 0))

# Función para recibir señales desde Arduino y actualizar la interfaz gráfica
def receive_signals():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            print("Señal recibida desde Arduino:", data)
            if data == "Botón 1 presionado":
                animate_preorden()
                sequence_label.config(text="Secuencia: PreOrden")
            elif data == "Botón 2 presionado":
                animate_inorden()
                sequence_label.config(text="Secuencia: InOrden")
            elif data == "Botón 3 presionado":
                animate_posorden()
                sequence_label.config(text="Secuencia: PosOrden")
            try:
                pot_value = int(data)
                progress_bar["value"] = pot_value
                pot_label.config(text=f"Valor del potenciómetro: {pot_value} Ω" + " " * 80)  # Ajustar la longitud extendida
            except ValueError:
                pass

# Función para animar el recorrido PreOrden
def animate_preorden():
    for i in [1, 3, 0, 4, 2]:
        change_circle_color(i, circle_colors[i])
        time.sleep(0.5)
        change_circle_color(i, circle_off_color)

# Función para animar el recorrido InOrden
def animate_inorden():
    for i in [0, 1, 3, 4, 2]:
        change_circle_color(i, circle_colors[i])
        time.sleep(0.5)
        change_circle_color(i, circle_off_color)

# Función para animar el recorrido PosOrden
def animate_posorden():
    for i in [3, 4, 1, 2, 0]:
        change_circle_color(i, circle_colors[i])
        time.sleep(0.5)
        change_circle_color(i, circle_off_color)

# Función para cambiar el color de un círculo (nodo)
def change_circle_color(circle_index, color):
    canvas.itemconfig(circles[circle_index], fill=color)

# Crear un hilo para recibir señales desde Arduino en segundo plano
signal_thread = threading.Thread(target=receive_signals)
signal_thread.daemon = True  # El hilo terminará cuando se cierre la aplicación
signal_thread.start()

root.mainloop()
