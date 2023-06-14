import tkinter as tk
import customtkinter
import numpy as np
import ast
import math
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import Symbol, diff
from scipy.optimize import fsolve
from scipy.interpolate import UnivariateSpline
from sympy import Symbol ,diff,lambdify
from scipy.optimize import fsolve
import numpy as np
from time import perf_counter
import time
from tkinter import messagebox
import ast
from sympy import symbols, SympifyError, sympify
from sympy import Symbol, sin, diff, lambdify

# Crearea ferestrei principale
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

window = customtkinter.CTk()
window.title("Metoda Bisectiei si Metoda Coardei")
# Set the window to be non-resizable
window.resizable(False, False)

# functie pentru interfata grafica la erori
def show_error(title, message):
    error_window = customtkinter.CTk()
    error_window.title(title)
    error_window.resizable(False, False)

    label = customtkinter.CTkLabel(error_window, text=message, font=("Arial", 12))
    label.pack(padx=10, pady=10)

    ok_button = customtkinter.CTkButton(error_window, text="OK", command=error_window.destroy)
    ok_button.pack(padx=10, pady=10)

    error_window.mainloop()

# functie care calculeaza metoda bisectiei
def my_bisection(f, a, b, tol):
    en = textbox_en.get()
    if np.sign(f(a)) == np.sign(f(b)):
        show_error("Eroare", "Scalarii a și b nu delimitează o rădăcină!")
        return
    m = (a + b) / 2

    if np.abs(f(m)) < tol:
        return m

    elif np.sign(f(a)) == np.sign(f(m)):
        return my_bisection(f, m, b, tol)

    elif np.sign(f(b)) == np.sign(f(m)):
        return my_bisection(f, a, m, tol)

# functie care calculeaza metoda coardei 
def coarda_er(f,a,b,er):
    x=Symbol('x')
    f2=diff(f,x,2)
    f=lambdify(x, f)
    f2=lambdify(x, f2)
    r_ex=fsolve(f,(a+b)/2)
    if f(a)*f2(a)<0:
        x=a
        while abs(r_ex-x)>er:
            x=x-f(x)/(f(x)-f(b))*(x-b)
    else:
             x=x-f(x)/(f(x)-f(a))*(x-a) 
    return x
    
# functie pentru validatoare
def errors():
    a = textbox_a.get()
    b = textbox_b.get()
    fx = textbox_fx.get()
    iterations = textbox_iterations.get()
    if not a or not b or not fx or not iterations:
        show_error("Eroare", "Toate campurile trebuie completate!")
        return
    if not (a.replace('.', '', 1).isdigit() or (a.startswith('-') and a[1:].replace('.', '', 1).isdigit())):
        show_error("Eroare", "Introduceți doar numere pentru a!")
        return
    if not (b.replace('.', '', 1).isdigit() or (b.startswith('-') and b[1:].replace('.', '', 1).isdigit())):
        show_error("Eroare", "Introduceți doar numere pentru b!")
        return
    
    a = float(a)
    b = float(b)
    

    try:
        float(iterations)
    except ValueError:
        show_error("Eroare", "Introduceti doar numere pentru iteratii!")
        return
    
    if not selected_method.get()=="secant" and not selected_method.get()=="bisection":
        show_error("Eroare", "Selectati o metoda!")
        return
    
    if is_valid_function(fx):
        print("Textul reprezintă o funcție validă.")
    else:
        print("Textul nu reprezintă o funcție validă.")

        
    

def is_valid_function(text):
    try:
        # Transformă textul într-un nod AST (Abstract Syntax Tree)
        node = ast.parse(text, mode='eval')

        # Verifică dacă nodul este de tip Expression și conține un nod de tip Call (apel de funcție)
        if isinstance(node, ast.Expression) and isinstance(node.body, ast.Call):
            # Verifică dacă numele funcției este în lista de funcții matematice
            if isinstance(node.body.func, ast.Name) and node.body.func.id in math.__dict__:
                return True
            else:
                return False
        else:
            return False
    except SyntaxError:
        return False
