import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

class DemandaIluminacaoTomadasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Demanda de Iluminação e Tomadas")
        
        # Potência em Iluminação
        ttk.Label(root, text="Potência em Iluminação (kW):").grid(row=0, column=0, padx=10, pady=5)
        self.potencia_iluminacao = tk.DoubleVar()
        ttk.Entry(root, textvariable=self.potencia_iluminacao).grid(row=0, column=1, padx=10, pady=5)

        # Potência em Tomadas
        ttk.Label(root, text="Potência em Tomadas (kW):").grid(row=1, column=0, padx=10, pady=5)
        self.potencia_tomadas = tk.DoubleVar()
        ttk.Entry(root, textvariable=self.potencia_tomadas).grid(row=1, column=1, padx=10, pady=5)

        # Botão de Calcular
        ttk.Button(root, text="Calcular Demanda", command=self.calcular_demanda).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Resultado
        self.resultado = tk.Text(root, height=10, width=50)
        self.resultado.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def calcular_demanda(self):
        try:
            potencia_iluminacao = self.potencia_iluminacao.get()
            potencia_tomadas = self.potencia_tomadas.get()

            # Cálculo da Demanda de Iluminação
            if potencia_iluminacao <= 10:
                demanda_iluminacao = potencia_iluminacao
                detalhe_iluminacao = f"Demanda de Iluminação: {potencia_iluminacao:.2f} kW (Potência <= 10 kW)"
            else:
                demanda_iluminacao = 10 + (potencia_iluminacao - 10) * 0.25
                detalhe_iluminacao = (f"Demanda de Iluminação: 10 kW + "
                                      f"({potencia_iluminacao:.2f} kW - 10 kW) * 0.25 = {demanda_iluminacao:.2f} kW")

            # Considerar o fator de potência de 0,9
            demanda_iluminacao /= 0.9

            # Cálculo da Demanda de Tomadas
            demanda_tomadas_sem_fp = potencia_tomadas * 0.25
            demanda_tomadas = demanda_tomadas_sem_fp / 0.9
            detalhe_tomadas = (f"Demanda de Tomadas: {potencia_tomadas:.2f} kW * 0.25 / 0.9 = {demanda_tomadas:.2f} kVA")

            # Total da Demanda
            demanda_total = demanda_iluminacao + demanda_tomadas

            # Exibir Resultados formatados
            resultado_formatado = (
                f"Potência em Iluminação: {potencia_iluminacao:.2f} kW\n"
                f"Fator utilizado: 0.9\n"
                f"{detalhe_iluminacao}\n"
                f"Potência em Tomadas: {potencia_tomadas:.2f} kW\n"
                f"{detalhe_tomadas}\n"
                f"Demanda Total: {demanda_total:.2f} kVA\n"
            )
            self.resultado.delete(1.0, tk.END)
            self.resultado.insert(tk.END, resultado_formatado)

            # Gerar memorial de cálculo em PDF
            detalhes_calculo = [
                f"Potência em Iluminação: {potencia_iluminacao:.2f} kW",
                detalhe_iluminacao,
                f"Potência em Tomadas: {potencia_tomadas:.2f} kW",
                detalhe_tomadas,
                f"Demanda de Iluminação (considerando fator de potência 0,9): {demanda_iluminacao:.2f} kVA",
                f"Demanda de Tomadas (considerando fator de potência 0,9): {demanda_tomadas:.2f} kVA",
                f"Demanda Total: {demanda_total:.2f} kVA"
            ]
            self.gerar_memorial_calculo(demanda_total, detalhes_calculo)

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    def gerar_memorial_calculo(self, total_demanda, detalhes_calculo):
        data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"memorial_calculo_{data_atual}.pdf"
        
        c = canvas.Canvas(nome_arquivo, pagesize=letter)
        width, height = letter  # obter as dimensões da página

        # Definir margens
        margem_esquerda = 72
        margem_superior = height - 72
        margem_inferior = 72
        deslocamento_linha_separacao = 5  # Novo deslocamento para a linha de separação
        linha_separacao = margem_superior - 60 - deslocamento_linha_separacao  # Ajustado com base no deslocamento

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margem_esquerda, margem_superior, "Memorial de Cálculo de Demanda de Apartamentos")
        
        c.setFont("Helvetica", 12)
        c.drawString(margem_esquerda, margem_superior - 20, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        c.drawString(margem_esquerda, margem_superior - 40, f"Demanda Total: {total_demanda:.2f} kVA")
        
        # Linha de separação
        c.line(margem_esquerda, linha_separacao, width - margem_esquerda, linha_separacao)
        
        # Detalhes do cálculo
        y_position = linha_separacao - 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margem_esquerda, y_position, "Detalhes do Cálculo:")
        
        c.setFont("Helvetica", 10)
        y_position -= 20
        
        # Adicionar detalhes do cálculo
        for linha in detalhes_calculo:
            if y_position < margem_inferior:
                c.showPage()  # Adicionar uma nova página se necessário
                c.setFont("Helvetica", 10)
                y_position = height - margem_superior + 20  # Redefinir posição Y para a nova página
                c.drawString(margem_esquerda, y_position, "Detalhes do Cálculo:")
                y_position -= 20
            c.drawString(margem_esquerda, y_position, linha)
            y_position -= 15
        
        c.save()
        messagebox.showinfo("Sucesso", f"Memorial de cálculo salvo como {nome_arquivo}")

# Código para inicializar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = DemandaIluminacaoTomadasApp(root)
    root.mainloop()
