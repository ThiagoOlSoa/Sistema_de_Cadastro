import tkinter as tk
from tkinter import messagebox, simpledialog

from attr.setters import validate

import Banco_de_Dados
import cadastro_base
import os

Banco_de_Dados.criar_tabela()

def caixa_cadastro():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Usuários")
    janela_cadastro.geometry("450x650")

    def campo_de_cadastro(texto_label, validacao, senha=False):
        tk.Label(janela_cadastro, text=texto_label, font=("Arial", 12, "bold")).pack(pady=(5, 0))
        texto =  tk.StringVar()
        entrada = tk.Entry(janela_cadastro, textvariable=texto, show="*" if senha else "", width=30, font=("Arial", 12))
        entrada.pack()
        aviso = tk.Label(janela_cadastro, text="", font=("Arial", 9))
        aviso.pack()

        def processar(*args):
            valor = texto.get()
            mensagem, cor = validacao(valor)
            aviso.config(text=mensagem, fg=cor)

        texto.trace_add("write", processar)
        return texto

    def validacao_nome(valor):
        limpo = valor.replace(" ", "")
        if not valor: return "", "black"
        if limpo.isalpha() and len(limpo) > 1: return "✔ OK!", "green"
        return "⚠ Digite apenas letras!", "red"

    def validacao_email(valor):
        if not valor: return "", "black"
        if cadastro_base.validar_email(valor): return "✔ E-mail Válido!", "green"
        return "⚠ E-mail Inválido, tente novamente!", "red"

    def validacao_idade(valor):
        if not valor: return "", "black"
        if valor.isdigit() and 0 < int(valor) < 130: return "✔ Idade Válida!", "green"
        return "⚠ Digite um número entre 1 e 130!", "red"

    def validacao_cpf(valor):
        if not valor: return "", "black"
        if not valor.isdigit(): return "⚠ Digite apenas números!", "red"
        if len(valor) < 11: return f"⚠ Faltam {11 - len(valor)} números!", "orange"
        if len(valor) > 11: return "⚠ CPF Inválido, passou de 11 digitos!", "red"
        if Banco_de_Dados.cpf_usado(valor): return "⚠ CPF já Cadastrado, tente novamente!", "red"
        return "✔ CPF válido", "green"

    def validacao_senha(valor):
        if not valor: return "", "black"
        if len(valor) < 8: return "⚠ Digite no mínimo 8 caracteres!", "red"
        if not any(c.isupper()for c in valor): return "⚠ Precisa conter pelo menos 1 letra maiúscula!", "red"
        if not any(c.islower() for c in valor): return "⚠ Precisa conter pelo menos 1 letra minúscula", "red"
        if not any(c.isdigit() for c in valor): return "⚠ Precisa conter pelo menos 1 número", "red"
        if not any(not c.isalnum() for c in valor): return "⚠ Precisa conter pelo menos 1 símbolo (@, #, etc)", "red"
        return "✔ Senha forte!", "green"

    nome = campo_de_cadastro("Nome", validacao_nome)
    sobrenome = campo_de_cadastro("Sobrenome", validacao_nome)
    email = campo_de_cadastro("Email", validacao_email)
    idade = campo_de_cadastro("Idade", validacao_idade)
    cpf = campo_de_cadastro("CPF", validacao_cpf)
    senha = campo_de_cadastro("Senha", validacao_senha,senha=True)

    tk.Label(janela_cadastro, text="Sexo", font=("Arial", 12, "bold")).pack(pady=(10, 0))
    sexo = tk.StringVar(value="")
    frame_sexo = tk.Frame(janela_cadastro)
    frame_sexo.pack(pady=5)

    botao_sexo = {
        "variable": sexo,
        "font": ("Arial", 12),
        "width": 5,
        "selectcolor": "#AED6F1",
        "pady": 5,
        "padx": 10
    }

    rb_m = tk.Radiobutton(frame_sexo, text="Masculino", value="Masculino", **botao_sexo)
    rb_m.pack(side="left", padx=5)
    rb_f = tk.Radiobutton(frame_sexo, text="Feminino", value="Feminino", **botao_sexo)
    rb_f.pack(side="left", padx=5)
    label_sexo = tk.Label(janela_cadastro, text="⚠ Selecione uma opção!", fg="red", font=("Arial", 9))
    label_sexo.pack()

    def atualizar(*args):
        if sexo.get() != "":
            label_sexo.config(text="✔ Opção selecionada", fg="green")

    sexo.trace_add("write", atualizar)

    def salvar():
        nome_v = nome.get().strip()
        sobrenome_v = sobrenome.get().strip()
        email_v = email.get().strip()
        idade_v = idade.get()
        sexo_v = sexo.get()
        cpf_v = cpf.get()
        senha_v = senha.get()

        validacao_sexo = (sexo_v in ["Masculino", "Feminino"])

        if (validacao_nome(nome_v)[1] == "green" and
            validacao_nome(sobrenome_v)[1] == "green" and
            validacao_email(email_v)[1] == "green" and
            validacao_idade(idade_v)[1] == "green" and
            validacao_sexo and
            validacao_cpf(cpf_v)[1] == "green" and
            validacao_senha(senha_v)[1] == "green"):

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
                messagebox.showerror("Erro", "Erro ao Salvar no banco de Dados!")
        else:
            if not validacao_sexo:
                label_sexo.config(text="⚠ Escolha o sexo para continuar!", fg="red")
            messagebox.showwarning("Atenção", "Existem campos incorretos ou vazios!\nPor favor, corrija o que precisa para salvar!")

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
    janela_menu.title("Editar Usuário")
    janela_menu.geometry("450x550")

    def campos_edicao(label, validacao, valor_inicial, senha=False):
        tk.Label(janela_menu, text=label, font=("Arial", 12, "bold")).pack(pady=(5, 0))
        texto = tk.StringVar(value=valor_inicial)
        entrada = tk.Entry(janela_menu, textvariable=texto, font=("Arial", 12), show="*" if senha else "", width=30)
        entrada.pack()
        aviso = tk.Label(janela_menu, text="✔ Dado atual carregado", fg="green", font=("Arial", 9))
        aviso.pack()

        def processar(*args):
            valor = texto.get()
            mensagem, cor = validacao(valor)
            aviso.config(text=mensagem, fg=cor)

        texto.trace_add("write", processar)
        return texto

    def validacao_nome(valor):
        limpo = valor.replace(" ", "")
        if not valor: return "⚠ Campo obrigatório", "red"
        if limpo.isalpha(): return "✔ OK!", "green"
        return "⚠ Digite apenas letras!", "red"

    def validacao_email(valor):
        if cadastro_base.validar_email(valor): return "✔ E-mail Válido!", "green"
        return "⚠ E-mail Inválido!", "red"

    def validacao_idade(valor):
        if valor.isdigit() and 0 < int(valor) < 130: return "✔ Idade Válida!", "green"
        return "⚠ Digite um número entre 1 e 130!", "red"

    def validacao_cpf(valor):
        if not valor.isdigit(): return "⚠ Apenas números!", "red"
        if len(valor) != 11: return "⚠ CPF precisa de 11 números", "red"
        if valor != str(dados_antigos[6]) and Banco_de_Dados.cpf_usado(valor):
            return "⚠ Este CPF pertence a outro usuário!", "red"
        return "✔ CPF válido", "green"

    id_usuario =dados_antigos[0]
    ent_nome = campos_edicao("Nome", validacao_nome, dados_antigos[1])
    ent_sobrenome = campos_edicao("Sobrenome", validacao_nome, dados_antigos[2])
    ent_email = campos_edicao("Email", validacao_email, dados_antigos[3])
    ent_idade = campos_edicao("Idade", validacao_idade, dados_antigos[4])
    ent_cpf = campos_edicao("CPF", validacao_cpf, dados_antigos[6])

    tk.Label(janela_menu, text="Sexo", font=("Arial", 12, "bold")).pack(pady=(10, 0))
    sexo = tk.StringVar(value=dados_antigos[5])
    frame_sexo = tk.Frame(janela_menu)
    frame_sexo.pack(pady=5)

    botao_sexo = {
        "variable": sexo,
        "font": ("Arial", 12),
        "width": 5,
        "selectcolor": "#AED6F1",
        "pady": 5,
        "padx": 10
    }

    tk.Radiobutton(frame_sexo, text="Masculino", value="Masculino", **botao_sexo).pack(side="left", padx=5)
    tk.Radiobutton(frame_sexo, text="Feminino", value="Feminino", **botao_sexo).pack(side="left", padx=5)


    def salvar_edicao():
        novo_nome = ent_nome.get().strip()
        novo_sobrenome = ent_sobrenome.get().strip()
        novo_email = ent_email.get().strip()
        nova_idade = ent_idade.get()
        novo_cpf = ent_cpf.get()

        if (validacao_nome(novo_nome)[1] == "green" and
            validacao_nome(novo_sobrenome)[1] == "green" and
            validacao_email(novo_email)[1] == "green" and
            validacao_idade(nova_idade)[1] == "green" and
            validacao_cpf(novo_cpf)[1] == "green"):

            sucesso = Banco_de_Dados.editar(id_usuario, novo_nome, novo_sobrenome, novo_email, nova_idade, novo_cpf)

            if sucesso:
                messagebox.showinfo("Sucesso!", "Dados atualizados com sucesso!")
                janela_menu.destroy()

            else:
                messagebox.showerror("Erro!", "Falha ao alterar informações no Banco!")

        else:
            messagebox.showwarning("Atenção", "Verifique se todos os campos estão corretos!")

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