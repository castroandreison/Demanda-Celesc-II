import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

tubos = []

def calcular_area(diametro, quantidade):
    """Calcula a área ocupada pelos tubos."""
    raio = diametro / 2  # Raio em mm
    area_mm2 = 3.1416 * (raio ** 2)  # Área do círculo em mm²
    area_cm2 = area_mm2 * 1e-2  # Convertendo para cm²
    return area_cm2 * quantidade, area_mm2 * quantidade

def adicionar_tubo():
    try:
        diametro = float(combo_diametro.get())
        quantidade = int(entry_quantidade.get())
        if diametro <= 0 or quantidade <= 0:
            raise ValueError("Valores inválidos")
        tubos.append((diametro, quantidade))
        atualizar_lista()
    except ValueError:
        messagebox.showerror("Erro", "Insira valores válidos.")

def atualizar_lista():
    """Atualiza a lista de tubos na interface."""
    listbox_tubos.delete(0, tk.END)
    for diametro, quantidade in tubos:
        listbox_tubos.insert(tk.END, f"{quantidade} tubo(s) de {diametro} mm")

def calcular_shaft():
    """Calcula o shaft com acréscimo e recomenda dimensões retangulares."""
    if not tubos:
        messagebox.showerror("Erro", "Nenhum tubo adicionado.")
        return
    
    area_total_cm2 = sum(calcular_area(d, q)[0] for d, q in tubos)
    acrescimo = float(combo_acrescimo.get().strip('%')) / 100
    shaft_final_cm2 = area_total_cm2 * (1 + acrescimo)

    largura, comprimento = recomendar_shaft(shaft_final_cm2)

    label_resultado.config(text=f"Tamanho do shaft: {shaft_final_cm2:.2f} cm²")
    label_recomendacao.config(text=f"Dimensão recomendada: {largura:.2f} cm x {comprimento:.2f} cm")

    return shaft_final_cm2, largura, comprimento

def recomendar_shaft(area_necessaria_cm2):
    """Calcula a dimensão retangular exata baseada na área total."""
    largura = (area_necessaria_cm2 / 1.5) ** 0.5
    comprimento = largura * 1.5
    return largura, comprimento

def gerar_pdf():
    """Gera um PDF com os cálculos e recomendações."""
    if not tubos:
        messagebox.showerror("Erro", "Nenhum tubo adicionado para gerar o PDF.")
        return
    
    shaft_final_cm2, largura, comprimento = calcular_shaft()
    if shaft_final_cm2 is None:
        return
    
    # Abre a caixa de diálogo "Salvar Como"
    filename = asksaveasfilename(defaultextension=".pdf",
                                   filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                                   title="Salvar como")
    if not filename:  # Se o usuário cancelar, não faz nada
        return
    
    c = canvas.Canvas(filename, pagesize=A4)
    c.drawString(100, 800, "Memorial de Cálculo do Shaft")
    c.drawString(100, 780, "----------------------------------------------")
    
    y = 750
    for diametro, quantidade in tubos:
        area_cm2, area_mm2 = calcular_area(diametro, quantidade)
        c.drawString(100, y, f"{quantidade} tubo(s) de {diametro} mm")
        c.drawString(120, y - 20, f"Área total: {area_cm2:.2f} cm² ({area_mm2:.2f} mm²)")
        y -= 50

    c.drawString(100, y, f"Área total dos tubos: {shaft_final_cm2:.2f} cm²")
    c.drawString(100, y - 20, f"Acréscimo aplicado: {combo_acrescimo.get()}")
    c.drawString(100, y - 40, f"Área total com acréscimo: {shaft_final_cm2:.2f} cm²")

    y -= 80
    c.drawString(100, y, "Dimensão retangular recomendada:")
    c.drawString(100, y - 20, f"Largura: {largura:.2f} cm")
    c.drawString(100, y - 40, f"Comprimento: {comprimento:.2f} cm")

    c.save()
    messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\nArquivo: {filename}")

# Interface gráfica
root = tk.Tk()
root.title("Calculadora de Shaft")
root.geometry("400x600")

tk.Label(root, text="Diâmetro do tubo (mm):").pack()
combo_diametro = ttk.Combobox(root, values=[25, 32, 40, 50, 75, 100, 150, 200])
combo_diametro.pack()
combo_diametro.current(0)

tk.Label(root, text="Quantidade:").pack()
entry_quantidade = tk.Entry(root)
entry_quantidade.pack()

tk.Button(root, text="Adicionar Tubo", command=adicionar_tubo).pack()

listbox_tubos = tk.Listbox(root)
listbox_tubos.pack()

tk.Label(root, text="Acréscimo de espaço:").pack()
combo_acrescimo = ttk.Combobox(root, values=["10%", "20%", "30%", "40%", "50%"])
combo_acrescimo.pack()
combo_acrescimo.current(0)

tk.Button(root, text="Calcular Shaft", command=calcular_shaft).pack()
label_resultado = tk.Label(root, text="")
label_resultado.pack()

label_recomendacao = tk.Label(root, text="", justify=tk.LEFT)
label_recomendacao.pack()

tk.Button(root, text="Gerar PDF", command=gerar_pdf).pack()

root.mainloop()
