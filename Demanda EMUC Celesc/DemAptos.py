import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# Dados iniciais
apartamentos = []


fatores_diversidade = {
    1: 1, 2: 2, 3: 3, 4: 3.88, 5: 4.84, 6: 5.8, 7: 6.76, 8: 7.72, 9: 8.68, 10: 9.64,
    11: 10.42, 12: 11.2, 13: 11.98, 14: 12.76, 15: 13.54, 16: 14.32, 17: 15.1, 18: 15.88,
    19: 16.66, 20: 17.44, 21: 18.04, 22: 18.65, 23: 19.25, 24: 19.86, 25: 20.46, 26: 21.06,
    27: 21.67, 28: 22.27, 29: 22.88, 30: 23.48, 31: 24.08, 32: 24.69, 33: 25.29, 34: 25.9,
    35: 26.5, 36: 27.1, 37: 27.71, 38: 28.31, 39: 28.92, 40: 29.52, 41: 30.12, 42: 30.73,
    43: 31.33, 44: 31.94, 45: 32.54, 46: 33.1, 47: 33.66, 48: 34.22, 49: 34.78, 50: 35.34,
    51: 35.9, 52: 36.46, 53: 37.02, 54: 37.58, 55: 38.14, 56: 38.7, 57: 39.26, 58: 39.82,
    59: 40.38, 60: 40.94, 61: 41.5, 62: 42.05, 63: 42.62, 64: 43.18, 65: 43.74, 66: 44.3,
    67: 44.86, 68: 45.42, 69: 45.98, 70: 46.54, 71: 47.1, 72: 47.66, 73: 48.22, 74: 48.78,
    75: 49.34, 76: 49.9, 77: 50.46, 78: 51.02, 79: 51.58, 80: 52.14, 81: 52.7, 82: 53.26,
    83: 53.82, 84: 54.38, 85: 54.9, 86: 55.5, 87: 56.06, 88: 56.62, 89: 57.18, 90: 57.74,
    91: 58.3, 92: 58.86, 93: 59.42, 94: 59.98, 95: 60.54, 96: 61.1, 97: 61.66, 98: 62.22,
    99: 62.78, 100: 63.34, 101: 63.59, 102: 63.84, 103: 64.09, 104: 64.34, 105: 64.59,
    106: 64.84, 107: 65.09, 108: 65.34, 109: 65.59, 110: 65.84, 111: 66.09, 112: 66.34,
    113: 66.59, 114: 66.84, 115: 67.09, 116: 67.34, 117: 67.59, 118: 67.84, 119: 68.09,
    120: 68.34, 121: 68.59, 122: 68.84, 123: 69.09, 124: 69.34, 125: 69.59, 126: 69.79,
    127: 69.99, 128: 70.19, 129: 70.39, 130: 70.59, 131: 70.79, 132: 70.99, 133: 71.19,
    134: 71.39, 135: 71.59, 136: 71.79, 137: 71.99, 138: 72.19, 139: 72.39, 140: 72.59,
    141: 72.79, 142: 72.99, 143: 73.19, 144: 73.39, 145: 73.59, 146: 73.79, 147: 73.99,
    148: 74.19, 149: 74.39, 150: 74.59, 151: 74.74, 152: 74.89, 153: 75.04, 154: 75.19,
    155: 75.34, 156: 75.49, 157: 75.64, 158: 75.79, 159: 75.94, 160: 76.09, 161: 76.24,
    162: 76.39, 163: 76.54, 164: 76.69, 165: 76.84, 166: 76.99, 167: 77.14, 168: 77.29,
    169: 77.44, 170: 77.59, 171: 77.74, 172: 77.89, 173: 78.04, 174: 78.19, 175: 78.34,
    176: 78.44, 177: 78.54, 178: 78.64, 179: 78.74, 180: 78.84, 181: 78.94, 182: 79.04,
    183: 79.14, 184: 79.24, 185: 79.34, 186: 79.44, 187: 79.54, 188: 79.64, 189: 79.74,
    190: 79.84, 191: 79.94, 192: 80.04, 193: 80.14, 194: 80.24, 195: 80.34, 196: 80.44,
    197: 80.54, 198: 80.64, 199: 80.74, 200: 80.84, 201: 80.89, 202: 80.94, 203: 80.89,
    204: 81.04, 205: 81.09, 206: 81.14, 207: 81.19, 208: 81.24, 209: 81.29, 210: 81.34,
    211: 81.39, 212: 81.44, 213: 81.49, 214: 81.54, 215: 81.59, 216: 81.64, 217: 81.69,
    218: 81.74, 219: 81.79, 220: 81.84, 221: 81.89, 222: 81.94, 223: 81.99, 224: 82.04,
    225: 82.09, 226: 82.12, 227: 82.14, 228: 82.17, 229: 82.19, 230: 82.22, 231: 82.24,
    232: 82.27, 233: 82.29, 234: 82.32, 235: 82.34, 236: 82.37, 237: 82.39, 238: 82.42,
    239: 82.44, 240: 82.47, 241: 82.49, 242: 82.52, 243: 82.54, 244: 82.57, 245: 82.59,
    246: 82.62, 247: 82.64, 248: 82.67, 249: 82.69, 250: 82.72, 251: 82.73, 252: 82.74,
    253: 82.75, 254: 82.76, 255: 82.77, 256: 82.78, 257: 82.79, 258: 82.8, 259: 82.81,
    260: 82.82, 261: 82.83, 262: 82.84, 263: 82.85, 264: 82.86, 265: 82.87, 266: 82.88,
    267: 82.89, 268: 82.9, 269: 82.91, 270: 82.92, 271: 82.93, 272: 82.94, 273: 82.95,
    274: 82.96, 275: 82.97, 276: 83, 277: 83, 278: 83, 279: 83, 280: 83, 281: 83, 282: 83,
    283: 83, 284: 83, 285: 83, 286: 83, 287: 83, 288: 83, 289: 83, 290: 83, 291: 83,
    292: 83, 293: 83, 294: 83, 295: 83, 296: 83, 297: 83, 298: 83, 299: 83, 300: 83
}


