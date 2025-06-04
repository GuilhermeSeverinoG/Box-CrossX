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

        self.treeAlunos.bind("<<TreeviewSelect>>", self.preencherCamposAluno)

        #Campos do formulário
        labelNome = tk.Label(janelaAlunos, text="Nome: ")
        labelNome.pack()
        self.campoNome = tk.Entry(janelaAlunos)
        self.campoNome.pack()

        labelEndereco= tk.Label(janelaAlunos, text="Endereço: ")
        labelEndereco.pack()
        self.campoEndereco = tk.Entry(janelaAlunos)
        self.campoEndereco.pack()

        labelCidade= tk.Label(janelaAlunos, text="Cidade: ")
        labelCidade.pack()
        self.campoCidade = tk.Entry(janelaAlunos)
        self.campoCidade.pack()

        labelEstado= tk.Label(janelaAlunos, text="Estado: ")
        labelEstado.pack()
        self.campoEstado = tk.Entry(janelaAlunos)
        self.campoEstado.pack()

        labelTelefone= tk.Label(janelaAlunos, text="Telefone: ")
        labelTelefone.pack()
        self.campoTelefone = tk.Entry(janelaAlunos)
        self.campoTelefone.pack()

        labelDataMatricula= tk.Label(janelaAlunos, text="Data de matrícula: ")
        labelDataMatricula.pack()
        self.campoDataMatricula = tk.Entry(janelaAlunos)
        self.campoDataMatricula.pack()

        labelDataVencimento= tk.Label(janelaAlunos, text="Data de vencimento: ")
        labelDataVencimento.pack()
        self.campoDataVencimento = tk.Entry(janelaAlunos)
        self.campoDataVencimento.pack()

        labelDataDesligamento= tk.Label(janelaAlunos, text="Data de desligamento: ")
        labelDataDesligamento.pack()
        self.campoDataDesligamento = tk.Entry(janelaAlunos)
        self.campoDataDesligamento.pack()
        #Botões
        btnCadastrar= tk.Button(janelaAlunos,text="Cadatrar aluno", command=self.cadastrarAluno)
        btnCadastrar.pack()
        
        btnAtualizar= tk.Button(janelaAlunos,text="Atualizar", command=self.atualizarAluno)
        btnAtualizar.pack()

        btnExcluir= tk.Button(janelaAlunos,text="Excluir", command=self.deletarAluno)
        btnExcluir.pack()

        self.exibirAlunos()

    def preencherCamposAluno(self, event):
        # Pega item selecionado
        item = self.treeAlunos.selection()
        if item:
            valores = self.treeAlunos.item(item[0], "values")

            # Armazena ID do aluno selecionado (importante para o UPDATE)
            self.idSelecionado = valores[0]

            # Preenche os campos
            self.campoNome.delete(0, tk.END)
            self.campoNome.insert(0, valores[1])

            self.campoEndereco.delete(0, tk.END)
            self.campoEndereco.insert(0, valores[2])

            self.campoCidade.delete(0, tk.END)
            self.campoCidade.insert(0, valores[3])

            self.campoEstado.delete(0, tk.END)
            self.campoEstado.insert(0, valores[4])

            self.campoTelefone.delete(0, tk.END)
            self.campoTelefone.insert(0, valores[5])

            self.campoDataMatricula.delete(0, tk.END)
            self.campoDataMatricula.insert(0, valores[6])

            self.campoDataVencimento.delete(0, tk.END)
            self.campoDataVencimento.insert(0, valores[7])

            self.campoDataDesligamento.delete(0, tk.END)
            self.campoDataDesligamento.insert(0, valores[8])    

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

    def cadastrarAluno(self):
        try:
            nome = self.campoNome.get()
            endereco = self.campoEndereco.get()
            cidade=self.campoCidade.get()
            estado=self.campoEstado.get()
            telefone=self.campoTelefone.get()
            dataMatricula=self.campoDataMatricula.get()
            dataVencimento=self.campoDataVencimento.get()
            dataDesligamento=self.campoDataDesligamento.get()
            self.objetoBanco.cadastrarAluno(nome,endereco,cidade,estado,telefone,dataMatricula,dataDesligamento,dataVencimento)
            self.exibirAlunos()

            self.campoNome.delete(0, tk.END)
            self.campoEndereco.delete(0, tk.END)
            self.campoCidade.delete(0, tk.END)
            self.campoEstado.delete(0, tk.END)
            self.campoTelefone.delete(0, tk.END)
            self.campoDataMatricula.delete(0, tk.END)
            self.campoDataVencimento.delete(0, tk.END)
            self.campoDataDesligamento.delete(0, tk.END)
            print("Aluno cadastrado com sucesso")
        except:
            print("Não foi possivel cadastrar")
    def atualizarAluno(self):
        try:
            nome = self.campoNome.get()
            endereco = self.campoEndereco.get()
            cidade = self.campoCidade.get()
            estado = self.campoEstado.get()
            telefone = self.campoTelefone.get()
            self.objetoBanco.atualizarAluno(self.idSelecionado, nome, endereco, cidade, estado, telefone)
            self.exibirAlunos()

            print("Aluno atualizado com sucesso")
        except Exception as e:
            print("Erro ao atualizar aluno:", e)

    def deletarAluno(self):
       try:
            selected_item = self.treeAlunos.selection()
            item = self.treeAlunos.item(selected_item)
            product = item["values"]
            product_id = product[0]
            self.objetoBanco.deletarAluno(product_id)

            self.campoNome.delete(0,tk.END)
            self.campoEndereco.delete(0,tk.END)
            self.campoCidade.delete(0,tk.END)
            self.campoEstado.delete(0,tk.END)
            self.campoTelefone.delete(0,tk.END)
            self.campoDataMatricula.delete(0,tk.END)
            self.campoDataVencimento.delete(0,tk.END)
            self.campoDataDesligamento.delete(0,tk.END)
            self.exibirAlunos()
       except:
          print("Nao foi possivel deletar!")
#Janela princial
janela = tk.Tk()
janela.geometry("700x500")
app = PrincipalBD(janela)
janela.mainloop()
