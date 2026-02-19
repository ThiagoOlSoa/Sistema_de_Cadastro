import tkinter as tk
from tkinter import messagebox, simpledialog
import Banco_de_Dados
import cadastro_base
import os

Banco_de_Dados.criar_tabela()

def caixa_cadastro():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Usuários")
    janela_cadastro.geometry("450x500")

    def campo_de_cadastro(texto, senha=False):
        tk.Label(janela_cadastro, text=texto, font=("Arial", 18)).pack()
        e = tk.Entry(janela_cadastro, show="*" if senha else "", width=30, font=("Arial", 14))
        e.pack()
        return e

    nome = campo_de_cadastro("Nome")
    sobrenome = campo_de_cadastro("Sobrenome")
    email = campo_de_cadastro("Email")
    idade = campo_de_cadastro("Idade")
    sexo = campo_de_cadastro("Sexo")
    cpf = campo_de_cadastro("CPF")
    senha = campo_de_cadastro("Senha", senha=True)

    def salvar():
        nome_v = nome.get()
        sobrenome_v = sobrenome.get()
        email_v = email.get()
        idade_v = idade.get()
        sexo_v = sexo.get()
        cpf_v = cpf.get()
        senha_v = senha.get()

        if not nome_v.isalpha():
            messagebox.showerror("Erro!", "Nome Inválido, Digite Apenas Letras!")
            return

        if not sobrenome_v.isalpha():
            messagebox.showerror("Erro!", "Sobrenome Inválido, Digite Apenas Letras!")
            return

        if not cadastro_base.validar_email(email_v):
            messagebox.showerror("Erro!", "E-mail Inválido, Tente Novamente!")
            return

        if not idade_v.isdigit() or not (0 < int(idade_v) <= 120):
            messagebox.showerror("Erro!", "Idade Inválida, Digite uma idade entre 0 e 120 anos!")
            return

        if sexo_v.upper() not in ["M", "F"]:
            messagebox.showerror("Erro!", "Digite apenas M para Masculino ou F para Feminino!")
            return

        if len(cpf_v) != 11 or not cpf_v.isdigit():
            messagebox.showerror("Erro!", "CPF Inválido! Digite apenas os 11 números")
            return

        if Banco_de_Dados.cpf_usado(cpf_v):
            messagebox.showerror("Erro!", "CPF já cadastrado, tente novamente!")
            return

        if not cadastro_base.validar_senha(senha_v):
            messagebox.showerror("Senha Inválida!", "A senha deve conter pelo menos 8 caracteres \n\n"
                    "Também deve conter ao menos 1 letra maiúscula, \n 1 letra minúscula, 1 número e 1 símbolo!")
            return

        dados_usuario = {
            "nome": nome_v,
            "sobrenome": sobrenome_v,
            "email": email_v,
            "idade": idade_v,
            "sexo": sexo_v,
            "cpf": cpf_v,
            "senha": senha_v
        }

        if cadastro_base.usuario_banco(dados_usuario):
            messagebox.showinfo("Sucesso!", "Usuário Cadastrado!")
            janela_cadastro.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao conectar com o banco de Dados!")

    btn_salvar = tk.Button(janela_cadastro, text="Salvar Cadastro", font=("Arial", 15), command=salvar, bg="green", fg="white", width=20)
    btn_salvar.pack(pady=20)


def caixa_lista():
    conteudo = cadastro_base.lista()
    messagebox.showinfo("Lista de Usuários", conteudo)

def caixa_excluir():

    janela_autenticar = tk.Toplevel(janela)
    janela_autenticar.title("Autenticação Necessária!")
    janela_autenticar.geometry("300x250")

    tk.Label(janela_autenticar, text="Digite o CPF do Usuário:", font=("Arial", 14)).pack()
    cpf_ent = tk.Entry(janela_autenticar)
    cpf_ent.pack()

    tk.Label(janela_autenticar, text="Digite a Senha do Usuário:", font=("Arial", 14)).pack()
    senha_ent = tk.Entry(janela_autenticar, show="*")
    senha_ent.pack()

    def confirmar():
        cpf_v = cpf_ent.get().strip()
        senha_v = senha_ent.get().strip()

        usuario = cadastro_base.autenticar_usuario(cpf_v, senha_v)

        if not cpf_v or not senha_v:
            messagebox.showerror("Erro!", "Preencha os 2 campos corretamente!")

        elif usuario:
            messagebox.showinfo("Sucesso", f"Usuário {usuario[1]} autenticado! Pronto para exclusão.")
            exclusao = cadastro_base.excluir_banco(usuario[0])

            if not exclusao:
                messagebox.showerror("Erro!", "Não foi possivel remover o usuário do banco.")
                return

            messagebox.showinfo("Excluído!", "Usuário removido com sucesso!")

            janela_autenticar.destroy()

        else:
            messagebox.showerror("Erro!", "CPF ou Senha Incorretos!")

    tk.Button(janela_autenticar, text="Confirmar", command=confirmar, font=("Arial", 15), bg="green", fg="white").pack(pady=20)

def caixa_editar():
    # cadastro_base.editar()
    janela_editar_aut = tk.Toplevel(janela)
    janela_editar_aut.title("Autenticação para o Menu de Edição do Usuário")
    janela_editar_aut.geometry("400x300")

    tk.Label(janela_editar_aut, text="Digite o CPF do Usuário:", font=("Arial", 18)).pack(pady=10)
    cpf_aut = tk.Entry(janela_editar_aut, font=("Arial", 14))
    cpf_aut.pack(pady=5)

    tk.Label(janela_editar_aut, text="Digite a senha do Usuário:", font=("Arial", 18)).pack(pady=10)
    senha_aut = tk.Entry(janela_editar_aut, font=("Arial", 14), show="*")
    senha_aut.pack(pady=5)

    def autenticar():
        cpf_v = cpf_aut.get()
        senha_v = senha_aut.get()

        usuario = Banco_de_Dados.autenticar(cpf_v, senha_v)

        if usuario:
            janela_editar_aut.destroy()
            menu_edicao(usuario)
        else:
            messagebox.showerror("Erro!", "CPF ou Senha Incorretos!")

    tk.Button(janela_editar_aut, text="Confirmar", command=autenticar, bg="green", fg="white").pack(pady=20)

