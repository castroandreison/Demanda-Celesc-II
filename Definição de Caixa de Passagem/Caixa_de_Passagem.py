import tkinter as tk
from tkinter import messagebox, scrolledtext
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# Função para determinar o tipo de caixa de passagem e o número de caixas necessárias
def determinar_caixa():
    try:
        secao = float(entry_secao.get())
        mais_de_um_cabo = var_mais_de_um_cabo.get()
        distancia_pq = float(entry_distancia_pq.get())
        mudanca_direcao = int(entry_mudanca_direcao.get())

        if secao <= 70 and not mais_de_um_cabo:
            tipo = "A1"
            dimensoes = "650 x 410 x 850 mm"
        else:
            tipo = "B1"
            dimensoes = "850 x 650 x 850 mm"

        # Definindo o número de caixas de passagem
        caixas_necessarias = 2
        if distancia_pq > 30:
            caixas_necessarias += 1

        caixas_necessarias += mudanca_direcao

        # Exibindo os resultados na tela
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, f"Tipo de Caixa: {tipo}\n")
        resultado_text.insert(tk.END, f"Dimensões da Caixa: {dimensoes}\n")
        resultado_text.insert(tk.END, f"Distância do Poste ao Quadro: {distancia_pq} m\n")
        resultado_text.insert(tk.END, f"Mudanças de Direção: {mudanca_direcao}\n")
        resultado_text.insert(tk.END, f"Número Total de Caixas Necessárias: {caixas_necessarias}\n")

        gerar_relatorio(tipo, dimensoes, distancia_pq, mudanca_direcao, caixas_necessarias)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para gerar o relatório em PDF
