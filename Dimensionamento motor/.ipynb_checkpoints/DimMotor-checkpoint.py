import tkinter as tk
from tkinter import ttk
import math
import time


class MotorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Motor")
        self.root.geometry("600x450")

        self.angle = 0  # Ângulo inicial do motor
        self.angular_velocity = 10  # Velocidade angular inicial em graus por segundo

        self.create_widgets()

    def create_widgets(self):
        # Motor (representado como um Canvas)
        self.canvas_motor = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.canvas_motor.pack(pady=20)

        # Label e Entry para inserir o ângulo desejado
        ttk.Label(self.root, text="Ângulo do Eixo do Motor:").pack()
        self.entry_angle = ttk.Entry(self.root, width=10)
        self.entry_angle.pack()

        # Label e Entry para inserir a velocidade angular desejada
        ttk.Label(self.root, text="Velocidade Angular (graus/seg):").pack()
        self.entry_velocity = ttk.Entry(self.root, width=10)
        self.entry_velocity.insert(tk.END, str(self.angular_velocity))
        self.entry_velocity.pack()

        # Botão para definir o ângulo e velocidade angular
        self.button_set_params = ttk.Button(self.root, text="Definir Parâmetros", command=self.definir_parametros)
        self.button_set_params.pack()

        # Botão para iniciar movimento automático
        self.button_automatico = ttk.Button(self.root, text="Iniciar Movimento Automático", command=self.iniciar_movimento_automatico)
        self.button_automatico.pack()

    def definir_parametros(self):
        try:
            self.angle = float(self.entry_angle.get())
            self.angular_velocity = float(self.entry_velocity.get())
            self.update_motor()
        except ValueError:
            tk.messagebox.showerror("Erro", "Insira valores numéricos para ângulo e velocidade angular.")

    def update_motor(self):
        # Limpar o canvas do motor
        self.canvas_motor.delete("all")

        # Centro do motor
        x_center, y_center = 200, 150

        # Ponta do motor
        x_tip = x_center + 120 * math.cos(math.radians(self.angle))
        y_tip = y_center - 120 * math.sin(math.radians(self.angle))

        # Desenhar o motor
        self.canvas_motor.create_line(x_center, y_center, x_tip, y_tip, width=5, arrow=tk.LAST)

        # Desenhar o ângulo atual
        x_text = x_center + 140 * math.cos(math.radians(self.angle))
        y_text = y_center - 140 * math.sin(math.radians(self.angle))
        self.canvas_motor.create_text(x_text, y_text, text=f"{self.angle:.1f}°", font=("Helvetica", 10), anchor=tk.CENTER)

        # Desenhar a velocidade angular
        self.canvas_motor.create_text(x_center, y_center + 100, text=f"Velocidade Angular: {self.angular_velocity:.1f} graus/seg",
                                      font=("Helvetica", 10), anchor=tk.CENTER)

    def iniciar_movimento_automatico(self):
        target_angle = float(self.entry_angle.get())  # Obtém o ângulo alvo definido pelo usuário

        # Calcula a menor distância entre o ângulo atual e o ângulo alvo
        diff_angle = (target_angle - self.angle + 180) % 360 - 180

        # Determina a direção mais curta para girar até o ângulo alvo
        if diff_angle > 0:
            direction = 1  # Sentido horário
        else:
            direction = -1  # Sentido anti-horário

        # Número de passos necessários para girar até o ângulo alvo
        steps = int(abs(diff_angle) / 10) + 1  # Cada passo gira 10 graus

        for _ in range(steps):
            self.angle += direction * 10  # Gira 10 graus na direção adequada
            self.update_motor()
            self.root.update()  # Atualiza a interface gráfica
            time.sleep(1 / self.angular_velocity)  # Aguarda o tempo correspondente à velocidade angular

        # Atualiza o ângulo para o valor alvo
        self.angle = target_angle
        self.update_motor()


if __name__ == "__main__":
    root = tk.Tk()
    app = MotorApp(root)
    root.mainloop()
