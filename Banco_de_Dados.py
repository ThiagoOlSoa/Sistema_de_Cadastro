import os
import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

basedir = os.path.dirname(os.path.abspath(__file__))
Banco_Cadastros = os.path.join(basedir, "Banco_de_Dados.db")

def criar_tabela():
    # Cria a tabela de Usuários se ela nao existir
    with sqlite3.connect(Banco_Cadastros) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                email TEXT NOT NULL,
                idade INTEGER NOT NULL,
                sexo TEXT NOT NULL,
                cpf TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        conn.commit()
    print("Banco de dados criado/verificado com sucesso!")

def inserir_usuario(nome, sobrenome, email, idade, sexo, cpf, senha):
    # Função para inserir um novo usuário no banco de dados
    try:
        with sqlite3.connect(Banco_Cadastros) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nome, sobrenome, email, idade, sexo, cpf, senha)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, sobrenome, email, idade, sexo, cpf, senha))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Erro ao inserir Usuário: {e}")
        return False

def buscar_usuarios():
    with sqlite3.connect(Banco_Cadastros) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nome, sobrenome, email, idade, sexo, cpf FROM usuarios")
        return cursor.fetchall()

def autenticar(cpf, senha):
    with sqlite3.connect(Banco_Cadastros) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE cpf=? AND senha = ?", (cpf, senha))
        return cursor.fetchone()

def excluir(id_usuario):
    with sqlite3.connect(Banco_Cadastros) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conn.commit()
        return True

def cpf_usado(cpf):
    with sqlite3.connect(Banco_Cadastros) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cpf = ?", (cpf,))
        resultado = cursor.fetchone()[0]
        return resultado > 0

def editar(id_usuario, nome, sobrenome, email, idade, cpf):
    try:
        with sqlite3.connect(Banco_Cadastros) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuarios 
                SET nome = ?, sobrenome = ?, email = ?, idade = ?, cpf = ?
                WHERE id = ?
                """, (nome, sobrenome, email, idade, cpf, id_usuario))
            conn.commit()
            return True
    except sqlite3.Error:
        return False

def exportar_planilha():
    try:
        with sqlite3.connect(Banco_Cadastros) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            dados = cursor.fetchall()

            wb = Workbook()
            ws = wb.active
            ws.title = "Planilha de Usuários"

            colunas = ["ID do Usuário", "Nome", "Sobrenome", "Email", "Idade", "Sexo", "Cpf", "Senha"]
            ws.append(colunas)

            for  linha in dados:
                ws.append(linha)

            negrito = Font(bold=True)
            alinhamento = Alignment(horizontal='left', vertical='center')

            for linha_celulas in ws.iter_rows():
                for celula in linha_celulas:
                    celula.alignment = alinhamento

                    if celula.row == 1:
                        celula.font = negrito

            for col in ws.columns:
                max_length = 0
                coluna = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[coluna].width = adjusted_width

            wb.save("Usuarios_Planilha.xlsx")
            return True

    except Exception as e:
        print(f"Erro: {e}")
        return False


        #Código usado antes
        # def exportar_planilha():
        #     try:
        #         with sqlite3.connect(Banco_Cadastros) as conn:
        #             cursor = conn.cursor()
        #             cursor.execute("SELECT * FROM usuarios")
        #             dados = cursor.fetchall()
        #
        #             with open("planilha_usuarios.csv", "w", newline='', encoding='utf-8-sig') as arquivo:
        #                 escrever = csv.writer(arquivo, delimiter= ';')
        #                 escrever.writerow(["ID do Usuario", "Nome", "Sobrenome", "Email", "Idade", "Sexo", "Cpf", "Senha"])
        #                 escrever.writerows(dados)
        #
        #         return True
        #     except Exception as e:
        #         print(f"Erro ao exportar: {e}")
        #         return False