# functie care calculeaza ce avem nevoie in functie de ce metoda alegi
def calculate(): 
    errors()
    if selected_method.get() == "bisection":
        a = float(textbox_a.get())
        b = float(textbox_b.get())
        fx = textbox_fx.get()
        iterations = float(textbox_iterations.get())
        f = lambda x: eval(fx)
        en = textbox_en.get()
        
        result = my_bisection(f, a, b, iterations)
        # Afișați rezultatele în câmpurile de text din panoul "Rezultate"
        textbox_xn.configure(state="normal")
        textbox_xn.delete(0, "end")
        textbox_xn.insert(0, result)
        textbox_xn.configure(state="disabled")

        # Calculați eroarea absolută
        error = f(result)
        textbox_error.configure(state="normal")
        textbox_error.delete(0, "end")
        textbox_error.insert(0, error)
        textbox_error.configure(state="disabled")

        # Calculează și afișează timpul de execuție pentru metoda my_bisection
        start_time_bisection = time.time()
        result_bisection = my_bisection(f, a, b, iterations)
        elapsed_time_bisection = time.time() - start_time_bisection
        
        textbox_method_wait.configure(state="normal")
        textbox_method_wait.delete(0, "end")
        textbox_method_wait.insert(0, elapsed_time_bisection)
        textbox_method_wait.configure(state="disabled")
        
        # Calculează și afișează timpul de execuție pentru fsolve
        start_time_fsolve = time.time()
        result_fsolve = fsolve(f, a)
        elapsed_time_fsolve = time.time() - start_time_fsolve
        
        textbox_fzero_wait.configure(state="normal")
        textbox_fzero_wait.delete(0, "end")
        textbox_fzero_wait.insert(0, elapsed_time_fsolve)
        textbox_fzero_wait.configure(state="disabled")

        # Realizați și afișați graficul funcției f(x)
        x_plt = np.linspace(a, b, 50)
        y_plt = f(x_plt)
        
        fig = plt.figure()
        plt.plot(x_plt, y_plt)
        plt.axhline()
        
        fig = plt.figure(facecolor='#343638')  # Set the background color of the figure

        # Create an axes object within the figure and set its background color
        ax = fig.add_subplot(111, facecolor='none')

        ax.plot(x_plt, y_plt, color='blue')  # Set the color of the plot lines
        ax.axhline(color='blue')  # Set the color of the horizontal line

        # Set the color of the axis labels and ticks to white
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Set the color of the plot's border to white
        for spine in ax.spines.values():
           spine.set_edgecolor('white')

        values_text.configure(fg="white")
        values = []
        for x in x_plt:
            values.append(f(x))
        values_text.configure(state="normal")
        values_text.delete("1.0", "end")
        values_text.insert("1.0", "\n".join(str(value) for value in values))
        values_text.configure(state="disabled")
        
        # Create the Tkinter canvas for the graph
        graph_canvas = FigureCanvasTkAgg(fig, master=window)
        graph_canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        graph_canvas.draw()
        
    elif selected_method.get() == "secant":        
        a = float(textbox_a.get())
        b = float(textbox_b.get())
        fx = textbox_fx.get()
        f = lambda x : eval(fx)
        iterations = textbox_iterations.get()
        en = textbox_en.get()
        
        
        result = coarda_er(fx, a, b, en)

        # Afișați rezultatele în câmpurile de text din panoul "Rezultate"
        textbox_xn.configure(state="normal")
        textbox_xn.delete(0, "end")
        textbox_xn.insert(0, result)
        textbox_xn.configure(state="disabled")

        # Calculați eroarea absolută
        error = f(result)
        textbox_error.configure(state="normal")
        textbox_error.delete(0, "end")
        textbox_error.insert(0, error)
        textbox_error.configure(state="disabled")

        # Calculează și afișează timpul de execuție pentru metoda coarda_er
        start_time_coarda = time.time()
        result_coarda = coarda_er(fx, a, b, en)
        elapsed_time_coarda = time.time() - start_time_coarda
        
        textbox_method_wait.configure(state="normal")
        textbox_method_wait.delete(0, "end")
        textbox_method_wait.insert(0, elapsed_time_coarda)
        textbox_method_wait.configure(state="disabled")
        
        # Calculează și afișează timpul de execuție pentru fsolve
        start_time_fsolve = time.time()
        result_fsolve = fsolve(f, a)
        elapsed_time_fsolve = time.time() - start_time_fsolve
        
        textbox_fzero_wait.configure(state="normal")
        textbox_fzero_wait.delete(0, "end")
        textbox_fzero_wait.insert(0, elapsed_time_fsolve)
        textbox_fzero_wait.configure(state="disabled")

        # Realizați și afișați graficul funcției f(x)
        x_plt = np.linspace(a, b, 50)
        y_plt = f(x_plt)
        
        fig = plt.figure()
        plt.plot(x_plt, y_plt)
        plt.axhline()
        
        fig = plt.figure(facecolor='#343638')  # Set the background color of the figure

        # Create an axes object within the figure and set its background color
        ax = fig.add_subplot(111, facecolor='none')

        ax.plot(x_plt, y_plt, color='blue')  # Set the color of the plot lines
        ax.axhline(color='blue')  # Set the color of the horizontal line

        # Set the color of the axis labels and ticks to white
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Set the color of the plot's border to white
        for spine in ax.spines.values():
           spine.set_edgecolor('white')

        values_text.configure(fg="white")
        values = []
        for x in x_plt:
            values.append(f(x))
        values_text.configure(state="normal")
        values_text.delete("1.0", "end")
        values_text.insert("1.0", "\n".join(str(value) for value in values))
        values_text.configure(state="disabled")
        
        # Create the Tkinter canvas for the graph
        graph_canvas = FigureCanvasTkAgg(fig, master=window)
        graph_canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        graph_canvas.draw()
        return
        

# Create components for inputting values
label_a = customtkinter.CTkLabel(window, text="a:", font=("Arial", 12))
label_a.grid(row=0, column=0, padx=10, pady=10)
textbox_a = customtkinter.CTkEntry(window)
textbox_a.grid(row=0, column=1, padx=10, pady=10)

