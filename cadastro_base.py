import Banco_de_Dados
from Banco_de_Dados import buscar_usuarios

#Antiga lista de Usuários -> usuarios = []

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

def validar_senha(senha):
    #Função para Validação da senha

    maiuscula = False
    minuscula = False
    numero = False
    simbolo = False

    for c in senha: #Validação de obrigatoriedades da senha
        if c.isupper():
            maiuscula = True
        elif c.islower():
            minuscula = True
        elif c.isdigit():
            numero = True
        elif not c.isalnum():
            simbolo = True

    if maiuscula and minuscula and numero and simbolo and len(senha) >= 8:
        return True
    else:
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

#
            # def usuarios_campos():
            #     #Função principal dos campos de cadastro dos usuários
            #
            #     while True: #Verificação do Nome
            #         nome = input("\nDigite o nome do Usuário: ")
            #         if nome.isalpha():
            #             break
            #         else:
            #             print("Digite apenas letras!")
            #     while True: #Verificação do Sobrenome
            #         sobrenome = input("\nDigite o Sobrenome do Usuário: ")
            #         if sobrenome.isalpha():
            #             break
            #         else:
            #             print("Digite apenas letras!")
            #     while True: #Uso da verificação do e-mail
            #         email = input("\nDigite o e-mail do Usuário: ").lower()
            #         if validar_email(email):
            #             break
            #     while True: #validação da Idade
            #         try:
            #             idade = int(input("\nDigite a idade do Usuário: "))
            #             if 0 < idade <= 120:
            #                 break
            #             else:
            #                 print("Digite uma idade valida! Entre 1 e 120 anos!")
            #         except ValueError:
            #             print("Dgite apenas Números!")
            #             continue
            #     while True: #Validação do Sexo
            #         sexo = input("\nDigite o sexo do Usuário (F para Feminino ou M para Masculino): ").upper()
            #         if sexo == "F" or sexo == "M":
            #             break
            #         else:
            #             print("Digite Somente F ou M para feminino ou masculino!")
            #     while True: #Validação do CPF
            #         cpf = input("\nDigite o CPF do Usuário: ")
            #         if len(cpf) == 11 and cpf.isdigit():
            #             cpf2 = False # Variável de controle
            #             for u in usuarios: # Verificação de duplicidade do CPF
            #                 if u["cpf"] == cpf:
            #                     print("CPF ja cadastrado!")
            #                     cpf2 = True
            #                     break
            #             if not cpf2:
            #                 break
            #         else:
            #             print("CPF Inválido! Digite apenas 11 Números!")
            #     while True:  #Uso da validação da Senha
            #         senha = input("\nDigite a senha do Usuário: ")
            #         if validar_senha(senha):
            #              break
            #
            #     usuario = {
            #         "nome": nome,
            #         "sobrenome": sobrenome,
            #         "email": email,
            #         "idade": idade,
            #         "sexo": sexo,
            #         "cpf": cpf,
            #         "senha": senha
            #     }
            #     return usuario
            #
            # def cadastro():
            #     #Função para puxar o cadastro de usuários
            #
            #     print("\nCadastro de Usuário")
            #     usuario = usuarios_campos()
            #     usuarios.append(usuario)
            #     print("Usuário Cadastrado Com Sucesso!")
            #
            # def editar():
            #     print("Editar Usuário")
            #
            #     usuario = autenticar_usuario()
            #
            #     if usuario:
            #         print("Usuário autenticado com Sucesso!")
            #
            #         def menu_edicao():
            #
            #             def editar_nome():
            #                 while True:  # Verificação do novo Nome
            #                     novo_nome = input("Digite o Novo Nome: ")
            #                     if novo_nome.isalpha():
            #                         usuario["nome"] = novo_nome
            #                         break
            #                     else:
            #                         print("Digite apenas letras!")
            #             def editar_sobrenome():
            #                 while True:  # Verificação do Sobrenome
            #                     novo_sobrenome = input("Digite o Novo Sobrenome: ")
            #                     if novo_sobrenome.isalpha():
            #                         usuario["sobrenome"] = novo_sobrenome
            #                         break
            #                     else:
            #                         print("Digite apenas letras!")
            #             def editar_email():
            #                 while True:
            #                     novo_email = input("Digite o Novo Email: ").lower()
            #                     if validar_email(novo_email):
            #                         usuario["email"] = novo_email
            #                         break
            #             def editar_idade():
            #                 while True:  # validação da nova Idade
            #                     try:
            #                         nova_idade = int(input("Digite a Nova idade: "))
            #                         if 0 < nova_idade <= 120:
            #                             usuario["idade"] = nova_idade
            #                             break
            #                         else:
            #                             print("Digite uma idade valida! Entre 1 e 120 anos!")
            #                     except ValueError:
            #                         print("Dgite apenas Números!")
            #                         continue
            #             def editar_sexo():
            #                 while True:  # Validação do Novo Sexo
            #                     novo_sexo = input("Digite o Novo Sexo (F para Feminino ou M para Masculino): ").upper()
            #                     if novo_sexo == "F" or novo_sexo == "M":
            #                         usuario["sexo"] = novo_sexo
            #                         break
            #                     else:
            #                         print("Digite Somente F ou M para feminino ou masculino!")
            #             def editar_cpf():
            #                 while True: # Validação do Novo CPF
            #                     novo_cpf = input("Digite o Novo CPF: ")
            #                     if len(novo_cpf) == 11 and novo_cpf.isdigit():
            #                         usuario["cpf"] = novo_cpf
            #                         break
            #                     else:
            #                         print("CPF Inválido! Digite apenas 11 Números!")
            #             def editar_senha():
            #                 while True:
            #                     nova_senha = input("Digite a Nova Senha: ")
            #                     if validar_senha(nova_senha):
            #                         usuario["senha"] = nova_senha
            #                         break
            #             def editar_cancelar():
            #                 print("Edição cancelada, Retornando ao menu principal!")
            #
            #
            #
            #             menu_editar = [
            #                 "Editar Nome do Usuário       |",
            #                 "Editar Sobrenome do Usuário  |",
            #                 "Editar E-mail do Usuário     |",
            #                 "Editar Idade do Usuário      |",
            #                 "Editar Sexo do Usuário       |",
            #                 "Editar CPF do Usuário        |",
            #                 "Editar Senha do Usuário      |",
            #                 "Cancelar Edição de Usuário   |",
            #             ]
            #
            #             while True:
            #                 print("\n|-----------MENU DE EDIÇÃO-----------|")
            #
            #                 for i, opcao_editar in enumerate(menu_editar, start=1):
            #                     print(f"| [{i}] - {opcao_editar}")
            #
            #                 print("|------------------------------------|")
            #
            #                 try:
            #                     opc = int(input("\nDigite sua opção: "))
            #                 except ValueError:
            #                     print("Digite apenas números!")
            #                     continue
            #                 if opc == 1:
            #                     editar_nome()
            #                 elif opc == 2:
            #                     editar_sobrenome()
            #                 elif opc == 3:
            #                     editar_email()
            #                 elif opc == 4:
            #                     editar_idade()
            #                 elif opc == 5:
            #                     editar_sexo()
            #                 elif opc == 6:
            #                     editar_cpf()
            #                 elif opc == 7:
            #                     editar_senha()
            #                 elif opc == 8:
            #                     editar_cancelar()
            #                     break
            #                 else:
            #                     invalido()
            #
            #         menu_edicao()
            #         #continuar tabela para saber o que deseja editar
            #
            # def encerrar():
            #     print("\nEncerrando o programa...")
            #
            # def invalido():
            #     print("\nOpção Inválida! Tente novamente!")
