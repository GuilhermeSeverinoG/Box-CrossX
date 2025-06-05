from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
from PIL import Image, ImageTk

import database

class PrincipalBD():
    #========== Janelas ==========#
    #Janela principal
    def __init__(self, win):
        self.objetoBanco = database.AppBd()
        self.janela = win
        self.janela.title("Academia CrossX")
        self.janela.geometry("800x600")
        self.janela.configure(bg="white")

        cor_menu = "#d3d3d3"

        barra_menu = tk.Frame(self.janela, bg=cor_menu, height=40)
        barra_menu.pack(side=tk.TOP, fill=tk.X)

        #Conteiner ods botões do menu
        container = tk.Frame(barra_menu, bg=cor_menu)
        container.pack(expand=True)

        btn_alunos = tk.Button(container, text="Gerenciar Alunos",bg=cor_menu, bd=0, relief=tk.FLAT, command=self.janelaGerenciarAlunos)
        btn_alunos.pack(side=tk.LEFT, padx=(10, 0), pady=5)

        self.divisor(container)

        btn_pagamentos = tk.Button(container, text="Pagamentos", bg=cor_menu, bd=0, relief=tk.FLAT, command=self.janelaAbrirPagamentos)
        btn_pagamentos.pack(side=tk.LEFT, padx=5, pady=5)

        self.divisor(container)

        btn_historico = tk.Button(container, text="Histórico de Pagamentos",bg=cor_menu, bd=0, relief=tk.FLAT, command=self.janelaHistoricoPagamentos)
        btn_historico.pack(side=tk.LEFT, padx=5, pady=5)

        self.colocarImagemCentral()

    def divisor(self, frame):#Divisor decorativo do menu
        tk.Label(frame, text="|", bg="#d3d3d3", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

    def colocarImagemCentral(self):#Logo da empresa no meio da janela
        imagem = Image.open("imgs/logo.png")
        imagem = imagem.resize((400, 400), Image.Resampling.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem) #Converter para tkinter
        label_imagem = tk.Label(self.janela, image=imagem_tk, bg="white")
        label_imagem.image = imagem_tk
        label_imagem.pack(expand=True) #centralizar

    #Janela dos alunos
    def janelaGerenciarAlunos(self):
        janelaAlunos = tk.Toplevel(self.janela)
        janelaAlunos.title("Gerenciar Alunos")
        janelaAlunos.geometry("1000x600")
        janelaAlunos.configure(bg="white")

        estilo = ttk.Style()
        estilo.theme_use("default")

        estilo.configure("Treeview.Heading", background="#d3d3d3", foreground="black",font=("Arial", 10),relief="flat")

        estilo.configure("Treeview",background="#f4f4f4",foreground="black",fieldbackground="#f4f4f4", font=("Arial", 10))

        estilo.map("Treeview", background=[("selected", "#ccc")])

        #Tabela
        self.treeAlunos = ttk.Treeview(
            janelaAlunos,
            columns=("Id aluno", "Nome", "Endereco", "Cidade", "Estado", "Telefone", "Data Matricula", "Data Desligamento", "Data Vencimento"),
            show='headings'
        )

        col_largura = {
            "Id aluno": 60,
            "Nome": 120,
            "Endereco": 120,
            "Cidade": 120,
            "Estado": 60,
            "Telefone": 120,
            "Data Matricula": 120,
            "Data Desligamento": 120,
            "Data Vencimento": 120
        }

        for col in self.treeAlunos["columns"]:
            largura = col_largura.get(col, 100)
            self.treeAlunos.heading(col, text=col, anchor="center")
            self.treeAlunos.column(col, width=largura, anchor="center")

        self.treeAlunos.pack()

        #Tabela: preenchimento de campos da tabela
        self.treeAlunos.bind("<<TreeviewSelect>>", self.preencherCamposAluno)

        #Formulário
        #Formulário: campos do formulário
        self.campoNome = tk.Entry(janelaAlunos, width=25, bg="#f4f4f4")
        self.campoEndereco = tk.Entry(janelaAlunos, width=25, bg="#f4f4f4")
        self.campoCidade = tk.Entry(janelaAlunos, width=25, bg="#f4f4f4")
        estados_brasil = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA","MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        self.campoEstado = ttk.Combobox(janelaAlunos, values=estados_brasil, state="readonly", width=25)
        estilo = ttk.Style()
        estilo.configure('TCombobox', fieldbackground='#f4f4f4')
        self.campoTelefone = tk.Entry(janelaAlunos, width=25, bg="#f4f4f4")
        self.campoDataMatricula = tk.Entry(janelaAlunos, width=25, bg="#f4f4f4")
        self.campoDataDesligamento = tk.Entry(janelaAlunos, width=25, bg="#f4f4f4")
        self.campoDataVencimento = tk.Entry(janelaAlunos, width=25, bg="#f4f4f4")

        #Fromulário: labels
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

        #Formulário: botões
        botoes_frame = tk.Frame(janelaAlunos)
        botoes_frame.pack(pady=10)
        btn_cadastrar = tk.Button(
            botoes_frame, text="Cadastrar aluno", bg="#4CAF50", fg="white",
            width=20, bd=0, relief=tk.FLAT,
            command=self.cadastrarAluno
        )
        btn_cadastrar.pack(side=tk.LEFT, padx=5)

        btn_atualizar = tk.Button(
            botoes_frame, text="Atualizar", bg="#FFC107", fg="black",
            width=20, bd=0, relief=tk.FLAT,
            command=self.atualizarAluno
        )
        btn_atualizar.pack(side=tk.LEFT, padx=5)

        btn_excluir = tk.Button(
            botoes_frame, text="Excluir", bg="#F44336", fg="white",
            width=20, bd=0, relief=tk.FLAT,
            command=self.deletarAluno
        )
        btn_excluir.pack(side=tk.LEFT, padx=5)

        self.exibirAlunos()#Método de mostrar os alunos

    #Janela dos alunos: método para preencher os textfields da janela de alunos
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
        janelaAbrirPagamentos.geometry("600x550")
        janelaAbrirPagamentos.configure(bg="white")

        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview.Heading",background="#d3d3d3",foreground="black",font=("Arial", 10),relief="flat")
        estilo.configure("Treeview",background="#f4f4f4",foreground="black",fieldbackground="#f4f4f4",font=("Arial", 10))
        estilo.map("Treeview", background=[("selected", "#ccc")])

        #Tabela
        self.treePagamentos = ttk.Treeview(
            janelaAbrirPagamentos,
            columns=("ID", "Nome"),
            show="headings"
        )
        self.treePagamentos.heading("ID", text="ID")
        self.treePagamentos.heading("Nome", text="Nome")
        self.treePagamentos.column("ID", width=20, anchor="center")
        self.treePagamentos.column("Nome", width=100, anchor="center")
        self.treePagamentos.pack(padx=10, pady=10, fill="x")

        #Janela dos pagamentos: método para preencher campos
        def preencherCamposPagamento(event):
            item = self.treePagamentos.selection()
            if item:
                valores = self.treePagamentos.item(item[0], "values")
                self.campoId.delete(0, tk.END)
                self.campoId.insert(0, valores[0])
                self.campoNomeAluno.delete(0, tk.END)
                self.campoNomeAluno.insert(0, valores[1])
        self.treePagamentos.bind("<<TreeviewSelect>>", preencherCamposPagamento)

        #Selecionar alunos do banco
        try:
            alunos = self.objetoBanco.selecionarAlunos()
            for aluno in alunos:
                self.treePagamentos.insert("", tk.END, values=(aluno[0], aluno[1]))
        except Exception as e:
            print("Erro ao carregar alunos:", e)

        #Formulário: cmapos
        self.campoId = tk.Entry(janelaAbrirPagamentos, bg="#f4f4f4")
        self.campoNomeAluno = tk.Entry(janelaAbrirPagamentos, bg="#f4f4f4")
        self.valor = tk.Entry(janelaAbrirPagamentos, bg="#f4f4f4")
        self.tipo = ttk.Combobox(janelaAbrirPagamentos, values=["dinheiro", "cartão"], state="readonly", width=22)
        estilo = ttk.Style()
        estilo.configure('TCombobox', fieldbackground='#f4f4f4')
        self.tipo.set("dinheiro")

        #Formulário: labels
        for label_text, widget in [
            ("ID do Aluno", self.campoId),
            ("Nome do Aluno", self.campoNomeAluno),
            ("Valor (R$)", self.valor),
            ("Tipo de Pagamento", self.tipo)
        ]:
            tk.Label(janelaAbrirPagamentos, text=label_text, bg="white").pack(pady=(10, 2))
            widget.pack(ipadx=5, ipady=3)

        #Formulário: botão
        btnCadastrarPag = tk.Button(
            janelaAbrirPagamentos,
            text="Cadastrar",
            bg="#4CAF50",
            fg="white",
            width=20,
            bd=0,
            relief=tk.FLAT,
            command=self.cadastrarPagamento
        )
        btnCadastrarPag.pack(pady=20)

    #Janela do histórico de pagamentos
    def janelaHistoricoPagamentos(self):
        janela = tk.Toplevel(self.janela)
        janela.title("Histórico de Pagamentos")
        janela.geometry("400x450")
        janela.configure(bg="white")

        estilo = ttk.Style()
        estilo.configure('TCombobox', fieldbackground='#f4f4f4')

        entrada_config = {"bg": "#f4f4f4", "relief": tk.GROOVE, "bd": 2, "font": ("Arial", 12), "width": 25}
        #Formulário
        tk.Label(janela, text="ID Pagamento", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        id_pagamento_entry = tk.Entry(janela, **entrada_config)
        id_pagamento_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(janela, text="ID Aluno", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        id_aluno_entry = tk.Entry(janela, **entrada_config)
        id_aluno_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(janela, text="Data", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        data_entry = tk.Entry(janela, **entrada_config)
        data_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(janela, text="Valor", bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        valor_entry = tk.Entry(janela, **entrada_config)
        valor_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(janela, text="Tipo", bg="white").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tipo_entry = ttk.Combobox(janela, values=["dinheiro", "cartão"], state="readonly", width=23)
        tipo_entry.grid(row=4, column=1, padx=5, pady=5)
        tipo_entry.set("dinheiro")

        #Tabela
        self.treePagamentos = ttk.Treeview(
            janela,
            columns=("ID pagamento", "ID aluno", "Data", "Valor", "Tipo"),
            show="headings"
        )
        for col in self.treePagamentos["columns"]:
            self.treePagamentos.heading(col, text=col)
        self.treePagamentos.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        #Decoração das colunas
        self.treePagamentos.column("ID pagamento", width=60, anchor="center")
        self.treePagamentos.column("ID aluno", width=60, anchor="center")
        self.treePagamentos.column("Data", width=100, anchor="center")
        self.treePagamentos.column("Valor", width=80, anchor="center")
        self.treePagamentos.column("Tipo", width=80, anchor="center")

        #Preencher
        def on_select(event):
            item = self.treePagamentos.selection()
            if item:
                valores = self.treePagamentos.item(item[0], "values")
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

    #========== Métodos do CRUD do pagamento ==========#
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
            data_pagamento = datetime.now()

            if not id_aluno or not valor or not tipo:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            data_formatada = data_pagamento.strftime("%d/%m/%Y")

            self.objetoBanco.cadastrarPagamento(id_aluno, data_formatada, valor, tipo)

            #Calcular nova data de vencimento
            nova_data_vencimento = (data_pagamento + timedelta(days=30)).strftime("%d/%m/%Y")

            #Atualizar aluno: nova data de vencimento e desligamento None
            self.objetoBanco.atualizarMatriculaAposPagamento(id_aluno, nova_data_vencimento)

            messagebox.showinfo("Sucesso","Pagamento cadastrado e matrícula atualizada com sucesso.")

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
