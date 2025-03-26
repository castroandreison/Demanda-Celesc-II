import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def potencia_motor_em_kva(potencia_hp):
    # Tabela de conversão de HP para kVA
    tabela_motores = {
        1/3: (0.39, 0.65, 1.7, 7.1, 0.61),
        1/2: (0.58, 0.87, 2.3, 9.9, 0.66),
        3/4: (0.83, 1.26, 3.3, 16.3, 0.66),
        1: (1.05, 1.52, 4.0, 20.7, 0.69),
        1.5: (1.54, 2.17, 5.7, 33.1, 0.71),
        2: (1.95, 2.70, 7.1, 44.3, 0.72),
        3: (2.95, 4.04, 10.6, 65.9, 0.73),
        4: (3.72, 5.03, 13.2, 74.4, 0.74),
        5: (4.51, 6.02, 15.8, 98.9, 0.75),
        7.5: (6.57, 8.65, 22.7, 157.1, 0.76),
        10: (8.89, 11.54, 30.3, 201.1, 0.77),
        12.5: (10.85, 14.09, 37.0, 270.5, 0.77),
        15: (12.82, 16.65, 43.7, 340.6, 0.77),
        20: (17.01, 22.10, 58.0, 422.1, 0.77),
        25: (20.92, 25.83, 67.8, 477.6, 0.81),
        30: (25.03, 30.52, 80.1, 566.0, 0.82),
        40: (33.38, 39.74, 104.3, 717.3, 0.84),
        50: (40.93, 48.73, 127.9, 915.5, 0.84),
        60: (49.42, 58.15, 152.6, 1095.7, 0.85),
        75: (61.44, 72.28, 189.7, 1288.0, 0.85),
        100: (81.23, 95.56, 250.8, 1619.0, 0.85),
        125: (100.67, 117.05, 307.2, 2014.0, 0.86),
        150: (120.09, 141.29, 370.8, 2521.7, 0.85)
    }
    
    return tabela_motores.get(potencia_hp, (0, 0, 0, 0, 0))  # Retorna 0 se a potência não estiver na tabela
def calcular_demanda(cursor):
    # Demanda Referente à Iluminação e Tomadas de Uso Geral
    D1a = 18.00  # Demanda dos Apartamentos em kVA
    D1b = 14.42  # Demanda da Administração em kVA
    D1 = D1a + D1b  # Demanda total
    print(f"Demanda Total (Iluminação e Tomadas): {D1:.2f} kVA")

    # Demanda Referente a Aparelhos
    # Chuveiros e Torneiras Elétricas
    chuveiros_apto = 80  # 20 apartamentos com 4 chuveiros
    chuveiros_admin = 4   # 1 administração com 4 chuveiros
    torneiras_admin = 2    # 1 administração com 2 torneiras
    fator_demanda = 0.23

    D2a = (chuveiros_apto * 6.5 * fator_demanda) + (chuveiros_admin * 6.5 * fator_demanda) + (torneiras_admin * 3.0 * fator_demanda)
    D2a = round(D2a, 2)  # Arredondar para 2 casas decimais

    # Máquina de Secar Roupa
    D2b = (20 * 2.5 * 0.40)  # 20 apartamentos
    D2b = round(D2b, 2)

    # Máquina de Lavar Louça
    D2c = (20 * 2.5 * 0.42)  # 20 apartamentos
    D2c = round(D2c, 2)

    # Demanda de Aparelhos
    D2 = D2a + D2b + D2c
    D2 = round(D2, 2)

    # Demanda de aparelhos da administração
    D_admin_a = (chuveiros_admin * 6.5 * fator_demanda) + (torneiras_admin * 3.0 * fator_demanda)
    D_admin_a = round(D_admin_a, 2)

    # Demanda de aparelhos dos apartamentos
    D_apto = D2 - D_admin_a
    D_apto = round(D_apto, 2)

    print(f"Demanda Total (Aparelhos): {D2:.2f} kVA")
    print(f"Demanda Administração (Aparelhos): {D_admin_a:.2f} kVA")
    print(f"Demanda Apartamentos (Aparelhos): {D_apto:.2f} kVA")

    # Demanda Referente a Motores
    cursor.execute("SELECT potencia_cv FROM motores")
    motores = cursor.fetchall()
    maior_motor = 0
    demais_motores = 0
    for motor in motores:
        potencia_cv = motor[0]
        potencia_kva, _, _, _, _ = potencia_motor_em_kva(potencia_cv)
        if potencia_kva > maior_motor:
            demais_motores += maior_motor
            maior_motor = potencia_kva
        else:
            demais_motores += potencia_kva

    D3 = (maior_motor * 1.0) + (demais_motores * 0.5)
    D3 = round(D3, 2)

    print(f"Demanda Total (Motores): {D3:.2f} kVA")

    return D1, D2, D3

