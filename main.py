import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sympy as sp
import numpy as np

# Constante de Euler con toda su precisión
e_redondeado = np.e

# Función para limpiar los campos y resultados
def limpiar_campos():
    entry_funcion.delete(0, tk.END)
    entry_x0.delete(0, tk.END)
    entry_error.delete(0, tk.END)
    derivada_label.config(text="")
    resultado_label.config(text="")
    for widget in tabla_frame.winfo_children():
        widget.destroy()

# Método de Newton-Raphson con tabla visual redondeada a 6 decimales
def NewtonRaphson(x1, es):
    x = x1  # Aproximación inicial
    ea = 2 * es  # Error absoluto inicial (mayor que el error solicitado)
    i = 0  # Número de iteraciones
    Newton_table = []

    # Agrega la primera fila con el valor inicial
    Newton_table.append([i, "{:.4f}".format(x), "{:.4f}".format(f(x)), "{:.4f}".format(f1(x)), "--"])

    # Ciclo de iteraciones de Newton-Raphson
    while ea > es:
        # Redondeamos x y la función antes de los cálculos
        x = round(x, 4)
        f_x = round(f(x), 4)
        f1_x = round(f1(x), 4)

        # Aplicación de la fórmula de Newton-Raphson
        x_new = round(x - f_x / f1_x, 4)

        # Calculamos el error relativo porcentual
        if x_new != 0:
            ea = round(abs((x_new - x) / x_new) * 100, 4)  # Redondeamos el error
        else:
            ea = 0

        # Calculamos f(x_new) y f'(x_new) para la siguiente iteración
        f_new = round(f(x_new), 4)
        f1_new = round(f1(x_new), 4)

        i += 1  # Incrementamos el contador de iteraciones

        # Agregamos la nueva fila con x_new, f(x_new), f'(x_new) y el error
        Newton_table.append([i, "{:.4f}".format(x_new), "{:.4f}".format(f_new), "{:.4f}".format(f1_new), "{:.4f}%".format(ea)])

        # Actualizamos x para la siguiente iteración
        x = x_new

    derivada_label.config(text=f"Derivada de la función: {f1_symb}")

    # Limpiar cualquier tabla anterior
    for widget in tabla_frame.winfo_children():
        widget.destroy()

    # Encabezados de la tabla
    encabezado_bg = "#00796b"
    encabezado_fg = "white"
    fila_bg = "#e0f2f1"
    fila_impar_bg = "#b2dfdb"

    # Encabezados de la tabla
    encabezados = ["Iteración", "x", "f(x)", "f'(x)", "Error (%)"]
    for j, encabezado in enumerate(encabezados):
        tabla_frame.grid_columnconfigure(j, weight=1)  # Hacer que las columnas se expandan
        label = tk.Label(tabla_frame, text=encabezado, bg=encabezado_bg, fg=encabezado_fg,
                         font=("Helvetica", 10, "bold"), padx=15, pady=5, borderwidth=1, relief="solid")
        label.grid(row=0, column=j, sticky="nsew", padx=2, pady=2)

    # Filas de la tabla
    for i, fila in enumerate(Newton_table):
        bg_color = fila_impar_bg if i % 2 == 0 else fila_bg
        for j, valor in enumerate(fila):
            tabla_frame.grid_columnconfigure(j, weight=1)  # Hacer que las columnas se expandan
            label = tk.Label(tabla_frame, text=valor, bg=bg_color, fg="black", font=("Helvetica", 10), padx=15, pady=5,
                             borderwidth=1, relief="solid")
            label.grid(row=i + 1, column=j, sticky="nsew", padx=2, pady=2)

    return x

# Función para obtener funciones y sus derivadas usando numpy
def obtener_funciones(funcion_str):
    x = sp.Symbol('x')

    # Aquí reemplazamos e por su valor original (sin redondear)
    funcion_str = funcion_str.replace("e", str(e_redondeado))

    funcion_simbolica = sp.sympify(funcion_str)  # Convertimos la cadena de texto a una expresión simbólica
    derivada_simbolica = sp.diff(funcion_simbolica, x)  # Derivada de la función simbólica
    f_numeric = sp.lambdify(x, funcion_simbolica, 'numpy')
    f1_numeric = sp.lambdify(x, derivada_simbolica, 'numpy')
    return f_numeric, f1_numeric, funcion_simbolica, derivada_simbolica

# Función que se ejecuta al hacer clic en el botón de calcular
def calcular():
    try:
        funcion_str = entry_funcion.get()  # Obtener la función ingresada por el usuario
        x1 = float(entry_x0.get())  # Obtener el valor inicial ingresado
        es = float(entry_error.get())  # Obtener el error permitido

        global f, f1, f1_symb
        f, f1, _, f1_symb = obtener_funciones(funcion_str)

        xr = NewtonRaphson(x1, es)

        resultado_label.config(text=f"Valor aproximado de la raíz: {xr:.6f}")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Calculadora del Método de Newton-Raphson Estándar")
root.geometry("1000x800")
root.configure(bg="#00796b")  # Fondo verde

style = ttk.Style()
style.theme_use('clam')

# Estilos de la interfaz con colores blanco y verde
style.configure("TLabel", background="#00796b", foreground="white", font=("Helvetica", 12, "bold"))  # Texto blanco
style.configure("TButton", background="#d32f2f", foreground="white", font=("Helvetica", 12, "bold"))
style.map("TButton", background=[('active', '#b71c1c')], foreground=[('active', 'white')])

titulo_label = ttk.Label(root, text="Calculadora del Método de Newton-Raphson Estándar", font=("Helvetica", 16, "bold"),
                         foreground="#ffffff")
titulo_label.pack(pady=20)

frame_campos = ttk.Frame(root, padding=20)
frame_campos.pack(pady=10, fill=tk.X)

ttk.Label(frame_campos, text="Función f(x):").grid(row=0, column=0, padx=10, pady=5, sticky="E")
entry_funcion = ttk.Entry(frame_campos, width=30)
entry_funcion.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame_campos, text="Valor inicial x₀:").grid(row=0, column=2, padx=10, pady=5, sticky="E")
entry_x0 = ttk.Entry(frame_campos, width=15)
entry_x0.grid(row=0, column=3, padx=10, pady=5)

ttk.Label(frame_campos, text="Error porcentual deseado (%):").grid(row=0, column=4, padx=10, pady=5, sticky="E")
entry_error = ttk.Entry(frame_campos, width=15)
entry_error.grid(row=0, column=5, padx=10, pady=5)

boton_calcular = ttk.Button(root, text="Calcular", command=calcular)
boton_calcular.pack(pady=20)

boton_limpiar = ttk.Button(root, text="Limpiar", command=limpiar_campos)
boton_limpiar.pack(pady=10)

derivada_label = ttk.Label(root, text="")
derivada_label.pack(pady=5)

# Crear frame para la tabla de resultados
tabla_frame = ttk.Frame(root, padding=10)
tabla_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

resultado_label = ttk.Label(root, text="")
resultado_label.pack(pady=5)

root.mainloop()
