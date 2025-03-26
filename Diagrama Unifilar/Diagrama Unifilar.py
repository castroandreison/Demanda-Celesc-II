import matplotlib.pyplot as plt

# Função para desenhar o diagrama unifilar com informações sobre ramal de entrada e 5 apartamentos
def desenhar_diagrama_unifilar(bitola_cabo, tipo_duto, num_apartamentos, ramal_info):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Desenhar o Ramal de Entrada principal com as informações de bitola, duto e fases
    ax.plot([0.1, 0.2], [0.9, 0.9], color="black", lw=3)
    ax.text(0.05, 0.9, "Ramal de Entrada", fontsize=12, ha='center')
    ax.text(0.45, 0.9, ramal_info, fontsize=12, ha='left', color='red')

    # Desenhar a linha principal que alimenta todos os apartamentos
    ax.plot([0.2, 0.2], [0.9, 0.1], color="black", lw=3)
    ax.text(0.25, 0.5, "Linha principal", fontsize=10, ha='center', rotation=90)

    # Adicionar 5 apartamentos com suas respectivas cargas e disjuntores
    for i in range(num_apartamentos):
        altura = 0.85 - i * 0.15  # Altura para cada apartamento
        ax.plot([0.2, 0.4], [altura, altura], color="black", lw=3)  # Ligação do disjuntor à carga
        ax.text(0.45, altura, f"Apartamento {i+1}", fontsize=12, ha='center')
        
        # Desenhar o disjuntor
        ax.plot([0.35, 0.35], [altura, altura - 0.1], color="black", lw=3)
        ax.plot([0.3, 0.4], [altura - 0.1, altura - 0.1], color="black", lw=3)
        ax.text(0.45, altura - 0.1, f"Disjuntor {i+1}", fontsize=10, ha='center')

        # Informações sobre a bitola e o duto
        ax.text(0.35, altura + 0.05, f"Bitola: {bitola_cabo}", fontsize=9, ha='center', color='blue')
        ax.text(0.35, altura + 0.1, f"Duto: {tipo_duto}", fontsize=9, ha='center', color='green')

    # Ajustes finais no diagrama
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.show()

# Exemplo de uso com 5 apartamentos e informações do ramal de entrada
bitola_cabo = "16 mm²"
tipo_duto = "PVC 25 mm"
num_apartamentos = 5
ramal_info = "3F/N/T - 3x150mm²/150mm²/70mm²"

desenhar_diagrama_unifilar(bitola_cabo, tipo_duto, num_apartamentos, ramal_info)
