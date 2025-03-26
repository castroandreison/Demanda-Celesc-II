import streamlit as st
import pandas as pd
import math
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# Lista para armazenar os eletrodutos
tubos = []

# Função para calcular a área do tubo
def calcular_area(diametro, quantidade):
    raio = diametro / 2  # Raio em mm
    area_mm2 = math.pi * (raio ** 2)  # Área do círculo em mm²
    area_m2 = area_mm2 * 1e-6  # Convertendo para m²
    return area_m2 * quantidade, area_mm2 * quantidade

# Função para calcular as dimensões do shaft
def calcular_shaft():
    if not tubos:
        return None, None, None, None
    
    area_total_m2 = sum(calcular_area(d, q)[0] for d, q in tubos)
    area_total_cm2 = sum(calcular_area(d, q)[1] for d, q in tubos)
    acrescimo = float(st.session_state.acrescimo.strip('%')) / 100
    shaft_final_m2 = area_total_m2 * (1 + acrescimo)
    shaft_final_cm2 = area_total_cm2 * (1 + acrescimo)

    largura, comprimento = recomendar_shaft(shaft_final_cm2)
    return shaft_final_m2, shaft_final_cm2, largura, comprimento

# Função para recomendar um shaft retangular
def recomendar_shaft(area_necessaria_cm2):
    largura = (area_necessaria_cm2 / 1.5) ** 0.5
    comprimento = largura * 1.5
    return largura, comprimento

# Função para gerar PDF
def gerar_pdf():
    shaft_final_m2, shaft_final_cm2, largura, comprimento = calcular_shaft()
    if shaft_final_m2 is None:
        st.error("Nenhum tubo adicionado para gerar o PDF.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Memorial_Calculo_Shaft_{timestamp}.pdf"
    
    c = canvas.Canvas(filename, pagesize=A4)
    c.drawString(100, 800, "Memorial de Cálculo do Shaft")
    c.drawString(100, 780, "----------------------------------------------")
    
    y = 750
    for diametro, quantidade in tubos:
        area_m2, area_cm2 = calcular_area(diametro, quantidade)
        c.drawString(100, y, f"{quantidade} tubo(s) de {diametro} mm")
        c.drawString(120, y - 20, f"Área total: {area_m2:.2f} m² ({area_cm2:.2f} cm²)")
        y -= 50
    
    c.drawString(100, y, f"Área total dos tubos: {shaft_final_m2:.2f} m² ({shaft_final_cm2:.2f} cm²)")
    c.drawString(100, y - 20, f"Acréscimo aplicado: {st.session_state.acrescimo}")
    c.drawString(100, y - 40, f"Dimensão recomendada: {largura:.2f} cm x {comprimento:.2f} cm")
    c.save()
    
    with open(filename, "rb") as f:
        st.download_button("Baixar PDF", f, file_name=filename)

# Interface do Streamlit
st.title("Calculadora de Shaft")

diametro = st.selectbox("Diâmetro do tubo (mm):", [25, 32, 40, 50, 75, 100, 150, 200])
quantidade = st.number_input("Quantidade:", min_value=1, step=1, value=1)
if "acrescimo" not in st.session_state:
    st.session_state.acrescimo = "10%"

if st.button("Adicionar Tubo"):
    tubos.append((diametro, quantidade))
    st.experimental_rerun()

if tubos:
    df = pd.DataFrame(tubos, columns=["Diâmetro (mm)", "Quantidade"])
    st.dataframe(df, use_container_width=True)

    shaft_final_m2, shaft_final_cm2, largura, comprimento = calcular_shaft()
    if shaft_final_m2:
        st.subheader("Resultados")
        st.write(f"Área total: **{shaft_final_m2:.2f} m²** (**{shaft_final_cm2:.2f} cm²**) com acréscimo")
        st.write(f"Dimensão recomendada: **{largura:.2f} cm x {comprimento:.2f} cm**")

    if st.button("Gerar PDF"):
        gerar_pdf()
