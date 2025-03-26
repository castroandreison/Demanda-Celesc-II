import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os



# Tabelas de Demanda em kVA
tabela_trifasico = {
    Fraction(1, 3): [0.65, 0.98, 1.24, 1.5, 1.76, 1.95, 2.15, 2.34, 2.53, 2.73],
    Fraction(1, 2): [0.87, 1.31, 1.65, 2.0, 2.35, 2.61, 2.87, 3.13, 3.39, 3.65],
    Fraction(3, 4): [1.26, 1.89, 2.39, 2.9, 3.4, 3.78, 4.16, 4.54, 4.91, 5.29],
    Fraction(1, 1): [1.52, 2.28, 2.89, 3.5, 4.1, 4.56, 5.02, 5.47, 5.93, 6.38],
    Fraction(3, 2): [2.17, 3.26, 4.12, 4.99, 5.86, 6.51, 7.16, 7.81, 8.46, 9.11],
    Fraction(2, 1): [2.7, 4.05, 5.13, 6.21, 7.29, 8.1, 8.91, 9.72, 10.53, 11.34],
    Fraction(3, 1): [4.04, 6.06, 7.68, 9.29, 10.91, 12.12, 13.33, 14.54, 15.76, 16.97],
    Fraction(4, 1): [5.03, 7.55, 9.56, 11.57, 13.58, 15.09, 16.6, 18.11, 19.62, 21.13],
    Fraction(5, 1): [6.02, 9.03, 11.44, 13.85, 16.25, 18.06, 19.87, 21.67, 23.48, 25.28],
    Fraction(15, 2): [8.65, 12.98, 16.44, 19.9, 23.36, 25.95, 28.55, 31.14, 33.74, 36.33],
    Fraction(10, 1): [11.54, 17.31, 21.93, 26.54, 31.16, 34.62, 38.03, 41.54, 45.01, 48.47],
    Fraction(25, 2): [14.09, 21.14, 26.77, 32.41, 38.04, 42.27, 46.5, 50.72, 54.95, 59.18],
    Fraction(15, 1): [16.65, 24.98, 31.63, 33.29, 44.96, 49.95, 54.95, 59.94, 64.93, 69.93],
    Fraction(20, 1): [22.1, 33.15, 41.99, 50.83, 59.67, 66.3, 72.93, 79.56, 86.19, 92.82],
    Fraction(25, 1): [25.83, 38.75, 49.08, 59.41, 69.74, 77.49, 85.24, 92.99, 100.74, 103.49],
    Fraction(30, 1): [30.52, 45.78, 57.99, 70.2, 82.4, 91.56, 100.72, 109.87, 119.03, 128.18]
}

tabela_monofasico = {
    Fraction(1, 4): [0.66, 0.99, 1.254, 1.518, 1.782, 1.98, 2.178, 2.376, 2.574, 2.772],
    Fraction(1, 3): [0.77, 1.155, 1.463, 1.771, 2.079, 2.31, 2.541, 2.772, 3.003, 3.234],
    Fraction(1, 2): [1.18, 1.77, 2.242, 2.714, 3.186, 3.54, 3.894, 4.248, 4.602, 4.956],
    Fraction(3, 4): [1.34, 2.01, 2.246, 3.032, 3.618, 4.02, 4.422, 4.824, 5.226, 5.628],
    Fraction(1, 1): [1.56, 2.34, 2.964, 3.588, 4.212, 4.68, 5.148, 5.616, 6.084, 6.552],
    Fraction(3, 2): [2.35, 3.525, 4.465, 5.405, 6.345, 7.05, 7.755, 8.46, 9.165, 9.87],
    Fraction(2, 1): [2.97, 4.455, 5.643, 6.831, 8.019, 8.91, 9.801, 10.692, 11.583, 12.474],
    Fraction(3, 1): [4.07, 6.105, 7.733, 9.361, 10.989, 12.21, 13.431, 14.652, 15.873, 17.094],
    Fraction(5, 1): [6.16, 9.24, 11.704, 14.168, 16.632, 18.48, 20.328, 22.176, 24.024, 25.872]
}

fatores_trifasico = {
    1: 1, 2: 0.75, 3: 0.633, 4: 0.575, 5: 0.54, 6: 0.5, 7: 0.471, 8: 0.45, 9: 0.433, 10: 0.42
}

fatores_monofasico = {
    1: 1, 2: 0.75, 3: 0.633, 4: 0.575, 5: 0.54, 6: 0.5, 7: 0.471, 8: 0.45, 9: 0.433, 10: 0.42
}

def atualizar_potencias(event):
    tipo = tipo_var.get()
    if tipo == 'Trifásico':
        potencias = list(tabela_trifasico.keys())
    else:
        potencias = list(tabela_monofasico.keys())
    
    potencia_combobox['values'] = [str(p) for p in potencias]
    potencia_combobox.current(0)

def calcular_kva(tipo, potencia, quantidade):
    if tipo == 'Trifásico':
        tabela = tabela_trifasico
        fator = fatores_trifasico[quantidade]
    else:
        tabela = tabela_monofasico
        fator = fatores_monofasico[quantidade]
    
    if potencia in tabela:
        if 1 <= quantidade <= 10:
            return tabela[potencia][quantidade-1], fator
        else:
            messagebox.showerror("Erro", "Quantidade de motores deve ser entre 1 e 10.")
    else:
        messagebox.showerror("Erro", "Potência não encontrada na tabela.")

    return None, None

