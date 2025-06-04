from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import database

class PrincipalBD():
    def __init__(self, win):
        self.objetoBanco = database.AppBd()
        self.janela = win
        self.janela.title("Academia CrossX")
        self.janela.geometry("800x600")

        cor_menu = "#d3d3d3"

        barra_menu = tk.Frame(self.janela, bg=cor_menu, height=40)
        barra_menu.pack(side=tk.TOP, fill=tk.X)

        # Container central para os botões
        container = tk.Frame(barra_menu, bg=cor_menu)
        container.pack(expand=True)

        btn_alunos = tk.Button(container, text="Gerenciar Alunos",
                               bg=cor_menu, bd=0, relief=tk.FLAT, command=self.janelaGerenciarAlunos)
        btn_alunos.pack(side=tk.LEFT, padx=(10, 0), pady=5)

        self._divisor(container)

        btn_pagamentos = tk.Button(container, text="Pagamentos",
                                   bg=cor_menu, bd=0, relief=tk.FLAT, command=self.janelaAbrirPagamentos)
        btn_pagamentos.pack(side=tk.LEFT, padx=5, pady=5)

        self._divisor(container)

        btn_historico = tk.Button(container, text="Histórico de Pagamentos",
                                  bg=cor_menu, bd=0, relief=tk.FLAT, command=self.janelaHistoricoPagamentos)
        btn_historico.pack(side=tk.LEFT, padx=5, pady=5)

    def _divisor(self, frame):
        tk.Label(frame, text="|", bg="#d3d3d3", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    #Janela principal
    def janelaGerenciarAlunos(self):
        janelaAlunos = tk.Toplevel(self.janela)
        janelaAlunos.title("Gerenciar Alunos")
        janelaAlunos.geometry("1000x500")

        # Tabela
        self.treeAlunos = ttk.Treeview(
            janelaAlunos,
            columns=("Id aluno", "Nome", "Endereco", "Cidade", "Estado", "Telefone", "Data Matricula", "Data Desligamento", "Data Vencimento"),
            show='headings'
        )

        for col in self.treeAlunos["columns"]:
            self.treeAlunos.heading(col, text=col)
            self.treeAlunos.column(col, width=100)
        self.treeAlunos.column("Id aluno", width=60)
        self.treeAlunos.column("Estado", width=60)
        self.treeAlunos.pack()

        #Prenchimento de campos
        self.treeAlunos.bind("<<TreeviewSelect>>", self.preencherCamposAluno)

        # Campos do formulário
        self.campoNome = tk.Entry(janelaAlunos)
        self.campoEndereco = tk.Entry(janelaAlunos)
        self.campoCidade = tk.Entry(janelaAlunos)
        estados_brasil = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA","MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        self.campoEstado = ttk.Combobox(janelaAlunos, values=estados_brasil, state="readonly")
        self.campoTelefone = tk.Entry(janelaAlunos)
        self.campoDataMatricula = tk.Entry(janelaAlunos)
        self.campoDataDesligamento = tk.Entry(janelaAlunos)
        self.campoDataVencimento = tk.Entry(janelaAlunos)

        #Criando as labels
        for label, entry in [
            ("Nome", self.campoNome),
            ("Endereço", self.campoEndereco),
            ("Cidade", self.campoCidade),
            ("Estado", self.campoEstado),
            ("Telefone", self.campoTelefone),
            ("Data de matrícula", self.campoDataMatricula),
            ("Data de desligamento", self.campoDataDesligamento),
            ("Data de vencimento", self.campoDataVencimento),
        ]:
            tk.Label(janelaAlunos, text=f"{label}:").pack()
            entry.pack()

        #Botões
        tk.Button(janelaAlunos, text="Cadastrar aluno", command=self.cadastrarAluno).pack()
        tk.Button(janelaAlunos, text="Atualizar", command=self.atualizarAluno).pack()
        tk.Button(janelaAlunos, text="Excluir", command=self.deletarAluno).pack()

        self.exibirAlunos()

    #Método para preencher os textfields da janela de alunos
    def preencherCamposAluno(self, event):
        item = self.treeAlunos.selection()
        if item:
            valores = self.treeAlunos.item(item[0], "values")
            self.idSelecionado = valores[0]
            campos = [self.campoNome, self.campoEndereco, self.campoCidade, self.campoEstado, self.campoTelefone, self.campoDataMatricula, self.campoDataDesligamento, self.campoDataVencimento]
            for i, campo in enumerate(campos):
                campo.delete(0, tk.END)
                campo.insert(0, valores[i+1])

    #Janela dos pagamentos
    def janelaAbrirPagamentos(self):
        janelaAbrirPagamentos = tk.Toplevel(self.janela)
        janelaAbrirPagamentos.title("Pagamentos")
        janelaAbrirPagamentos.geometry("600x500")

        #Tabela
        self.treePagamentos = ttk.Treeview(janelaAbrirPagamentos, columns=("ID", "Nome"), show="headings")
        self.treePagamentos.heading("ID", text="ID")
        self.treePagamentos.heading("Nome", text="Nome")
        self.treePagamentos.column("ID", width=50)
        self.treePagamentos.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        def preencherCamposPagamento(event):
            item = self.treePagamentos.selection()
            if item:
                valores = self.treePagamentos.item(item[0], "values")
                self.campoId.delete(0, tk.END)
                self.campoId.insert(0, valores[0])
                self.campoNomeAluno.delete(0, tk.END)
                self.campoNomeAluno.insert(0, valores[1])
        #Função para preencher textfiels
        self.treePagamentos.bind("<<TreeviewSelect>>", preencherCamposPagamento)

        try:
            alunos = self.objetoBanco.selecionarAlunos()
            for aluno in alunos:
                self.treePagamentos.insert("", tk.END, values=(aluno[0], aluno[1]))
        except Exception as e:
            print("Erro ao carregar alunos:", e)

        #Formulário
        self.campoId = tk.Entry(janelaAbrirPagamentos)
        self.campoNomeAluno = tk.Entry(janelaAbrirPagamentos)
        self.valor = tk.Entry(janelaAbrirPagamentos)
        self.tipo = ttk.Combobox(janelaAbrirPagamentos, values=["dinheiro", "cartão"])
        self.tipo.set("dinheiro")

        #Laço para criar labels
        labels = ["ID do Aluno", "Nome do Aluno", "Valor (R$)", "Tipo de Pagamento"]
        entries = [self.campoId, self.campoNomeAluno, self.valor, self.tipo]
        for i, (label, widget) in enumerate(zip(labels, entries)):
            tk.Label(janelaAbrirPagamentos, text=label).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
            widget.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")

        #Botão de cadastrar
        btnCadastrarPag = tk.Button(janelaAbrirPagamentos, text="Cadastrar", command=self.cadastrarPagamento)
        btnCadastrarPag.grid(row=6, column=0, columnspan=2, pady=10)

    #Janela do histórico de pagamentos
    def janelaHistoricoPagamentos(self):
        #from tkinter import ttk  # Certifique-se de importar se estiver em outro escopo
        janela = tk.Toplevel(self.janela)
        janela.title("Histórico de Pagamentos")
        janela.geometry("600x400")

        #Campos
        tk.Label(janela, text="ID Pagamento").grid(row=0, column=0)
        id_pagamento_entry = tk.Entry(janela)
        id_pagamento_entry.grid(row=0, column=1)

        tk.Label(janela, text="ID Aluno").grid(row=1, column=0)
        id_aluno_entry = tk.Entry(janela)
        id_aluno_entry.grid(row=1, column=1)

        tk.Label(janela, text="Data").grid(row=2, column=0)
        data_entry = tk.Entry(janela)
        data_entry.grid(row=2, column=1)

        tk.Label(janela, text="Valor").grid(row=3, column=0)
        valor_entry = tk.Entry(janela)
        valor_entry.grid(row=3, column=1)

        tk.Label(janela, text="Tipo").grid(row=4, column=0)
        tipo_entry = ttk.Combobox(janela, values=["dinheiro", "cartão"], state="readonly")
        tipo_entry.grid(row=4, column=1)
        tipo_entry.set("dinheiro")  # valor padrão

        # Tabela
        self.treePagamentos = ttk.Treeview(
            janela,
            columns=("id_pagamento", "id_aluno", "data", "valor", "tipo"),
            show="headings"
        )
        for col in self.treePagamentos["columns"]:
            self.treePagamentos.heading(col, text=col)
        self.treePagamentos.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        #Seleção da tabela preenche os campos
        def on_select(event):
            item = self.treePagamentos.selection()
            if item:
                valores = self.treePagamentos.item(item, "values")
                id_pagamento_entry.delete(0, tk.END)
                id_pagamento_entry.insert(0, valores[0])
                id_aluno_entry.delete(0, tk.END)
                id_aluno_entry.insert(0, valores[1])
                data_entry.delete(0, tk.END)
                data_entry.insert(0, valores[2])
                valor_entry.delete(0, tk.END)
                valor_entry.insert(0, valores[3])
                tipo_entry.set(valores[4])

        self.treePagamentos.bind("<<TreeviewSelect>>", on_select)

        #Botões
        tk.Button(janela, text="Atualizar", command=self.atualizarAluno).grid(row=6, column=1, pady=10)
        tk.Button(janela, text="Excluir", command=self.deletarAluno).grid(row=6, column=2, pady=10)

        self.exibirPagamentos()

    #========== Métodos do CRUD do aluno ==========#
    #Método Read
    def exibirAlunos(self):
        try:
            self.treeAlunos.delete(*self.treeAlunos.get_children())
            alunos = self.objetoBanco.selecionarAlunos()
            for aluno in alunos:
                self.treeAlunos.insert("", tk.END, values=aluno)
        except Exception as e:
            print("Não foi possível exibir os alunos:", e)
    #Método Create
    def cadastrarAluno(self):
        try:
            nome = self.campoNome.get()
            endereco = self.campoEndereco.get()
            cidade = self.campoCidade.get()
            estado = self.campoEstado.get()
            telefone = self.campoTelefone.get()
            dataMatricula = datetime.now().strftime("%d/%m/%Y")
            dataVencimento = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
            dataVencimentoCampo = self.campoDataVencimento.get()
            dataDesligamento = self.campoDataDesligamento.get()

            if dataDesligamento.strip() or dataVencimentoCampo.strip():
                messagebox.showerror("Erro", "Os campos de data de matrícula e vencimento devem estar vazios. Eles são definidos automaticamente.")
                return
            #Verificação de campos vazios
            if not all([nome, endereco, cidade, estado, telefone, dataMatricula]):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return

            self.objetoBanco.cadastrarAluno(nome, endereco, cidade, estado, telefone, dataMatricula, None, dataVencimento)
            self.exibirAlunos()

            for campo in [self.campoNome, self.campoEndereco, self.campoCidade, self.campoEstado, self.campoTelefone]:
                campo.delete(0, tk.END)

            messagebox.showinfo("Sucesso","Aluno cadastrado com sucesso.")
        except Exception as e:
            print("Não foi possível cadastrar:", e)
    #Upadate
    def atualizarAluno(self):
        try:
            nome = self.campoNome.get()
            endereco = self.campoEndereco.get()
            cidade = self.campoCidade.get()
            estado = self.campoEstado.get()
            telefone = self.campoTelefone.get()
            dataMatricula = self.campoDataMatricula.get()
            dataDesligamento = self.campoDataDesligamento.get()
            dataVencimento = self.campoDataVencimento.get()

            # Verifica se todos os campos obrigatórios foram preenchidos
            if not all([nome, endereco, cidade, estado, telefone, dataMatricula, dataVencimento]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
                return

            # Converte datas obrigatórias
            try:
                data_matricula = datetime.strptime(dataMatricula, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Data de matrícula inválida. Use o formato DD/MM/AAAA.")
                return
            try:
                data_vencimento = datetime.strptime(dataVencimento, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Data de vencimento inválida. Use o formato DD/MM/AAAA.")
                return

            #Matrícula deve ser anterior ao vencimento
            if data_matricula >= data_vencimento:
                messagebox.showerror("Erro", "A data de matrícula deve ser anterior à data de vencimento.")
                return

            # Atualiza no banco
            self.objetoBanco.atualizarAluno(
                self.idSelecionado,
                nome, endereco, cidade, estado, telefone,
                dataMatricula, dataDesligamento, dataVencimento
            )

            self.exibirAlunos()
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso.")

        except Exception as e:
            print("Erro ao atualizar aluno:", e)
            messagebox.showerror("Erro","Falha ao atualizar aluno:")
    #Delete
    def deletarAluno(self):
        try:
            selected_item = self.treeAlunos.selection()
            if not selected_item:
                print("Nenhum aluno selecionado.")
                return

            item = self.treeAlunos.item(selected_item)
            valores = item["values"]
            #Pega pelo posição na tabela       
            aluno_id = valores[0]
            data_desligamento_str = valores[7]
            
            #Deleta se data de desligamento NÃO for None, vazio ou ""
            if data_desligamento_str.strip() == "" or data_desligamento_str.strip().lower() == "none":
                messagebox.showerror("Erro", "Aluno sem data de desligamento. Exclusão não permitida.")
                return
            #Verifica data de deligamento
            try:
                data_desligamento = datetime.strptime(data_desligamento_str, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Data de desligamento inválida.")
                return

            self.objetoBanco.deletarAluno(aluno_id)

            #Limpar campos
            for campo in [self.campoNome, self.campoEndereco, self.campoCidade, self.campoEstado, self.campoTelefone,self.campoEstado,self.campoDataMatricula, self.campoDataDesligamento,self.campoDataVencimento]:
                campo.delete(0, tk.END)

            self.exibirAlunos()
            messagebox.showinfo("Sucesso","Aluno excluído com sucesso.")
        except Exception as e:
            print("Não foi possível deletar:", e)

    #========== Métodos do CRUD do pagegamento ==========#
    #Método Read
    def exibirPagamentos(self):
        try:
            self.treePagamentos.delete(*self.treePagamentos.get_children())
            pagamentos = self.objetoBanco.selecionarPagamentos()
            for aluno in pagamentos:
                self.treePagamentos.insert("", tk.END, values=aluno)
        except Exception as e:
            print("Não foi possível exibir os pagamentos:", e)
    #Create do pagamento
    def cadastrarPagamento(self):
        try:
            id_aluno = self.campoId.get()
            valor = self.valor.get()
            tipo = self.tipo.get()
            data_pagamento = datetime.now().strftime("%d/%m/%Y")

            if not id_aluno or not valor or not tipo:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            self.objetoBanco.cadastrarPagamento(id_aluno, data_pagamento, valor, tipo)
            print("Pagamento cadastrado com sucesso.")

            self.campoId.delete(0, tk.END)
            self.campoNomeAluno.delete(0, tk.END)
            self.valor.delete(0, tk.END)
            self.tipo.set("dinheiro")

        except Exception as e:
            print("Erro ao cadastrar pagamento:", e)
# Janela principal
janela = tk.Tk()
janela.geometry("700x500")
app = PrincipalBD(janela)
janela.mainloop()