# Tabela de potência em kVA em função da área do apartamento
potencia_por_area = {
    70.0: 1.570, 71.0: 1.590, 72.0: 1.610, 73.0: 1.630, 74.0: 1.650,
    75.0: 1.670, 76.0: 1.690, 77.0: 1.710, 78.0: 1.730, 79.0: 1.750,
    80.0: 1.760, 81.0: 1.786, 82.0: 1.805, 83.0: 1.825, 84.0: 1.844,
    85.0: 1.864, 86.0: 1.883, 87.0: 1.903, 88.0: 1.922, 89.0: 1.942,
    90.0: 1.961, 91.0: 1.981, 92.0: 2.000, 93.0: 2.019, 94.0: 2.039,
    95.0: 2.058, 96.0: 2.078, 97.0: 2.097, 98.0: 2.117, 99.0: 2.136,
    100.0: 2.156, 101.0: 2.175, 102.0: 2.195, 103.0: 2.214, 104.0: 2.233,
    105.0: 2.253, 106.0: 2.272, 107.0: 2.292, 108.0: 2.311, 109.0: 2.331,
    110.0: 2.350, 111.0: 2.370, 112.0: 2.389, 113.0: 2.409, 114.0: 2.428,
    115.0: 2.447, 116.0: 2.467, 117.0: 2.486, 118.0: 2.506, 119.0: 2.525,
    120.0: 2.545, 121.0: 2.564, 122.0: 2.584, 123.0: 2.603, 124.0: 2.623,
    125.0: 2.642, 126.0: 2.661, 127.0: 2.681, 128.0: 2.700, 129.0: 2.720,
    130.0: 2.739, 131.0: 2.759, 132.0: 2.778, 133.0: 2.798, 134.0: 2.817,
    135.0: 2.837, 136.0: 2.856, 137.0: 2.875, 138.0: 2.895, 139.0: 2.914,
    140.0: 2.934, 141.0: 2.953, 142.0: 2.973, 143.0: 2.992, 144.0: 3.012,
    145.0: 3.031, 146.0: 3.051, 147.0: 3.070, 148.0: 3.089, 149.0: 3.109,
    150.0: 3.128, 151.0: 3.148, 152.0: 3.167, 153.0: 3.187, 154.0: 3.206,
    155.0: 3.226, 156.0: 3.245, 157.0: 3.265, 158.0: 3.284, 159.0: 3.303,
    160.0: 3.323, 161.0: 3.342, 162.0: 3.362, 163.0: 3.381, 164.0: 3.401,
    165.0: 3.420, 166.0: 3.440, 167.0: 3.459, 168.0: 3.479, 169.0: 3.498,
    170.0: 3.517, 171.0: 3.537, 172.0: 3.556, 173.0: 3.576, 174.0: 3.595,
    175.0: 3.615, 176.0: 3.634, 177.0: 3.654, 178.0: 3.673, 179.0: 3.693,
    180.0: 3.712, 181.0: 3.731, 182.0: 3.751, 183.0: 3.770, 184.0: 3.790,
    185.0: 3.809, 186.0: 3.829, 187.0: 3.848, 188.0: 3.868, 189.0: 3.887,
    190.0: 3.907, 191.0: 3.926, 192.0: 3.945, 193.0: 3.965, 194.0: 3.984,
    195.0: 4.004, 196.0: 4.023, 197.0: 4.043, 198.0: 4.062, 199.0: 4.082,
    200.0: 4.101, 201.0: 4.121, 202.0: 4.140, 203.0: 4.159, 204.0: 4.179,
    205.0: 4.198, 206.0: 4.218, 207.0: 4.237, 208.0: 4.257, 209.0: 4.276,
    210.0: 4.296, 211.0: 4.315, 212.0: 4.335, 213.0: 4.354, 214.0: 4.373,
    215.0: 4.393, 216.0: 4.412, 217.0: 4.432, 218.0: 4.451, 219.0: 4.471,
    220.0: 4.490, 221.0: 4.510, 222.0: 4.529, 223.0: 4.549, 224.0: 4.568,
    225.0: 4.587, 226.0: 4.607, 227.0: 4.626, 228.0: 4.646, 229.0: 4.665,
    230.0: 4.685, 231.0: 4.704, 232.0: 4.724, 233.0: 4.743, 234.0: 4.763,
    235.0: 4.782, 236.0: 4.801, 237.0: 4.821, 238.0: 4.840, 239.0: 4.860,
    240.0: 4.879, 241.0: 4.899, 242.0: 4.918, 243.0: 4.938, 244.0: 4.957,
    245.0: 4.977, 246.0: 4.996, 247.0: 5.015, 248.0: 5.035, 249.0: 5.054,
    250.0: 5.074, 251.0: 5.093, 252.0: 5.113, 253.0: 5.132, 254.0: 5.152,
    255.0: 5.171, 256.0: 5.191, 257.0: 5.210, 258.0: 5.229, 259.0: 5.249,
    260.0: 5.268, 261.0: 5.288, 262.0: 5.307, 263.0: 5.327, 264.0: 5.346,
    265.0: 5.366, 266.0: 5.385, 267.0: 5.405, 268.0: 5.424, 269.0: 5.443,
    270.0: 5.463, 271.0: 5.482, 272.0: 5.502, 273.0: 5.521, 274.0: 5.541,
    275.0: 5.560, 276.0: 5.580, 277.0: 5.599, 278.0: 5.619, 279.0: 5.638,
    280.0: 5.657, 281.0: 5.677, 282.0: 5.696, 283.0: 5.716, 284.0: 5.735,
    285.0: 5.755, 286.0: 5.774, 287.0: 5.794, 288.0: 5.813, 289.0: 5.833,
    290.0: 5.852, 291.0: 5.871, 292.0: 5.891, 293.0: 5.910, 294.0: 5.930,
    295.0: 5.949, 296.0: 5.969, 297.0: 5.988, 298.0: 6.008, 299.0: 6.027,
    300.0: 6.047, 301.0: 6.066, 302.0: 6.085, 303.0: 6.105, 304.0: 6.124,
    305.0: 6.144, 306.0: 6.163, 307.0: 6.183, 308.0: 6.202, 309.0: 6.222,
    310.0: 6.241, 311.0: 6.261, 312.0: 6.280, 313.0: 6.299, 314.0: 6.319,
    315.0: 6.338, 316.0: 6.358, 317.0: 6.377, 318.0: 6.397, 319.0: 6.416,
    320.0: 6.436, 321.0: 6.455, 322.0: 6.475, 323.0: 6.494, 324.0: 6.513,
    325.0: 6.533, 326.0: 6.552, 327.0: 6.572, 328.0: 6.591, 329.0: 6.611,
    330.0: 6.630, 331.0: 6.650, 332.0: 6.669, 333.0: 6.689, 334.0: 6.708,
    335.0: 6.727, 336.0: 6.747, 337.0: 6.766, 338.0: 6.786, 339.0: 6.805,
    340.0: 6.825, 341.0: 6.844, 342.0: 6.864, 343.0: 6.883, 344.0: 6.903,
    345.0: 6.922, 346.0: 6.941, 347.0: 6.961, 348.0: 6.980, 349.0: 7.000,
    350.0: 7.019, 351.0: 7.039, 352.0: 7.058, 353.0: 7.078, 354.0: 7.097,
    355.0: 7.117, 356.0: 7.136, 357.0: 7.155, 358.0: 7.175, 359.0: 7.194,
    360.0: 7.214, 361.0: 7.233, 362.0: 7.253, 363.0: 7.272, 364.0: 7.292,
    365.0: 7.311, 366.0: 7.331, 367.0: 7.350, 368.0: 7.369, 369.0: 7.389,
    370.0: 7.408, 371.0: 7.428, 372.0: 7.447, 373.0: 7.467, 374.0: 7.487,
    375.0: 7.507, 376.0: 7.527, 377.0: 7.547, 378.0: 7.567, 379.0: 7.587,
    380.0: 7.607, 381.0: 7.627, 382.0: 7.647, 383.0: 7.667, 384.0: 7.687,
    385.0: 7.707, 386.0: 7.727, 387.0: 7.747, 388.0: 7.767, 389.0: 7.787,
    390.0: 7.807, 391.0: 7.827, 392.0: 7.847, 393.0: 7.867, 394.0: 7.887,
    395.0: 7.907, 396.0: 7.927, 397.0: 7.947, 398.0: 7.967, 399.0: 7.987,
    400.0: 8.007
}
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# Dados iniciais
apartamentos = []