label_b = customtkinter.CTkLabel(window, text="b:", font=("Arial", 12))
label_b.grid(row=1, column=0, padx=10, pady=10)
textbox_b = customtkinter.CTkEntry(window)
textbox_b.grid(row=1, column=1, padx=10, pady=10)

label_fx = customtkinter.CTkLabel(window, text="f(x):", font=("Arial", 12))
label_fx.grid(row=2, column=0, padx=10, pady=10)
textbox_fx = customtkinter.CTkEntry(window)
textbox_fx.grid(row=2, column=1, padx=10, pady=10)

# Create the "Stop Criteria" panel
criteria_frame = tk.LabelFrame(window, text="Criterii de oprire", font=("Arial", 12),bg="#1A1A1A", fg="white")
criteria_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

label_iterations = customtkinter.CTkLabel(criteria_frame, text="Numar de iteratii:", font=("Arial", 12))
label_iterations.grid(row=0, column=0, padx=10, pady=5)
textbox_iterations = customtkinter.CTkEntry(criteria_frame)
textbox_iterations.grid(row=0, column=1, padx=10, pady=5)

label_en = customtkinter.CTkLabel(criteria_frame, text="E(n):", font=("Arial", 12))
label_en.grid(row=1, column=0, padx=10, pady=5)
textbox_en = customtkinter.CTkEntry(criteria_frame)
textbox_en.grid(row=1, column=1, padx=10, pady=5)

# Create components for selecting the method
method_label = customtkinter.CTkLabel(window, text="Selectati metoda:", font=("Arial", 12))
method_label.grid(row=0, column=3, padx=10, pady=10)

# Variable for the selected option
selected_method = tk.StringVar()

# Create radio buttons
radio_bisection = customtkinter.CTkRadioButton(window, text="Metoda Bisectiei", variable=selected_method, value="bisection", font=("Arial", 12))
radio_bisection.grid(row=1, column=3, padx=10, pady=5)

radio_secant = customtkinter.CTkRadioButton(window, text="Metoda Coardei", variable=selected_method, value="secant", font=("Arial", 12))
radio_secant.grid(row=2, column=3, padx=10, pady=5)

# Deselect the initial option
selected_method.set(None)

# Create components for displaying approximate values
# Create the "Results" panel
results_frame = tk.LabelFrame(window, text="Rezultate", font=("Arial", 12), bg="#1A1A1A", fg="white")
results_frame.grid(row=0, column=4, rowspan=3, padx=10, pady=10, sticky="nsew")

label_xn = customtkinter.CTkLabel(results_frame, text="xn:", font=("Arial", 12))
label_xn.grid(row=0, column=0, padx=10, pady=5)
textbox_xn = customtkinter.CTkEntry(results_frame, state="disabled")
textbox_xn.grid(row=0, column=1, padx=10, pady=5)

label_error = customtkinter.CTkLabel(results_frame, text="Eroare absoluta:", font=("Arial", 12))
label_error.grid(row=1, column=0, padx=10, pady=5)
textbox_error = customtkinter.CTkEntry(results_frame, state="disabled")
textbox_error.grid(row=1, column=1, padx=10, pady=5)

label_method_wait = customtkinter.CTkLabel(results_frame, text="Timp de asteptare pentru metoda:", font=("Arial", 12))
label_method_wait.grid(row=2, column=0, padx=10, pady=5)
textbox_method_wait = customtkinter.CTkEntry(results_frame, state="disabled")
textbox_method_wait.grid(row=2, column=1, padx=10, pady=5)

label_fzero_wait = customtkinter.CTkLabel(results_frame, text="Timp de asteptare pentru fzero:", font=("Arial", 12))
label_fzero_wait.grid(row=3, column=0, padx=10, pady=5)
textbox_fzero_wait = customtkinter.CTkEntry(results_frame, state="disabled")
textbox_fzero_wait.grid(row=3, column=1, padx=10, pady=5)

# Create components for the graph
graph_label = customtkinter.CTkLabel(window, text="Grafic:", font=("Arial", 14))
graph_label.grid(row=3, column=0, padx=10, pady=10)
graph_canvas = customtkinter.CTkCanvas(window, width=450, height=350, bg="#343638", highlightbackground="#5f6568")
graph_canvas.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Create the calculation button
calculate_button = customtkinter.CTkButton(window,width=160,
                                 height=62, text="Calculeaza", command=calculate, font=("Arial", 25))
calculate_button.grid(row=4, column=4, padx=10, pady=10)

# Set the font size for all labels
labels = [label_a, label_b, label_fx, label_iterations, label_en, label_xn, label_error, label_method_wait, label_fzero_wait, method_label, graph_label]
for label in labels:
    label.configure(font=("Arial", 18))

# Create the "Valori Funcție" panel
values_frame = tk.LabelFrame(window, text="Valori Functie", font=("Arial", 12), bg="#1A1A1A", fg="white")
values_frame.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

values_text = tk.Text(values_frame, width=30, height=20, bg="#343638", state="disabled")
values_text.grid(row=0, column=0, padx=10, pady=10)

def append_value(value):
    values_text.insert(tk.END, str(value) + "\n")

# Start the main GUI loop
window.mainloop()