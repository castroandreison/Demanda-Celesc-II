import streamlit as st
from fractions import Fraction
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Tabelas de Demanda em kVA
tabela_trifasico = {
    Fraction(1, 3): [0.65, 0.98, 1.24, 1.5, 1.76, 1.95, 2.15, 2.34, 2.53, 2.73],
    Fraction(1, 2): [0.87, 1.31, 1.65, 2.0, 2.35, 2.61, 2.87, 3.13, 3.39, 3.65],
    # ... (demais dados omitidos para brevidade)
}

tabela_monofasico = {
    Fraction(1, 4): [0.66, 0.99, 1.254, 1.518, 1.782, 1.98, 2.178, 2.376, 2.574, 2.772],
    Fraction(1, 3): [0.77, 1.155, 1.463, 1.771, 2.079, 2.31, 2.541, 2.772, 3.003, 3.234],
    # ... (demais dados omitidos para brevidade)
}

fatores_trifasico = {
    1: 1, 2: 0.75, 3: 0.633, 4: 0.575, 5: 0.54, 6: 0.5, 7: 0.471, 8: 0.45, 9: 0.433, 10: 0.42
}

fatores_monofasico = {
    1: 1, 2: 0.75, 3: 0.633, 4: 0.575, 5: 0.54, 6: 0.5, 7: 0.471, 8: 0.45, 9: 0.433, 10: 0.42
}

def calcular_kva(tipo, potencia, quantidade):
    if tipo == 'Trifásico':
        tabela = tabela_trifasico
        fator = fatores_trifasico.get(quantidade, None)
    else:
        tabela = tabela_monofasico
        fator = fatores_monofasico.get(quantidade, None)
    
    if potencia in tabela and fator:
        return tabela[potencia][quantidade-1], fator
    else:
        return None, None

def gerar_relatorio_pdf(motores):
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
    
    for motor in motores:
        c.drawString(30, y_position, motor['tipo'])
        c.drawString(120, y_position, str(motor['potencia']))
        c.drawString(200, y_position, str(motor['quantidade']))
        c.drawString(300, y_position, f"{motor['kva']:.2f}")
        c.drawString(380, y_position, f"{motor['fator']:.3f}")
        c.drawString(470, y_position, motor['descricao'])
        y_position -= 20
        total_kva += motor['kva']
    
    y_position -= 20
    c.drawString(30, y_position, f"Demanda Total: {total_kva:.2f} kVA")
    
    c.save()
    return pdf_path

# Interface com Streamlit
st.title("Gerenciamento de Motores")

# Seção de entrada de dados
tipo = st.selectbox("Tipo de Motor", ["Trifásico", "Monofásico"])
potencia_str = st.selectbox("Potência (kW)", [str(p) for p in (tabela_trifasico.keys() if tipo == 'Trifásico' else tabela_monofasico.keys())])
quantidade = st.number_input("Quantidade", min_value=1, max_value=10, step=1)
descricao = st.text_input("Descrição do Motor")

# Lista de motores adicionados
motores = []

# Botões de ação
if st.button("Adicionar Motor"):
    potencia = Fraction(potencia_str)
    kva, fator = calcular_kva(tipo, potencia, quantidade)
    if kva is not None:
        motores.append({
            'tipo': tipo,
            'potencia': potencia,
            'quantidade': quantidade,
            'kva': kva,
            'fator': fator,
            'descricao': descricao
        })
        st.success("Motor adicionado com sucesso!")
    else:
        st.error("Erro ao calcular a demanda em kVA. Verifique os dados inseridos.")

if st.button("Calcular Total"):
    total_kva = sum(motor['kva'] for motor in motores)
    st.info(f"Demanda total: {total_kva:.2f} kVA")

if st.button("Gerar Relatório"):
    if motores:
        pdf_path = gerar_relatorio_pdf(motores)
        st.success(f"Relatório gerado com sucesso: {pdf_path}")
        st.write("Baixar relatório:", pdf_path)
    else:
        st.warning("Nenhum motor adicionado para gerar o relatório.")

# Exibição dos motores
st.subheader("Lista de Motores Adicionados")
for motor in motores:
    st.write(f"**Tipo**: {motor['tipo']} | **Potência**: {motor['potencia']} kW | **Quantidade**: {motor['quantidade']} | **kVA**: {motor['kva']:.2f} | **Fator**: {motor['fator']:.3f} | **Descrição**: {motor['descricao']}")