# Obter as opções para os comboboxes a partir das tabelas
quantidades = sorted(fatores_diversidade.keys())
areas = sorted(potencia_por_area.keys())

# Funções para manipulação de dados
def adicionar_apartamento():
    descricao = entry_descricao.get()
    quantidade = combobox_quantidade.get()
    area = combobox_area.get()

    if not descricao or not quantidade or not area:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return

    try:
        quantidade = int(quantidade)
        area = float(area)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e Área deve ser um número decimal")
        return

    apartamentos.append({
        "descricao": descricao,
        "quantidade": quantidade,
        "area": area
    })
    atualizar_lista()

def editar_apartamento():
    selected_item = lista_apartamentos.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um apartamento para editar")
        return
    
    item_id = selected_item[0]
    descricao = entry_descricao.get()
    quantidade = combobox_quantidade.get()
    area = combobox_area.get()

    if not descricao or not quantidade or not area:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")
        return

    try:
        quantidade = int(quantidade)
        area = float(area)
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e Área deve ser um número decimal")
        return

    # Encontra o índice do item para atualizar
    index = lista_apartamentos.index(item_id)
    apartamentos[index] = {
        "descricao": descricao,
        "quantidade": quantidade,
        "area": area
    }
    atualizar_lista()

def remover_apartamento():
    selected_item = lista_apartamentos.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um apartamento para remover")
        return

    item_id = selected_item[0]
    # Encontra o índice do item para remover
    index = lista_apartamentos.index(item_id)
    del apartamentos[index]
    atualizar_lista()

