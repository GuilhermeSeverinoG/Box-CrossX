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

        self.menu_principal.add_command(label="Gerenciar Alunos", command=self.janelaGerenciarAlunos)
        self.menu_principal.add_command(label="Pagamentos", command=self.janelaAbrirPagamentos)
        self.menu_principal.add_command(label="Histórico de Pagamentos", command=self.janelaHistoricoPagamentos)

    def janelaGerenciarAlunos(self):
        janelaAlunos = tk.Toplevel(self.janela)
        janelaAlunos.title("Gerenciar Alunos")
        janelaAlunos.geometry("1000x500")
        #Tabela
        self.treeAlunos = ttk.Treeview(janelaAlunos, columns=("Id aluno",
                                                      "Nome", 
                                                      "Endereco",
                                                      "Cidade",
                                                      "Estado",
                                                      "Telefone",
                                                      "Data Matricula",
                                                      "Data Vencimento",
                                                      "Data Desligamento"), show='headings')
        self.treeAlunos.heading("Id aluno", text="ID")
        self.treeAlunos.heading("Nome", text="Nome")
        self.treeAlunos.heading("Endereco", text="Endereço")
        self.treeAlunos.heading("Cidade", text="Cidade")
        self.treeAlunos.heading("Estado", text="Estado")
        self.treeAlunos.heading("Telefone", text="Telefone")
        self.treeAlunos.heading("Data Matricula", text="Data de matrícula")
        self.treeAlunos.heading("Data Vencimento", text="Data de vencimento")
        self.treeAlunos.heading("Data Desligamento", text="Data de desligamento")
        self.treeAlunos.column("Id aluno", width=60)
        self.treeAlunos.column("Estado", width=60)
        self.treeAlunos.pack()
        #Campos do formulário
        labelNome = tk.Label(janelaAlunos, text="Nome: ")
        labelNome.pack()
        campoNome = tk.Entry(janelaAlunos)
        campoNome.pack()

        labelEndereco= tk.Label(janelaAlunos, text="Endereço: ")
        labelEndereco.pack()
        campoEndereco = tk.Entry(janelaAlunos)
        campoEndereco.pack()

        labelCidade= tk.Label(janelaAlunos, text="Cidade: ")
        labelCidade.pack()
        campoCidade = tk.Entry(janelaAlunos)
        campoCidade.pack()

        labelEstado= tk.Label(janelaAlunos, text="Estado: ")
        labelEstado.pack()
        campoEstado = tk.Entry(janelaAlunos)
        campoEstado.pack()

        labelTelefone= tk.Label(janelaAlunos, text="Telefone: ")
        labelTelefone.pack()
        campoTelefone = tk.Entry(janelaAlunos)
        campoTelefone.pack()

        labelDataMatricula= tk.Label(janelaAlunos, text="Data de matrícula: ")
        labelDataMatricula.pack()
        campoDataMatricula = tk.Entry(janelaAlunos)
        campoDataMatricula.pack()

        labelDataVencimento= tk.Label(janelaAlunos, text="Data de vencimento: ")
        labelDataVencimento.pack()
        campoDataVencimento = tk.Entry(janelaAlunos)
        campoDataVencimento.pack()

        labelDataDesligamento= tk.Label(janelaAlunos, text="Data de desligamento: ")
        labelDataDesligamento.pack()
        campoDataDesligamento = tk.Entry(janelaAlunos)
        campoDataDesligamento.pack()
        #Botões
        btnCadastrar= tk.Button(janelaAlunos,text="Cadatrar aluno")
        btnCadastrar.pack()
        
        btnAtualizar= tk.Button(janelaAlunos,text="Atualizar")
        btnAtualizar.pack()

        btnExcluir= tk.Button(janelaAlunos,text="Excluir")
        btnExcluir.pack()

        self.exibirAlunos()

    def janelaAbrirPagamentos(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Pagamentos")
        janela.geometry("400x300")

    def janelaHistoricoPagamentos(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Histórico de Pagamentos")
        janela.geometry("400x300")
    
    def exibirAlunos(self):
        try:
            self.treeAlunos.delete(*self.treeAlunos.get_children())
            alunos = self.objetoBanco.selecionarAlunos()
            for aluno in alunos:
                self.treeAlunos.insert("", tk.END, values=aluno)
        except Exception as e:
            print("Não foi possível exibir os alunos:", e)

#Janela princial
janela = tk.Tk()
janela.geometry("700x500")
app = PrincipalBD(janela)
janela.mainloop()
