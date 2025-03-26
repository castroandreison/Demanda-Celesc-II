import streamlit as st
from datetime import datetime

# Dados iniciais
apartamentos = []

fatores_diversidade = {
    1: 1, 2: 2, 3: 3, 4: 3.88, 5: 4.84, 6: 5.8, 7: 6.76, 8: 7.72, 9: 8.68, 10: 9.64,
    11: 10.42, 12: 11.2, 13: 11.98, 14: 12.76, 15: 13.54, 16: 14.32, 17: 15.1, 18: 15.88,
    19: 16.66, 20: 17.44, 21: 18.04, 22: 18.65, 23: 19.25, 24: 19.86, 25: 20.46, 26: 21.06,
    # ... (adicione o restante dos dados aqui) ...
}

# Tabela de potência em kVA em função da área do apartamento
potencia_por_area = {
    70.0: 1.570, 71.0: 1.590, 72.0: 1.610, 73.0: 1.630, 74.0: 1.650,
    75.0: 1.670, 76.0: 1.690, 77.0: 1.710, 78.0: 1.730, 79.0: 1.750,
    80.0: 1.760, 81.0: 1.786, 82.0: 1.805, 83.0: 1.825, 84.0: 1.844,
    # ... (adicione o restante dos dados aqui) ...
}

st.title("Calculadora de Potência de Apartamentos")

# Inputs
num_apartamentos = st.number_input("Número de apartamentos:", min_value=1, value=1)
area_apartamento = st.number_input("Área do apartamento (m²):", min_value=0.0, value=70.0)
fator_diversidade = st.selectbox("Fator de diversidade:", options=list(fatores_diversidade.keys()), index=0)

if st.button("Adicionar apartamento"):
    potencia = potencia_por_area.get(area_apartamento, 0)
    fator = fatores_diversidade.get(fator_diversidade, 1)
    total_potencia = potencia * num_apartamentos * fator
    apartamentos.append({
        'Área': area_apartamento,
        'Potência': potencia,
        'Fator de Diversidade': fator,
        'Potência Total': total_potencia
    })
    st.success("Apartamento adicionado com sucesso!")

if st.button("Gerar Relatório"):
    if not apartamentos:
        st.warning("Nenhum apartamento adicionado.")
    else:
        st.write("Relatório de Apartamentos")
        for ap in apartamentos:
            st.write(f"Área: {ap['Área']} m², Potência: {ap['Potência']} kVA, Fator de Diversidade: {ap['Fator de Diversidade']}, Potência Total: {ap['Potência Total']} kVA")
        st.write(f"Total de potência calculada: {sum(ap['Potência Total'] for ap in apartamentos)} kVA")

# Salvar PDF (Simulação - Em Streamlit, o suporte direto para PDFs pode ser limitado)
if st.button("Salvar Relatório em PDF"):
    st.warning("A funcionalidade de salvar em PDF não está implementada no Streamlit.")
    # Implementar geração de PDF usando alguma biblioteca externa, se necessário.
