import tkinter as tk
import empresa as em
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import calendar
import os

# Create an instance of the Empresa class
empresa = em.Empresa()

# Create the main Tkinter window
root = tk.Tk()
root.title("Organizar Calendário")
root.geometry("800x600")
icon_path = os.path.join(os.path.dirname(__file__), 'image.ico')
root.iconbitmap(icon_path)

# Label for the main title
label = tk.Label(root, text="Organização de Calendário", font=("Arial", 16))
label.pack(pady=10)

# Error label for displaying error messages
error_label = tk.Label(root, text="", fg="red", font=("Arial", 12))
error_label.pack(pady=5)

# Text area for displaying the calendar
calendar_text = tk.Text(root, height=10, width=50)
calendar_text.pack(pady=10)

# Function to view the current calendar
def view_calendar():
    error_message = empresa.preencherCalendario()
    if error_message:
        error_label.config(text=error_message)
    else:
        calendar_text.delete(1.0, tk.END)
        for week in empresa.calendario:
            calendar_text.insert(tk.END, f"{week}\n")

# Button to view the calendar
view_calendar_button = tk.Button(root, text="Ver Calendário", command=view_calendar)
view_calendar_button.pack(pady=10)

# Entry field for adding a new employee
new_employee_entry = tk.Entry(root, width=30)
new_employee_entry.pack(pady=5)
new_employee_entry.insert(0, "Nome de funcionário")

# Function to add a new employee
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

# Button to add a new employee
add_employee_button = tk.Button(root, text="Adicionar", command=add_employee)
add_employee_button.pack(pady=5)

# Entry field for removing an employee
remove_employee_entry = tk.Entry(root, width=30)
remove_employee_entry.pack(pady=5)
remove_employee_entry.insert(0, "Nome de funcionário")

# Function to remove an employee
def remove_employee():
    employee_to_remove = remove_employee_entry.get()
    if employee_to_remove:
        error_message = empresa.retirarFuncionario(employee_to_remove)
        if error_message:
            error_label.config(text=error_message)  # Show error message
        else:
            label.config(text=f"Removido: {employee_to_remove}")
            error_label.config(text="")  # Clear any previous error
            remove_employee_entry.delete(0, tk.END)  # Clear the entry field

# Button to remove an employee
remove_employee_button = tk.Button(root, text="Remover", command=remove_employee)
remove_employee_button.pack(pady=5)

add_subtitle_entry = tk.Entry(root, width=30)
add_subtitle_entry.pack(pady=5)
add_subtitle_entry.insert(0, "Titulo")

def create_simple_calendar_pdf():
    year = datetime.now().year  # Set the year for which the calendar is generated
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

    cols = 2  # Number of columns for months
    rows = 6  # Number of rows for months
    month_width = (width / cols) * size_multiplier
    month_height = (height / rows) * size_multiplier

    # Title and subtitle
    title_width = c.stringWidth(title, "Helvetica-Bold", 16 * size_multiplier)
    subtitle_width = c.stringWidth(subtitle, "Helvetica", 12 * size_multiplier)
    c.setFont("Helvetica-Bold", 16 * size_multiplier)
    c.drawString((width - title_width) / 2, height - 30 * size_multiplier, title)
    c.setFont("Helvetica", 12 * size_multiplier)
    c.drawString((width - subtitle_width) / 2, height - 50 * size_multiplier, subtitle)

    last_week_employee = None  # Track the last week's employee
    week_counter = 0  # Global week counter to rotate employees
    employee_rotation = empresa.funcionarios  # Assuming `empresa.funcionarios` is the list of employee names

    for month in range(1, 13):
        col = (month - 1) % cols
        row = (month - 1) // cols
        x = col * month_width + col * space_x + month_x
        y = height - (row + 1) * month_height - row * space_y - 60 * size_multiplier + month_y

        # Month title
        month_name = calendar.month_name[month]
        c.setFillColor(colors.blue)
        c.rect(x, y + month_height - 20 * size_multiplier, month_width, 20 * size_multiplier, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12 * size_multiplier)

        # Center the month title        
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

        # Calendar days
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

            # Week label for the first week of the month
            if week_index == 0:
                c.rect(emp_rect_x, emp_rect_y + emp_rect_height + 2, emp_rect_width, emp_rect_height, stroke=1, fill=0)
                c.drawString(emp_rect_x + (emp_rect_width - string_width) / 2, emp_rect_y + emp_rect_height + 2 + (emp_rect_height - 10 * size_multiplier) / 2, "Nome")

            y_offset -= 20 * size_multiplier

    c.save()
    label.config(text = f"PDF '{pdf_file}' created successfully!")

create_pdf_button = tk.Button(root, text="Criar PDF do Calendário", command=create_simple_calendar_pdf)
create_pdf_button.pack(pady=10)


if __name__ == "__main__":
    root.mainloop()