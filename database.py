import sqlite3
class AppBd():
    def __init__(self):
        self.create_table()
    #Conexão
    def abrirconexao(self):
        try:
            self.connect = sqlite3.connect("db/database.db")
            self.connect.execute("PRAGMA foreign_keys = ON;")
        except sqlite3.Error as erro:
            print("Falha ao se conectar ao banco de dados:", erro)
    #Criando tabelas aluno e pagamento
    def create_table(self):
        self.abrirconexao()
        create_table_aluno_query = """CREATE TABLE IF NOT EXISTS aluno(
                                        id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
                                        nome TEXT NOT NULL,
                                        endereco TEXT NOT NULL,
                                        cidade TEXT NOT NULL,
                                        estado TEXT NOT NULL,
                                        telefone TEXT NOT NULL,
                                        data_matricula TEXT,
                                        data_desligamento TEXT,
                                        data_vencimento TEXT);
                                   """

        create_table_pagamento_query = """CREATE TABLE IF NOT EXISTS pagamento(
                                            id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
                                            id_aluno INTEGER NOT NULL,
                                            data TEXT NOT NULL,
                                            valor REAL NOT NULL,
                                            tipo TEXT NOT NULL CHECK (tipo IN ('dinheiro', 'cartão')),
                                            FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno));
                                       """
        try:
            cursor = self.connect.cursor()
            cursor.execute(create_table_aluno_query)
            cursor.execute(create_table_pagamento_query)
        except sqlite3.Error as erro:
            print(f"Falha ao criar tabelas: {erro}")
        finally:
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexão com o SQLite foi fechada.")
    #========== Métodos do CRUD do aluno ==========#
    #Insert
    def cadastrarAluno(self, nome, endereco, cidade, estado, telefone, data_matricula, data_desligamento, data_vencimento):
        self.abrirconexao()
        insert_query = """INSERT INTO aluno
          (nome, endereco, cidade, estado, telefone, data_matricula, data_desligamento, data_vencimento) VALUES (?, ?,?, ?,?, ?,?, ?)"""
        try:
            cursor = self.connect.cursor()
            cursor.execute(insert_query, (nome, endereco, cidade, estado, telefone, data_matricula, data_desligamento, data_vencimento))
            print("Aluno cadastrado com sucesso!!")
            self.connect.commit()
        except sqlite3.Error as erro:
            print("Falha ao inserir aluno")
        finally:
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexao com o sqlite foi fechada!!")
    #Select
    def selecionarAlunos(self):
        self.abrirconexao()
        select_query = """SELECT * FROM aluno"""
        products = []
        try:
            cursor = self.connect.cursor()
            cursor.execute(select_query)
            products = cursor.fetchall() 
        except  sqlite3.Error as error:
                print("Falha ao retornar alunos", error)
        finally:
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexao com o sqlite foi fechada")
        return products
    #Update
    def atualizarAluno(self, id_aluno, nome, endereco, cidade, estado, telefone, dataMatricula, dataDesligamento, dataVencimento):
        self.abrirconexao()
        update_query = """UPDATE aluno SET nome = ?, endereco = ?, cidade = ?, estado = ?, telefone = ?, data_matricula = ?, data_desligamento = ?, data_vencimento = ? 
        WHERE id_aluno = ?"""
        try:
            cursor = self.connect.cursor()
            cursor.execute(update_query, (nome, endereco, cidade, estado, telefone, dataMatricula, dataDesligamento, dataVencimento, id_aluno))
            self.connect.commit()
            print("Aluno atualizado com sucesso")
        except sqlite3.Error as error:
            print("Falha ao atualizar o aluno",error)
        finally:    
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexão com o sqlite foi fechada.")
    #Delete
    def deletarAluno(self, id):
        self.abrirconexao()
        delete_query = """DELETE FROM aluno WHERE id_aluno=?"""
        try:
            cursor = self.connect.cursor()
            cursor.execute(delete_query, (id,))
            self.connect.commit()
        except sqlite3.Error as error:
            print("Falha ao deletar aluno")
        finally:    
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexão com o sqlite foi fechada.")
    #========== Métodos do CRUD do pagamento ==========#
    #Create do pagamento
    def cadastrarPagamento(self, id_aluno, data, valor, tipo):
        self.abrirconexao()
        insert_query = """INSERT INTO pagamento (id_aluno, data, valor, tipo)
                        VALUES (?, ?, ?, ?)"""
        try:
            cursor = self.connect.cursor()
            cursor.execute(insert_query, (id_aluno, data, valor, tipo))
            print("Pagamento cadastrado com sucesso!")
            self.connect.commit()
        except sqlite3.Error as erro:
            print("Falha ao cadastrar pagamento:", erro)
        finally:
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexão com o SQLite foi fechada.")
    #Select
    def selecionarPagamentos(self):
        self.abrirconexao()
        select_query = """SELECT * FROM pagamento"""
        products = []
        try:
            cursor = self.connect.cursor()
            cursor.execute(select_query)
            products = cursor.fetchall() 
        except  sqlite3.Error as error:
                print("Falha ao retornar pagamentos", error)
        finally:
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexao com o sqlite foi fechada")
        return products
    #Atulizar desligamento e vencimento após pagar
    def atualizarMatriculaAposPagamento(self, id_aluno, nova_data_vencimento):
        self.abrirconexao()
        update_query = """UPDATE aluno SET data_vencimento = ?, data_desligamento = NULL WHERE id_aluno = ?"""
        try:
            cursor = self.connect.cursor()
            cursor.execute(update_query, (nova_data_vencimento, id_aluno))
            self.connect.commit()
            print("Matrícula atualizada após pagamento com sucesso")
        except sqlite3.Error as error:
            print("Erro ao atualizar matrícula após pagamento:", error)
        finally:
            if self.connect:
                cursor.close()
                self.connect.close()
                print("A conexão com o sqlite foi fechada.")