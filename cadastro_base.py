import Banco_de_Dados
from Banco_de_Dados import buscar_usuarios

def cadastro_novo_usuario(dados):
    sucesso = Banco_de_Dados.inserir_usuario(
        nome=dados["nome"],
        sobrenome=dados["sobrenome"],
        email=dados["email"],
        idade=dados["idade"],
        sexo=dados["sexo"],
        cpf=dados["cpf"],
        senha=dados["senha"]
    )

    if sucesso:
        print("Sucesso! Usuário salvo!")
        return True
    else:
        print("Erro! Falha ao salvar Usuário!")
        return False

def  validar_email(email):
    #Função para Validação de e-mail

    if "@" in email and "." in email:
        return True
    else:
        return False

def usuario_banco(dados):
    # Função para salvar o usuário no banco

    salvo = Banco_de_Dados.inserir_usuario(
        dados["nome"],
        dados["sobrenome"],
        dados["email"],
        dados["idade"],
        dados["sexo"],
        dados["cpf"],
        dados["senha"]
    )
    return salvo

def lista():
    #Função para listar os usuários e algumas informações
    usuarios = buscar_usuarios()

    if not usuarios:
        return "Nenhum Usuário Cadastrado!"

    relatorio = "Lista de Usuários:\n"
    for u in usuarios:
        relatorio += f"\nNome: {u[0]} {u[1]}\n Email: {u[2]}\n Idade: {u[3]}\n Sexo: {u[4]}\n CPF: {u[5]}\n"
        relatorio += "-"*30
    return relatorio

def autenticar_usuario(cpf, senha):
    #Função de autenticação de usuário para uso posterior para excluir/editar informações
    return Banco_de_Dados.autenticar(cpf, senha)

def excluir_banco(id_usuario):
    excluido = Banco_de_Dados.excluir(id_usuario)
    return excluido