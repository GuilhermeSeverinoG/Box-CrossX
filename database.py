import sqlite3
class AppBd():
    def __init__(self):
        self.create_table()
    #Abindo conexão com o banco
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
AppBd()