def menu_edicao(dados_antigos):
    janela_menu = tk.Toplevel(janela)
    janela_menu.title("Menu de Edição do Usuario")
    janela_menu.geometry("450x500")

    def campos_edicao(label, valor_padrao):
        tk.Label(janela_menu, text=label, font=("Arial", 14)).pack()
        ent = tk.Entry(janela_menu)
        ent.insert(0, valor_padrao)
        ent.pack(pady=5)
        return ent

    ent_nome = campos_edicao("Nome", dados_antigos[1])
    ent_sobrenome = campos_edicao("Sobrenome", dados_antigos[2])
    ent_email = campos_edicao("E-mail", dados_antigos[3])
    ent_idade = campos_edicao("Idade", dados_antigos[4])
    ent_cpf = campos_edicao("CPF", dados_antigos[6])

    def salvar_edicao():
        novo_nome = ent_nome.get()
        novo_sobrenome = ent_sobrenome.get()
        novo_email = ent_email.get()
        nova_idade = ent_idade.get()
        novo_cpf = ent_cpf.get()
        id_usuario = dados_antigos[0]

        if not novo_nome.isalpha():
            messagebox.showerror("Erro!", "Nome Inválido, Digite Apenas Letras!")
            return

        if not novo_sobrenome.isalpha():
            messagebox.showerror("Erro!", "Sobrenome Inválido, Digite Apenas Letras!")
            return

        if not cadastro_base.validar_email(novo_email):
            messagebox.showerror("Erro!", "E-mail Inválido, Tente Novamente!")
            return

        if not nova_idade.isdigit() or not (0 < int(nova_idade) <= 120):
            messagebox.showerror("Erro!", "Idade Inválida, Digite uma idade entre 0 e 120 anos!")
            return

        if len(novo_cpf) != 11 or not novo_cpf.isdigit():
            messagebox.showerror("Erro!", "CPF Inválido! Digite apenas os 11 números")
            return

        if novo_cpf != dados_antigos[6] and Banco_de_Dados.cpf_usado(novo_cpf):
            messagebox.showerror("Erro!", "CPF já cadastrado, tente novamente!")
            return

        sucesso = Banco_de_Dados.editar(id_usuario, novo_nome, novo_sobrenome, novo_email, nova_idade, novo_cpf)

        if sucesso:
            messagebox.showinfo("Sucesso!", "Dados alterados com sucesso!")
            janela_menu.destroy()
        else:
            messagebox.showerror("Erro!", "Falha ao alterar informações no Banco!")

    tk.Button(janela_menu, text="Salvar Edição", bg="green", fg="white", font=("Arial", 14), command=salvar_edicao).pack(pady=20)

def admin():
    cpf_adm = "000"
    senha_adm = "ADM123"

    cpf = simpledialog.askstring("Usuário Admin", "Digite o CPF:")

    if cpf is None:
        return

    if cpf == cpf_adm:
        senha = simpledialog.askstring("Usuário Admin", "Digite a Senha:", show="*")
        if senha == senha_adm:
            messagebox.showinfo("Sucesso!", "Usuário Admin autenticado com sucesso!")
            if Banco_de_Dados.exportar_planilha():
                messagebox.showinfo("Sucesso", "Planilha exportada com sucesso!")

                try:
                    os.startfile("Usuarios_Planilha.xlsx")
                except Exception as e:
                    messagebox.showwarning("Aviso!", "Planilha gerada, mas não aberta automaticamente!")
            else:
                messagebox.showerror("Erro!", "Falha ao exportar planilha! Verifique se ela já está aberta")
        else:
            messagebox.showerror("Acesso Negado", "Senha do Admin Inválida!")
    else:
        messagebox.showerror("Acesso Negado", "CPF de Admin Inválido")

def sair():
    janela.destroy()

# Menu Principal
janela = tk.Tk()
janela.title("Sistema de Cadastro de Usuários")
janela.geometry("550x700")

titulo = tk.Label(janela, text="Menu", font=("Arial", 75))
titulo.pack(pady=15)

btn_cadastro = tk.Button(janela, text="Cadastrar Usuário", width=300, font=("Calibri", 20), command=caixa_cadastro)
btn_cadastro.pack(pady=10, padx=70)

btn_listar = tk.Button(janela, text="Listar Usuários", width=300, font=("Calibri", 20), command=caixa_lista)
btn_listar.pack(pady=20, padx=70)

btn_editar = tk.Button(janela, text="Editar Informações do Usuário", width=300, font=("Calibri", 20), command=caixa_editar)
btn_editar.pack(pady=20, padx=70)

btn_excluir = tk.Button(janela, text="Excluir Usuário", width=300, font=("Calibri", 20), command=caixa_excluir)
btn_excluir.pack(pady=20, padx=70)

btn_sair = tk.Button(janela, text="Sair", width=300, font=("Calibri", 20), bg="green", fg="white",command=sair)
btn_sair.pack(pady=20, padx=150)

btn_adm = tk.Button(janela, text="Planilha\n(ADM)", width=30 ,bg="dark green", fg="white", font=("Calibri", 12), command=admin)
btn_adm.pack(pady=5, padx=230)

janela.mainloop()