def adicionar_motor():
    tipo = tipo_var.get()
    potencia = Fraction(potencia_combobox.get())
    quantidade = int(quantidade_spinbox.get())
    descricao = descricao_entry.get()
    kva, fator = calcular_kva(tipo, potencia, quantidade)
    
    if kva:
        lista_motores.insert("", "end", values=(tipo, str(potencia), quantidade, f"{kva:.2f}", f"{fator:.3f}", descricao))
        descricao_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Não foi possível calcular a demanda em kVA.")

def editar_motor():
    selected_item = lista_motores.selection()
    if selected_item:
        item = lista_motores.item(selected_item)
        valores = item['values']
        
        tipo_var.set(valores[0])
        potencia_combobox.set(valores[1])
        quantidade_spinbox.delete(0, tk.END)
        quantidade_spinbox.insert(0, valores[2])
        descricao_entry.delete(0, tk.END)
        descricao_entry.insert(0, valores[5])
        
        lista_motores.delete(selected_item)
    else:
        messagebox.showwarning("Atenção", "Selecione um motor para editar.")

def excluir_motor():
    selected_item = lista_motores.selection()
    if selected_item:
        lista_motores.delete(selected_item)
    else:
        messagebox.showwarning("Atenção", "Selecione um motor para excluir.")

def calcular_total():
    total_kva = sum(float(item[3]) for item in lista_motores.get_children())
    messagebox.showinfo("Total de Demanda", f"Demanda total: {total_kva:.2f} kVA")

def gerar_relatorio_pdf():
    pdf_path = "relatorio_demanda_motores.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    c.drawString(30, height - 50, "Relatório de Demanda de Motores")
    
    y_position = height - 80
    c.drawString(30, y_position, "Tipo")
    c.drawString(120, y_position, "Potência (kW)")
    c.drawString(200, y_position, "Quantidade")
    c.drawString(300, y_position, "Demanda (kVA)")
    c.drawString(380, y_position, "Fator de Demanda")
    c.drawString(470, y_position, "Descrição")
    
    y_position -= 20
    
    total_kva = 0
    
    for item in lista_motores.get_children():
        values = lista_motores.item(item)['values']
        c.drawString(30, y_position, values[0])
        c.drawString(120, y_position, values[1])
        c.drawString(200, y_position, str(values[2]))
        c.drawString(300, y_position, values[3])
        c.drawString(380, y_position, values[4])
        c.drawString(470, y_position, values[5])
        y_position -= 20
        total_kva += float(values[3])
    
    y_position -= 20
    c.drawString(30, y_position, f"Demanda Total: {total_kva:.2f} kVA")
    
    c.save()
    messagebox.showinfo("Relatório Gerado", f"Relatório gerado com sucesso: {pdf_path}")

root = tk.Tk()
root.title("Gerenciamento de Motores")

# Tipo de motor
tipo_label = tk.Label(root, text="Tipo de Motor:")
tipo_label.grid(row=0, column=0, padx=10, pady=10)
tipo_var = tk.StringVar(value="Trifásico")
tipo_combobox = ttk.Combobox(root, textvariable=tipo_var, values=["Trifásico", "Monofásico"])
tipo_combobox.grid(row=0, column=1, padx=10, pady=10)
tipo_combobox.bind("<<ComboboxSelected>>", atualizar_potencias)

# Potência do motor
potencia_label = tk.Label(root, text="Potência (kW):")
potencia_label.grid(row=1, column=0, padx=10, pady=10)
potencia_combobox = ttk.Combobox(root)
potencia_combobox.grid(row=1, column=1, padx=10, pady=10)

# Quantidade de motores
quantidade_label = tk.Label(root, text="Quantidade:")
quantidade_label.grid(row=2, column=0, padx=10, pady=10)
quantidade_spinbox = tk.Spinbox(root, from_=1, to=10)
quantidade_spinbox.grid(row=2, column=1, padx=10, pady=10)

# Descrição do motor
descricao_label = tk.Label(root, text="Descrição:")
descricao_label.grid(row=3, column=0, padx=10, pady=10)
descricao_entry = tk.Entry(root)
descricao_entry.grid(row=3, column=1, padx=10, pady=10)

# Botões
adicionar_button = tk.Button(root, text="Adicionar Motor", command=adicionar_motor)
adicionar_button.grid(row=4, column=0, padx=10, pady=10)

editar_button = tk.Button(root, text="Editar Motor", command=editar_motor)
editar_button.grid(row=4, column=1, padx=10, pady=10)

excluir_button = tk.Button(root, text="Excluir Motor", command=excluir_motor)
excluir_button.grid(row=4, column=2, padx=10, pady=10)

calcular_button = tk.Button(root, text="Calcular Total", command=calcular_total)
calcular_button.grid(row=5, column=0, padx=10, pady=10)

relatorio_button = tk.Button(root, text="Gerar Relatório", command=gerar_relatorio_pdf)
relatorio_button.grid(row=5, column=1, padx=10, pady=10)

# Lista de motores
lista_motores = ttk.Treeview(root, columns=("Tipo", "Potência", "Quantidade", "kVA", "Fator", "Descrição"), show="headings")
lista_motores.heading("Tipo", text="Tipo")
lista_motores.heading("Potência", text="Potência (kW)")
lista_motores.heading("Quantidade", text="Quantidade")
lista_motores.heading("kVA", text="Demanda (kVA)")
lista_motores.heading("Fator", text="Fator de Demanda")
lista_motores.heading("Descrição", text="Descrição")

lista_motores.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Inicializa as potências disponíveis com base no tipo de motor padrão
atualizar_potencias(None)

root.mainloop()
