import tkinter as tk
from tkinter import ttk
import database

class PrincipalBD():
    def __init__(self, win):
        self.objetoBanco = database.AppBd()
        self.janela = win

        self.botaoNovaJanela = tk.Button(self.janela, text="Teste", command=self.abrir_janela)
        self.botaoNovaJanela.pack(pady=10)

        self.treeProdutos = ttk.Treeview(
            self.janela,
            columns=("id", "nome", "endereco", "cidade", "estado", "telefone"),
            show='headings'
        )

        self.treeProdutos.heading("id", text="ID do Aluno")
        self.treeProdutos.heading("nome", text="Nome")
        self.treeProdutos.heading("endereco", text="Endereço")
        self.treeProdutos.heading("cidade", text="Cidade")
        self.treeProdutos.heading("estado", text="Estado")
        self.treeProdutos.heading("telefone", text="Telefone")

        self.treeProdutos.pack(fill="both", expand=True)

    def abrir_janela(self):
        nova = tk.Toplevel(self.janela)
        nova.title("Nova Janela - Cadastro de Aluno")
        nova.geometry("400x300")

        tk.Label(nova, text="Aqui você pode colocar um formulário!").pack(pady=20)

        tk.Label(nova, text="Nome:").pack()
        entry_nome = tk.Entry(nova)
        entry_nome.pack()

        tk.Button(nova, text="Fechar", command=nova.destroy).pack(pady=10)

janela = tk.Tk()
product_app = PrincipalBD(janela)
janela.geometry("900x700")
janela.mainloop()