def selecionar_apartamento(event):
    selected_item = lista_apartamentos.selection()
    if selected_item:
        item_id = selected_item[0]
        apartamento = apartamentos[lista_apartamentos.index(item_id)]
        entry_descricao.delete(0, tk.END)
        entry_descricao.insert(0, apartamento["descricao"])
        combobox_quantidade.set(apartamento["quantidade"])
        combobox_area.set(apartamento["area"])

def atualizar_lista():
    lista_apartamentos.delete(*lista_apartamentos.get_children())
    for i, apto in enumerate(apartamentos):
        lista_apartamentos.insert("", "end", iid=str(i), values=(apto["descricao"], apto["quantidade"], apto["area"]))
    atualizar_fatores()

def atualizar_fatores():
    quantidade = combobox_quantidade.get()
    area = combobox_area.get()
    
    fator_diversidade = fatores_diversidade.get(int(quantidade), "Não encontrado") if quantidade else "Não encontrado"
    fator_potencia = potencia_por_area.get(float(area), "Não encontrado") if area else "Não encontrado"
    
    fator_diversidade_label.config(text=f"Fator de Diversidade: {fator_diversidade}")
    fator_potencia_label.config(text=f"Potência por Área: {fator_potencia} kVA")

def calcular_demanda():
    if not apartamentos:
        messagebox.showerror("Erro", "Não há apartamentos cadastrados para calcular a demanda")
        return
    
    total_demanda = 0
    detalhes_demanda = []
    detalhes_calculo = []

    global potencia_por_area, fatores_diversidade
    
    for apartamento in apartamentos:
        area = apartamento["area"]
        quantidade = apartamento["quantidade"]
        descricao = apartamento["descricao"]

        # Encontrar a potência correspondente à área
        potencia = potencia_por_area.get(area)
        if potencia is None:
            messagebox.showerror("Erro", f"Área {area} não encontrada na tabela de potência")
            return
        
        # Encontrar o fator de diversidade para a quantidade
        fator_diversidade = fatores_diversidade.get(quantidade, fatores_diversidade[max(fatores_diversidade.keys())])
        
        # Calcular a demanda ajustada para o apartamento
        demanda_apartamento = fator_diversidade * potencia
        
        # Atualizar a demanda total
        total_demanda += demanda_apartamento

        detalhes_demanda.append(f"{descricao}: {demanda_apartamento:.2f} kVA")
        detalhes_calculo.append(f"Descrição: {descricao}")
        detalhes_calculo.append(f"Número de Apartamentos: {quantidade}")
        detalhes_calculo.append(f"Fator de Diversidade: {fator_diversidade:.2f}")
        detalhes_calculo.append(f"Área do Apartamento: {area:.2f} m²")
        detalhes_calculo.append(f"Potência do Apartamento: {potencia:.2f} kVA")
        detalhes_calculo.append("")

    # Atualizar a interface com a demanda total e detalhes
    demanda_total_label.config(text=f"Demanda Total: {total_demanda:.2f} kVA")
    detalhes_demanda_text.set("\n".join(detalhes_demanda))
    
    # Gerar o memorial de cálculo
    gerar_memorial_calculo(
        total_demanda,
        detalhes_calculo
    )

