import tkinter as tk
from tkinter import ttk
from reportlab.pdfgen import canvas
from datetime import datetime

# Especificações dos barramentos conforme o disjuntor
barramento_specs = {
    "ATÉ 125 A": {"Seção Mínima (mm²)": "60 mm²", "Pol (L x E)": "7/8 x 1/8", "mm (L x E)": "22,23 x 3,18"},
    "ATÉ 150 A": {"Seção Mínima (mm²)": "75 mm²", "Pol (L x E)": "1 x 1/8", "mm (L x E)": "25,4 x 3,18"},
    "ATÉ 200 A": {"Seção Mínima (mm²)": "90 mm²", "Pol (L x E)": "1 x 5/32", "mm (L x E)": "25,4 x 3,97"},
    "ATÉ 250 A": {"Seção Mínima (mm²)": "120 mm²", "Pol (L x E)": "1 x 3/16", "mm (L x E)": "25,4 x 4,76"},
    "ATÉ 350 A": {"Seção Mínima (mm²)": "150 mm²", "Pol (L x E)": "1 x 1/4", "mm (L x E)": "25,4 x 6,35"},
    "ATÉ 500 A": {"Seção Mínima (mm²)": "200 mm²", "Pol (L x E)": "1 1/4 x 1/4", "mm (L x E)": "31,75 x 6,35"},
    "ATÉ 650 A": {"Seção Mínima (mm²)": "240 mm²", "Pol (L x E)": "1 x 3/8", "mm (L x E)": "25,4 x 9,53"},
    "ATÉ 700 A": {"Seção Mínima (mm²)": "300 mm²", "Pol (L x E)": "1 1/2 x 5/16", "mm (L x E)": "38,1 x 7,94"},
    "ATÉ 700 A (360)": {"Seção Mínima (mm²)": "360 mm²", "Pol (L x E)": "3 x 3/16", "mm (L x E)": "76,2 x 4,76"},
    "ATÉ 700 A (400)": {"Seção Mínima (mm²)": "400 mm²", "Pol (L x E)": "2 x 5/16", "mm (L x E)": "50,8 x 7,94"},
}

# Notas adicionais
notas = [
    "1. A largura do barramento deve ser compatível com o terminal do cabo de maior seção.",
    "2. A seção da barra PE não deve ser inferior a 120 mm² (1\" x 3/16\")."
]

# Função para calcular a seção do barramento PE
def calcular_secao_pe(disjuntor_selecionado):
    secao_minima = int(barramento_specs[disjuntor_selecionado]["Seção Mínima (mm²)"].split()[0])
    if secao_minima > 100:
        return f"{secao_minima} mm²  Pol (L x E): {barramento_specs[disjuntor_selecionado]['Pol (L x E)']}  mm (L x E): {barramento_specs[disjuntor_selecionado]['mm (L x E)']}"
    else:
        return f"120 mm²  Pol (L x E): 1 x 3/16  mm (L x E): 25,4 x 4,76"

# Função para gerar o PDF
def gerar_pdf(especificacoes, disjuntor_selecionado):
    data_criacao = datetime.now().strftime("%Y-%m-%d")
    c = canvas.Canvas(f"Dimensionamento_Barramento_Geral_{data_criacao}.pdf")

    # Título do PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 800, "Dimensionamento Barramento Geral")

    # Data de criação
    c.setFont("Helvetica", 12)
    c.drawCentredString(300, 780, f"Data de Criação: {data_criacao}")

    # Informações do disjuntor
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 740, f"Disjuntor Selecionado: {disjuntor_selecionado}")

    # Informações do barramento
    c.setFont("Helvetica", 12)
    y_position = 720
    for key, value in especificacoes.items():
        c.drawString(100, y_position, f"{key}: {value}")
        y_position -= 20

    # Seção do barramento PE
    secao_pe = calcular_secao_pe(disjuntor_selecionado)
    c.drawString(100, y_position, f"Seção do Barramento PE: {secao_pe}")
    y_position -= 20

    # Adicionar notas ao PDF
    y_position -= 20  # Espaçamento extra antes das notas
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "Notas:")

    y_position -= 20
    c.setFont("Helvetica", 12)
    for nota in notas:
        c.drawString(100, y_position, nota)
        y_position -= 20

    # Salvar PDF
    c.save()

# Função para exibir as especificações na tela
def exibir_especificacoes():
    disjuntor_selecionado = combo.get()
    especificacoes = barramento_specs[disjuntor_selecionado]

    # Limpar o texto anterior
    text_widget.delete("1.0", tk.END)

    # Exibir as especificações na tela
    for key, value in especificacoes.items():
        text_widget.insert(tk.END, f"{key}: {value}\n")

    # Seção do barramento PE
    secao_pe = calcular_secao_pe(disjuntor_selecionado)
    text_widget.insert(tk.END, f"Seção do Barramento PE: {secao_pe}\n")

    # Adicionar notas na tela
    text_widget.insert(tk.END, "\nNotas:\n")
    for nota in notas:
        text_widget.insert(tk.END, f"{nota}\n")

    # Gerar PDF
    gerar_pdf(especificacoes, disjuntor_selecionado)

# Interface gráfica usando Tkinter
root = tk.Tk()
root.title("Seleção de Disjuntor")

# Lista de disjuntores
disjuntores = list(barramento_specs.keys())

# ComboBox para seleção do disjuntor
combo = ttk.Combobox(root, values=disjuntores)
combo.set("Selecione o Disjuntor")
combo.pack(pady=20)

# Botão para exibir especificações
button = tk.Button(root, text="Exibir Especificações", command=exibir_especificacoes)
button.pack(pady=10)

# Text widget para mostrar as especificações
text_widget = tk.Text(root, height=15, width=60)
text_widget.pack(pady=20)

# Iniciar a interface gráfica
root.mainloop()
