import tkinter as tk
from tkinter import ttk
import database

class PrincipalBD():
    def __init__(self, win):
        self.objetoBanco = database.AppBd()
        self.janela = win
        self.janela.title("Academia CrossX")

        self.menu_principal = tk.Menu(self.janela)
        self.janela.config(menu=self.menu_principal)

        self.menu_principal.add_command(label="Gerenciar Alunos")
        self.menu_principal.add_command(label="Pagamentos")
        self.menu_principal.add_command(label="Histórico de Pagamentos")

    

# Janela principal
janela = tk.Tk()
janela.geometry("900x700")
app = PrincipalBD(janela)
janela.mainloop()
