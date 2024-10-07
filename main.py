import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import empresa as em
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import calendar
import os

# Instanciação do objeto da classe Empresa
empresa = em.Empresa()

# Tela principal do tkinter
root = tk.Tk()

# Instanciação do Notebook para criação de guias
notebook = ttk.Notebook(root)

root.geometry("800x600")
icon_path = os.path.join(os.path.dirname(__file__), 'image.ico')
root.iconbitmap(icon_path)

# Inicializa as guias
tab1 = tk.Frame(notebook, bg="lightblue")
tab2 = tk.Frame(notebook, bg="lightblue")
tab3 = tk.Frame(notebook, bg="lightblue")

# Adiciona o "nome" das guias
notebook.add(tab1, text="Manutenção")
notebook.add(tab2, text="Notificação")
notebook.add(tab3, text="Visualização")

notebook.pack(expand=True, fill="both")

# Declaração das funções

def open_form():
    form_window = tk.Toplevel(root)
    form_window.title("Form")
    form_window.geometry("300x200")
    
    icon_path = os.path.join(os.path.dirname(__file__), 'formimage.ico')
    form_window.iconbitmap(icon_path)
    
    tk.Label(form_window, text="Nome:", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(form_window, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(form_window, text="Email:", font=("Arial", 12)).pack(pady=5)
    email_entry = tk.Entry(form_window, font=("Arial", 12))
    email_entry.pack(pady=5)
    
    submit_button = tk.Button(form_window, text="Adicionar", font=("Arial", 12), command=lambda: submit_form(name_entry.get(), email_entry.get()))
    submit_button.pack(pady=20)

def submit_form(name, email):
    print(f"Name: {name}, Email: {email}")

def view_calendar():
    error_message = empresa.preencherCalendario()
    if error_message:
        error_label.config(text=error_message)
    else:
        calendar_text.delete(1.0, tk.END)
        for week in empresa.calendario:
            calendar_text.insert(tk.END, f"{week}\n")

def add_employee():
    new_employee = new_employee_entry.get()
    if new_employee:
        error_message = empresa.adicionarFuncionario(new_employee)
        if error_message:
            error_label.config(text=error_message)  # Show error message
        else:
            label.config(text=f"Adicionado: {new_employee}")
            error_label.config(text="")  # Clear any previous error 
            new_employee_entry.delete(0, tk.END)  # Clear the entry field

def remove_employee():
    employee_to_remove = remove_employee_entry.get()
    if employee_to_remove:
        error_message = empresa.retirarFuncionario(employee_to_remove)
        if error_message:
            error_label.config(text=error_message)  
        else:
            label.config(text=f"Removido: {employee_to_remove}")
            error_label.config(text="") 
            remove_employee_entry.delete(0, tk.END) 


def create_simple_calendar_pdf():
    year = datetime.now().year
    size_multiplier = 0.6
    space_x = 100
    space_y = 30
    month_x = 80
    month_y = -20
    title = '2024'
    subtitle = add_subtitle_entry.get()
    emp_rect_width = 70
    emp_rect_height = 10
    emp_rect_offset_x = 185
    emp_rect_offset_y = 0
    pdf_file = "Calendario" + str(year) + ".pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    cols = 2
    rows = 6 
    month_width = (width / cols) * size_multiplier
    month_height = (height / rows) * size_multiplier

    # Title and subtitle
    title_width = c.stringWidth(title, "Helvetica-Bold", 16 * size_multiplier)
    subtitle_width = c.stringWidth(subtitle, "Helvetica", 12 * size_multiplier)
    c.setFont("Helvetica-Bold", 16 * size_multiplier)
    c.drawString((width - title_width) / 2, height - 30 * size_multiplier, title)
    c.setFont("Helvetica", 12 * size_multiplier)
    c.drawString((width - subtitle_width) / 2, height - 50 * size_multiplier, subtitle)

    last_week_employee = None
    week_counter = 0 
    employee_rotation = empresa.funcionarios

    for month in range(1, 13):
        col = (month - 1) % cols
        row = (month - 1) // cols
        x = col * month_width + col * space_x + month_x
        y = height - (row + 1) * month_height - row * space_y - 60 * size_multiplier + month_y

        month_name = calendar.month_name[month]
        c.setFillColor(colors.blue)
        c.rect(x, y + month_height - 20 * size_multiplier, month_width, 20 * size_multiplier, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12 * size_multiplier)

        month_title_width = c.stringWidth(month_name, "Helvetica-Bold", 12 * size_multiplier)
        c.drawString(x + (month_width - month_title_width) / 2, y + month_height - 15 * size_multiplier, month_name)

        c.setFillColor(colors.lightgrey)
        c.rect(x, y + month_height - 40 * size_multiplier, month_width, 20 * size_multiplier, stroke=0, fill=1)
        c.setFillColor(colors.black)
        days = ["D", "S", "T", "Q", "Q", "S", "S"]

        for i, day in enumerate(days):
            c.setFont("Helvetica", 10 * size_multiplier)
            day_width = c.stringWidth(day, "Helvetica", 10 * size_multiplier)
            c.drawString(x + (i * (month_width / 7)) + (month_width / 7 - day_width) / 2, y + month_height - 35 * size_multiplier, day)

        month_calendar = calendar.monthcalendar(year, month)
        y_offset = y + month_height - 60 * size_multiplier

        for week_index, week in enumerate(month_calendar):
            is_partial_week = any(day == 0 for day in week)

            if is_partial_week and week_index == 0:
                current_employee = last_week_employee
                week_counter += 1

            elif is_partial_week and week_index == len(month_calendar) - 1:
                current_employee = employee_rotation[week_counter % len(employee_rotation)]
                last_week_employee = current_employee

            else:
                current_employee = employee_rotation[week_counter % len(employee_rotation)]
                week_counter += 1
                last_week_employee = current_employee

            for i, day in enumerate(week):
                if day != 0:
                    c.rect(x + (i * (month_width / 7)), y_offset, month_width / 7, 20 * size_multiplier, stroke=1, fill=0)
                    day_num_width = c.stringWidth(str(day), "Helvetica", 10 * size_multiplier)
                    c.drawString(x + (i * (month_width / 7)) + (month_width / 7 - day_num_width) / 2, y_offset + 5 * size_multiplier, str(day))

            emp_rect_x = x + month_width - emp_rect_width - emp_rect_offset_x
            emp_rect_y = y_offset + emp_rect_offset_y
            string_width = c.stringWidth(current_employee, "Helvetica", 10 * size_multiplier)

            c.rect(emp_rect_x, emp_rect_y, emp_rect_width, emp_rect_height, stroke=1, fill=0)
            c.drawString(emp_rect_x + (emp_rect_width - string_width) / 2, emp_rect_y + (emp_rect_height - 10 * size_multiplier) / 2, current_employee)

            if week_index == 0:
                c.rect(emp_rect_x, emp_rect_y + emp_rect_height + 2, emp_rect_width, emp_rect_height, stroke=1, fill=0)
                c.drawString(emp_rect_x + (emp_rect_width - string_width) / 2, emp_rect_y + emp_rect_height + 2 + (emp_rect_height - 10 * size_multiplier) / 2, "Nome")

            y_offset -= 20 * size_multiplier

    c.save()
    label.config(text = f"PDF '{pdf_file}'")

# Declaração de fontes
titleFont = ("Arial", 20)

# Tab 1 - Manutenção
title_tab1 = tk.Label(tab1, text="Manutenção de Funcionários", font=titleFont, bg="lightblue")
title_tab1.pack(padx=20, pady=20)

button_new_employ = tk.Button(tab1, text="Adicionar Funcionário", command=open_form)
button_new_employ.pack(padx=30, pady=40)

button_remove_employ = tk.Button(tab1, text="Remover Funcionário")
button_remove_employ.pack(padx=60, pady=40)

#Tab 2 - Notificação
title_tab2 = tk.Label(tab2, text="Notificação de Funcionários", font=titleFont, bg="lightblue")
title_tab2.pack(padx=20, pady=20)


#Tab 3 - Visualização
title_tab3 = tk.Label(tab3, text="Visualização do Calendário e Geração de PDF", font=titleFont, bg="lightblue")
title_tab3.pack(padx=20, pady=20)

if __name__ == "__main__":
    root.mainloop()