class DemandaEdificio:
    def __init__(self, area_apto, area_adm, num_aptos, num_chuveiros_apto, num_chuveiros_adm, num_torneiras_adm, num_maquinas_lavar, num_maquinas_secar, db_cursor):
        self.area_apto = area_apto
        self.area_adm = area_adm
        self.num_aptos = num_aptos
        self.num_chuveiros_apto = num_chuveiros_apto
        self.num_chuveiros_adm = num_chuveiros_adm
        self.num_torneiras_adm = num_torneiras_adm
        self.num_maquinas_lavar = num_maquinas_lavar
        self.num_maquinas_secar = num_maquinas_secar
        self.cursor = db_cursor

    def demanda_iluminacao_tomadas(self):
        D1a = 18.00
        D1b = 14.42
        D1 = D1a + D1b
        return D1

    def demanda_aparelhos(self):
        D2a = (self.num_chuveiros_apto * 6.5 * 0.23) + (self.num_chuveiros_adm * 6.5 * 0.23) + (self.num_torneiras_adm * 3.0 * 0.23)
        D2b = (self.num_maquinas_secar * 2.5 * 0.40)
        D2c = (self.num_maquinas_lavar * 2.5 * 0.42)
        D2 = D2a + D2b + D2c
        return D2

    def demanda_administracao(self):
        demanda_aparelhos_adm = (self.num_chuveiros_adm * 6.5 * 0.23) + (self.num_torneiras_adm * 3.0 * 0.23)
        return demanda_aparelhos_adm

    def demanda_apartamentos(self):
        demanda_aparelhos_total = self.demanda_aparelhos()
        demanda_administracao = self.demanda_administracao()
        demanda_aparelhos_apto = demanda_aparelhos_total - demanda_administracao
        return demanda_aparelhos_apto

    def demanda_motores(self):
        self.cursor.execute("SELECT potencia_cv FROM motores")
        motores = self.cursor.fetchall()
        maior_motor = 0
        demais_motores = 0
        for motor in motores:
            potencia_cv = motor[0]
            potencia_kva, _, _, _, _ = potencia_motor_em_kva(potencia_cv)
            if potencia_kva > maior_motor:
                demais_motores += maior_motor
                maior_motor = potencia_kva
            else:
                demais_motores += potencia_kva
        D3 = (maior_motor * 1.0) + (demais_motores * 0.5)
        return D3

    def demanda_total_apartamentos(self):
        D1 = 18.00
        D2 = self.demanda_apartamentos()
        D3 = 0.00
        coef_simultaneidade = 0.87
        Dapt = (D1 + D2 + D3) * coef_simultaneidade
        return Dapt

    def demanda_total_administracao(self):
        D1 = 14.42
        D2 = self.demanda_administracao()
        D3 = self.demanda_motores()
        Dadm = D1 + D2 + D3
        return Dadm

    def demanda_geral_entrada(self):
        Dapt = self.demanda_total_apartamentos()
        Dadm = self.demanda_total_administracao()
        Dg = Dapt + Dadm
        return Dg

    def gerar_relatorio(self):
        relatorio = f"""
        Relatório de Demanda Geral de Entrada:
        =======================================
        1. Demanda Referente à Iluminação e Tomadas de Uso Geral:
           - Demanda dos Apartamentos (D1a): 18,00 kVA
           - Demanda da Administração (D1b): 14,42 kVA
           - Demanda Total (D1): {self.demanda_iluminacao_tomadas():.2f} kVA

        2. Demanda Referente a Aparelhos:
           - Demanda Total (D2): {self.demanda_aparelhos():.2f} kVA
           - Demanda de Aparelhos da Administração: {self.demanda_administracao():.2f} kVA
           - Demanda de Aparelhos dos Apartamentos: {self.demanda_apartamentos():.2f} kVA

        3. Demanda Referente a Motores:
           - Demanda Total (D3): {self.demanda_motores():.2f} kVA

        4. Demanda Geral da Entrada:
           - Demanda Total dos Apartamentos (Dapt): {self.demanda_total_apartamentos():.2f} kVA
           - Demanda Total da Administração (Dadm): {self.demanda_total_administracao():.2f} kVA
           - Demanda Geral de Entrada (Dg): {self.demanda_geral_entrada():.2f} kVA
        """
        return relatorio

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cálculo de Demanda de Energia Elétrica")
        self.geometry("800x600")
        self.create_widgets()
        self.create_database()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Dados Gerais')
        tab_control.add(tab2, text='Aparelhos')
        tab_control.add(tab3, text='Motores')

        tab_control.pack(expand=1, fill='both')

        # Tab 1 - Dados Gerais
        ttk.Label(tab1, text="Área dos Apartamentos (m²):").grid(column=0, row=0, padx=10, pady=10)
        self.area_apto_entry = ttk.Entry(tab1)
        self.area_apto_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(tab1, text="Área da Administração (m²):").grid(column=0, row=1, padx=10, pady=10)
        self.area_adm_entry = ttk.Entry(tab1)
        self.area_adm_entry.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(tab1, text="Número de Apartamentos:").grid(column=0, row=2, padx=10, pady=10)
        self.num_
        self.num_aptos_entry = ttk.Entry(tab1)
        self.num_aptos_entry.grid(column=1, row=2, padx=10, pady=10)

        # Tab 2 - Aparelhos
        ttk.Label(tab2, text="Número de Chuveiros por Apartamento:").grid(column=0, row=0, padx=10, pady=10)
        self.num_chuveiros_apto_entry = ttk.Entry(tab2)
        self.num_chuveiros_apto_entry.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(tab2, text="Número de Chuveiros na Administração:").grid(column=0, row=1, padx=10, pady=10)
        self.num_chuveiros_adm_entry = ttk.Entry(tab2)
        self.num_chuveiros_adm_entry.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(tab2, text="Número de Torneiras na Administração:").grid(column=0, row=2, padx=10, pady=10)
        self.num_torneiras_adm_entry = ttk.Entry(tab2)
        self.num_torneiras_adm_entry.grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(tab2, text="Número de Máquinas de Lavar Louça:").grid(column=0, row=3, padx=10, pady=10)
        self.num_maquinas_lavar_entry = ttk.Entry(tab2)
        self.num_maquinas_lavar_entry.grid(column=1, row=3, padx=10, pady=10)

        ttk.Label(tab2, text="Número de Máquinas de Secar Roupa:").grid(column=0, row=4, padx=10, pady=10)
        self.num_maquinas_secar_entry = ttk.Entry(tab2)
        self.num_maquinas_secar_entry.grid(column=1, row=4, padx=10, pady=10)

        # Tab 3 - Motores
        ttk.Label(tab3, text="Potência do Motor (CV):").grid(column=0, row=0, padx=10, pady=10)
        self.potencia_motor_combobox = ttk.Combobox(tab3)
        self.potencia_motor_combobox.grid(column=1, row=0, padx=10, pady=10)
        self.potencia_motor_combobox.bind('<<ComboboxSelected>>', self.preencher_dados_motor)

        ttk.Label(tab3, text="Potência Absorvida da Rede (kVA):").grid(column=0, row=1, padx=10, pady=10)
        self.potencia_kva_entry = ttk.Entry(tab3)
        self.potencia_kva_entry.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(tab3, text="Corrente a Plena Carga (A):").grid(column=0, row=2, padx=10, pady=10)
        self.corrente_plena_carga_entry = ttk.Entry(tab3)
        self.corrente_plena_carga_entry.grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(tab3, text="Corrente de Partida (A):").grid(column=0, row=3, padx=10, pady=10)
        self.corrente_partida_entry = ttk.Entry(tab3)
        self.corrente_partida_entry.grid(column=1, row=3, padx=10, pady=10)

        ttk.Label(tab3, text="Fator de Potência Médio:").grid(column=0, row=4, padx=10, pady=10)
        self.fator_potencia_entry = ttk.Entry(tab3)
        self.fator_potencia_entry.grid(column=1, row=4, padx=10, pady=10)

        ttk.Button(tab3, text="Adicionar Motor", command=self.adicionar_motor).grid(column=1, row=5, padx=10, pady=10)

        self.motores_listbox = tk.Listbox(tab3)
        self.motores_listbox.grid(column=0, row=6, columnspan=2, padx=10, pady=10)

        # Buttons
        ttk.Button(self, text="Salvar Dados", command=self.salvar_dados).pack(side='left', padx=10, pady=10)
        ttk.Button(self, text="Carregar Dados", command=self.carregar_dados).pack(side='left', padx=10, pady=10)
        ttk.Button(self, text="Gerar Relatório", command=self.gerar_relatorio).pack(side='left', padx=10, pady=10)

    def create_database(self):
        self.conn = sqlite3.connect('demanda_energia.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS motores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                potencia_cv REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def adicionar_motor(self):
        potencia_cv = self.potencia_motor_combobox.get()
        if potencia_cv:
            self.cursor.execute("INSERT INTO motores (potencia_cv) VALUES (?)", (float(potencia_cv),))
            self.conn.commit()
            self.motores_listbox.insert(tk.END, potencia_cv)
            messagebox.showinfo("Sucesso", "Motor adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione uma potência de motor.")

    def salvar_dados(self):
        # Salvar dados gerais
        area_apto = self.area_apto_entry.get()
        area_adm = self.area_adm_entry.get()
        num_aptos = self.num_aptos_entry.get()
        num_chuveiros_apto = self.num_chuveiros_apto_entry.get()
        num_chuveiros_adm = self.num_chuveiros_adm_entry.get()
        num_torneiras_adm = self.num_torneiras_adm_entry.get()
        num_maquinas_lavar = self.num_maquinas_lavar_entry.get()
        num_maquinas_secar = self.num_maquinas_secar_entry.get()

        # Aqui você pode implementar a lógica para salvar esses dados em um arquivo ou banco de dados
        # Por simplicidade, vamos apenas mostrar uma mensagem
        messagebox.showinfo("Salvar Dados", "Dados salvos com sucesso!")

    def carregar_dados(self):
        # Aqui você pode implementar a lógica para carregar dados de um arquivo ou banco de dados
        # Por simplicidade, vamos apenas mostrar uma mensagem
        messagebox.showinfo("Carregar Dados", "Dados carregados com sucesso!")

    def gerar_relatorio(self):
        # Coletar dados para gerar o relatório
        area_apto = float(self.area_apto_entry.get())
        area_adm = float(self.area_adm_entry.get())
        num_aptos = int(self.num_aptos_entry.get())
        num_chuveiros_apto = int(self.num_chuveiros_apto_entry.get())
        num_chuveiros_adm = int(self.num_chuveiros_adm_entry.get())
        num_torneiras_adm = int(selfnum_torneiras_adm_entry.get())
        num_maquinas_lavar = int(self.num_maquinas_lavar_entry.get())
        num_maquinas_secar = int(self.num_maquinas_secar_entry.get())

        # Criar uma instância da classe DemandaEdificio
        edificio = DemandaEdificio(
            area_apto,
            area_adm,
            num_aptos,
            num_chuveiros_apto,
            num_chuveiros_adm,
            num_torneiras_adm,
            num_maquinas_lavar,
            num_maquinas_secar,
            self.cursor
        )

        # Gerar o relatório
        relatorio = edificio.gerar_relatorio()
        messagebox.showinfo("Relatório", relatorio)

    def preencher_dados_motor(self, event):
        # Preencher os dados do motor selecionado na combobox
        potencia_cv = self.potencia_motor_combobox.get()
        if potencia_cv:
            potencia_kva, corrente_plena_carga, corrente_partida, fator_potencia, _ = potencia_motor_em_kva(float(potencia_cv))
            self.potencia_kva_entry.delete(0, tk.END)
            self.potencia_kva_entry.insert(0, f"{potencia_kva:.2f}")
            self.corrente_plena_carga_entry.delete(0, tk.END)
            self.corrente_plena_carga_entry.insert(0, f"{corrente_plena_carga:.2f}")
            self.corrente_partida_entry.delete(0, tk.END)
            self.corrente_partida_entry.insert(0, f"{corrente_partida:.2f}")
            self.fator_potencia_entry.delete(0, tk.END)
            self.fator_potencia_entry.insert(0, f"{fator_potencia:.2f}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