def gerar_relatorio(tipo, dimensoes, distancia_pq, mudanca_direcao, caixas_necessarias):
    # Obtendo a data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"Caixa de Passagem - {data_atual}.pdf"

    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica", 12)
    c.drawString(100, altura - 100, "Relatório de Escolha da Caixa de Passagem")
    c.drawString(100, altura - 130, f"Tipo de Caixa: {tipo}")
    c.drawString(100, altura - 150, f"Dimensões da Caixa: {dimensoes}")
    c.drawString(100, altura - 170, "Especificações atendidas conforme normas da Celesc D:")
    c.drawString(100, altura - 190, "- Caixa pré-fabricada de fabricante certificado e homologado.")
    c.drawString(100, altura - 210, "- Tampa de ferro fundido nodular conforme Especificação 01.")
    c.drawString(100, altura - 230, "- Instalada com afastamento de 50 cm a 150 cm do poste.")
    c.drawString(100, altura - 250, "- Instalada com afastamento de 50 cm a 70 cm do quadro de medição.")
    c.drawString(100, altura - 270, f"- Distância do poste ao quadro de medição: {distancia_pq} m.")
    c.drawString(100, altura - 290, f"- Mudança de direção: {mudanca_direcao}")
    c.drawString(100, altura - 310, f"- Número total de caixas de passagem: {caixas_necessarias}")
    c.drawString(100, altura - 330, "- A caixa deve ser fabricada em concreto armado ou construída com blocos de concreto")
    c.drawString(100, altura - 350, "  estrutural preenchidos com argamassa ou tijolo maciço, com resistência mecânica")
    c.drawString(100, altura - 370, "  adequada ao local em que for aplicada, em conformidade com a classe do tampão.")
    c.drawString(100, altura - 390, "- A caixa pré-fabricada deve ser de fabricante certificado e modelo homologado pela")
    c.drawString(100, altura - 410, "  Celesc D, identificada próximo à borda superior da parte interna com modelo e nome")
    c.drawString(100, altura - 430, "  ou logomarca do fabricante.")
    c.drawString(100, altura - 450, "- Nota: A cada mudança de direção deve possuir uma caixa de passagem, ou seja, uma")
    c.drawString(100, altura - 470, "  abaixo do poste e uma junto ao quadro de medição e uma a cada mudança de direção.")
    
    # Adicionando notas especificadas pelo usuário
    c.drawString(100, altura - 490, "Notas Adicionais:")
    c.drawString(100, altura - 510, "a) CLASSE MÍNIMA D 400 (400 kN) - PARA APLICAÇÃO EM VIAS DE CIRCULAÇÃO")
    c.drawString(100, altura - 530, "   DE VEÍCULOS, RUAS, ACOSTAMENTOS E ESTACIONAMENTOS PARA TODOS")
    c.drawString(100, altura - 550, "   OS TIPOS DE VEÍCULOS. VER FIGURA ACIMA.")
    c.drawString(100, altura - 570, "b) CLASSE MÍNIMA B 125 (125 kN) - PARA APLICAÇÃO EM PASSEIOS (CALÇADAS),")
    c.drawString(100, altura - 590, "   LOCAIS DE CIRCULAÇÃO DE PEDESTRES E ÁREAS DE ESTACIONAMENTO DE")
    c.drawString(100, altura - 610, "   CARROS DE PASSEIO. VER FIGURA ACIMA.")
    
    # Adicionando nova nota especificada
    c.drawString(100, altura - 630, "No tampão da caixa de passagem deve ser gravado de forma legível e indelével em")
    c.drawString(100, altura - 650, "alto-relevo as seguintes identificações:")
    c.drawString(100, altura - 670, "- Na face superior: raio típico de eletricidade, as inscrições “CUIDADO ELETRICIDADE”,")
    c.drawString(100, altura - 690, "  “ENERGIA”, “NBR 10160”, “NODULAR”, a classe “B125” ou “D400” e a carga de controle")
    c.drawString(100, altura - 710, "  “125kN” ou “400kN”;")
    c.drawString(100, altura - 730, "- Na face inferior: logomarca e/ou nome do fabricante, mês/ano de fabricação e lote;")
    c.drawString(100, altura - 750, "- No aro, em local visível após instalação: “NBR 10160” e classe “B125” ou “D400”;")
    c.drawString(100, altura - 770, "Notas:")
    c.drawString(100, altura - 790, "1. Caixa em concreto armado, blocos de concreto estrutural preenchido com argamassa ou tijolo maciço;")
    c.drawString(100, altura - 810, "2. A caixa pré-fabricada deve ser de fabricante certificado e modelo homologado pela Celesc D;")
    c.drawString(100, altura - 830, "3. A classe do concreto deve ser maior ou igual a C25 ou maior ou igual C30 em regiões marítimas ou")
    c.drawString(100, altura - 850, "   industriais (ABNT NBR 6118);")
    c.drawString(100, altura - 870, "4. Espessura mínima da parede de 100 mm para concreto armado, 120 mm para blocos de concreto")
    c.drawString(100, altura - 890, "   estrutural preenchido com argamassa ou 150 mm para tijolo maciço;")
    c.drawString(100, altura - 910, "5. A caixa deve ser rebocada internamente;")
    c.drawString(100, altura - 930, "6. O fundo da caixa deve ser preenchido com 150 mm de brita No 2;")

    c.save()

    messagebox.showinfo("Sucesso", f"Relatório '{nome_arquivo}' gerado com sucesso!")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Escolha da Caixa de Passagem")

tk.Label(root, text="Seção Transversal do Condutor (mm²):").grid(row=0, column=0, padx=10, pady=5)
entry_secao = tk.Entry(root)
entry_secao.grid(row=0, column=1, padx=10, pady=5)

var_mais_de_um_cabo = tk.IntVar()
tk.Checkbutton(root, text="Mais de um cabo por fase", variable=var_mais_de_um_cabo).grid(row=1, columnspan=2, pady=5)

tk.Label(root, text="Distância do Poste ao Quadro (m):").grid(row=2, column=0, padx=10, pady=5)
entry_distancia_pq = tk.Entry(root)
entry_distancia_pq.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Número de Mudanças de Direção:").grid(row=3, column=0, padx=10, pady=5)
entry_mudanca_direcao = tk.Entry(root)
entry_mudanca_direcao.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Calcular", command=determinar_caixa).grid(row=4, columnspan=2, pady=20)

# Área de texto para exibir os resultados
resultado_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
resultado_text.grid(row=5, columnspan=2, padx=10, pady=10)

root.mainloop()
