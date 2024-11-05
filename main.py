import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import maintenance as em
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import calendar
import os

main = em.Maintenance()

root = tk.Tk()

notebook = ttk.Notebook(root)

root.geometry("800x600")
icon_path = os.path.join(os.path.dirname(__file__), 'image.ico')
root.iconbitmap(icon_path)

# Starting tabs
tab1 = tk.Frame(notebook, bg="lightblue")
tab2 = tk.Frame(notebook, bg="lightblue")
tab3 = tk.Frame(notebook, bg="lightblue")

# Giving the "name" of the tabs
notebook.add(tab1, text="Manutenção")
notebook.add(tab2, text="Notificação")
notebook.add(tab3, text="Visualização")

notebook.pack(expand=True, fill="both")

# Starting fonts
titleFont = ("Arial", 26)
errorFont = ("Arial", 25)
infoFont = ("Arial", 20)
formFont = ("Arial", 12)

# Tab 1 - Maintenance
title_tab1 = tk.Label(tab1, text="Manutenção de Funcionários", font=titleFont, bg="lightblue")
title_tab1.pack(padx=20, pady=20)

error_label_tab1 = tk.Label(tab1, text="", font=errorFont, bg='lightblue', fg='red')
error_label_tab1.pack(padx=20, pady=10)

info_label_tab1 = tk.Label(tab1, text="", font=infoFont, bg='lightblue', fg='yellow')
info_label_tab1.pack(padx=20, pady=10)

button_new_employ = tk.Button(tab1, text="Adicionar Funcionário")
button_new_employ.pack(padx=30, pady=40)

button_remove_employ = tk.Button(tab1, text="Remover Funcionário")
button_remove_employ.pack(padx=60, pady=40)

#Tab 2 - Notification
title_tab2 = tk.Label(tab2, text="Notificação de Funcionários", font=titleFont, bg="lightblue")
title_tab2.pack(padx=20, pady=20)

#Tab 3 - Visualization
title_tab3 = tk.Label(tab3, text="Visualização do Calendário e Geração de PDF", font=titleFont, bg="lightblue")
title_tab3.pack(padx=20, pady=20)

if __name__ == "__main__":
    root.mainloop()