detalhes_calculo = [
    "1. Cálculo da Demanda Total:",
    "   - Demanda Base: 10 kVA",
    "   - Fator de Correção: 1.2",
    "   - Resultado: 12 kVA",
    "2. Cálculo da Distribuição por Andar:",
    "   - Número de Apartamentos: 20",
    "   - Demanda por Apartamento: 0.6 kVA",
    "   - Total: 12 kVA",
    "Observações:",
    "   - A demanda total foi calculada com base nos parâmetros fornecidos."
]

def gerar_memorial_calculo(total_demanda, detalhes_calculo):
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

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gestão de Apartamentos")

# Layout da interface
frame_form = tk.Frame(root)
frame_form.pack(padx=10, pady=10)

tk.Label(frame_form, text="Descrição").grid(row=0, column=0, padx=5, pady=5)
entry_descricao = tk.Entry(frame_form)
entry_descricao.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Quantidade").grid(row=1, column=0, padx=5, pady=5)
combobox_quantidade = ttk.Combobox(frame_form, values=quantidades)
combobox_quantidade.grid(row=1, column=1, padx=5, pady=5)
combobox_quantidade.bind("<<ComboboxSelected>>", lambda event: atualizar_fatores())

tk.Label(frame_form, text="Área (m²)").grid(row=2, column=0, padx=5, pady=5)
combobox_area = ttk.Combobox(frame_form, values=areas)
combobox_area.grid(row=2, column=1, padx=5, pady=5)
combobox_area.bind("<<ComboboxSelected>>", lambda event: atualizar_fatores())

btn_adicionar = tk.Button(frame_form, text="Adicionar", command=adicionar_apartamento)
btn_adicionar.grid(row=3, column=0, padx=5, pady=5)

btn_editar = tk.Button(frame_form, text="Editar", command=editar_apartamento)
btn_editar.grid(row=3, column=1, padx=5, pady=5)

btn_remover = tk.Button(frame_form, text="Remover", command=remover_apartamento)
btn_remover.grid(row=3, column=2, padx=5, pady=5)

btn_calcular_demanda = tk.Button(frame_form, text="Calcular Demanda", command=calcular_demanda)
btn_calcular_demanda.grid(row=3, column=3, padx=5, pady=5)

frame_lista = tk.Frame(root)
frame_lista.pack(padx=10, pady=10)

lista_apartamentos = ttk.Treeview(frame_lista, columns=("Descrição", "Quantidade", "Área"), show='headings')
lista_apartamentos.heading("Descrição", text="Descrição")
lista_apartamentos.heading("Quantidade", text="Quantidade")
lista_apartamentos.heading("Área", text="Área")
lista_apartamentos.bind("<ButtonRelease-1>", selecionar_apartamento)
lista_apartamentos.pack()

frame_resultados = tk.Frame(root)
frame_resultados.pack(padx=10, pady=10)

demanda_total_label = tk.Label(frame_resultados, text="Demanda Total: 0.00 kVA")
demanda_total_label.pack()

fator_diversidade_label = tk.Label(frame_resultados, text="Fator de Diversidade: Não encontrado")
fator_diversidade_label.pack()

fator_potencia_label = tk.Label(frame_resultados, text="Potência por Área: Não encontrado")
fator_potencia_label.pack()

detalhes_demanda_text = tk.StringVar()
detalhes_demanda_label = tk.Label(frame_resultados, textvariable=detalhes_demanda_text, justify=tk.LEFT)
detalhes_demanda_label.pack()

root.mainloop()
