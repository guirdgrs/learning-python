saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

#Arrays para armazenar os usuários e contas correntes
usuarios = []
contas_correntes = []


print ("Bem-vindo(a) ao sistema bancário!")
print ("\nSelecione a operação desejada:")  

def menu():
    menu = """

[c] Cadastrar Usuário
[l] Listar Usuários
[cc] Criar Conta Corrente
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """
    return input(menu)

#Função para realizar o saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    #Verifica se o valor a ser sacado é maior que o saldo disponível
    if valor > saldo:
        print("Operação falhou! O saldo é insuficiente.")

    #Verifica se o valor a ser sacado é maior que o limite estabelecido
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")

    #Verifica se o número de saques atingiu o limite diário
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    #Se todas as verificações forem verdadeiras, realiza o saque
    else:
        #Subtrai o valor do saque do saldo
        saldo -= valor
        #Adiciona o saque ao extrato
        extrato += f"Saque: R$ {valor:.2f}\n"
        #Incrementa o número de saques para controle de limite
        numero_saques += 1

    return saldo, extrato

#Função para realizar o depósito
def depositar(saldo, valor, extrato, /):

    #Verifica se o valor a ser depositado é um número válido
    if valor > 0:
        #Realiza o depósito somando o valor ao saldo
        saldo += valor
        #Adiciona o depósito ao extrato
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! Por favor, digite um valor válido.")

    return saldo, extrato

#Função para mostrar o extrato
def mostrar_extrato(saldo, /, *, extrato):
    #Obs: o nome da função foi alterado de extrato() para mostrar_extrato() 
    # devido ao erro de colisão com o argumento extrato.
    
    #Verifica se o extrato está vazio
    if extrato == "":
        print("Não foram realizadas movimentações na sua conta.")
    else:
        print(extrato)

    print(f"\nSaldo: R$ {saldo:.2f}")
    print("".center(40, "="))

    return extrato

#Função para cadastrar usuário
def cadastrar_usuario(usuarios):

    print("\nCadastrar Usuário")

    cpf = input("Digite o CPF do titular da conta: ")

    #Verifica se o CPF ja foi cadastrado
    if cpf in [usuario["cpf"] for usuario in usuarios]:
        print("\nCPF ja cadastrado!")
        return None

    nome = input("Digite o nome do titular da conta: ")
    data_de_nascimento = input("Digite a data de nascimento do titular da conta: ")
    
    print("\nEndereço do titular da conta:")

    logradouro = input("Digite o logradouro: ")
    numero = input("Digite o número do endereço: ")
    bairro = input("Digite o bairro: ")
    cidade = input("Digite a cidade: ")
    uf = input("Digite a UF: ")

    #Armazena os dados do usuário em um dicionário
    usuario = {
        "nome": nome,
        "data_de_nascimento": data_de_nascimento,

        #Remove os caracteres especiais do CPF para armazenar apenas os números
        "cpf": cpf.replace(".", "").replace("-", ""),

        "endereco": {
            "logradouro": logradouro,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "uf": uf
        }
    }

    #Adiciona o usuário ao array
    usuarios.append(usuario)

    return usuarios

#Função para listar usuários
def listar_usuarios(usuarios):

    #Verifica se algum usuário foi cadastrado
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    #Mostra todos os usuários
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}")
        print(f"Data de Nascimento: {usuario['data_de_nascimento']}")
        print(f"CPF: {usuario['cpf']}")
        print("".center(40, "="))

    return usuarios

#Função para criar uma conta corrente
def criar_conta_corrente(usuarios, conta_corrente):

    print("\nCriar Conta Corrente")

    #Verifica se algum usuário foi cadastrado
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    
    #Input para cadastrar o titular da conta a uma conta corrente
    cpf = input("\nDigite o CPF do titular da conta corrente: ")

    #usuario_encontrado é utilizado para armazenar o titular da conta corrente
    usuario_encontrado = None

    #Verifica se o CPF do titular da conta corrente foi encontrado
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            #Armazena o titular da conta corrente
            usuario_encontrado = usuario
            break

    #Caso o CPF do titular da conta corrente nao seja encontrado
    if not usuario_encontrado:
        print("CPF do titular da conta corrente não encontrado.")
        return contas_correntes
    
    #Valores padrão
    numero_conta = len(contas_correntes) + 1 #Incrementa o número da conta
    AGENCIA = "0001"

    #Armazena a conta corrente
    conta_corrente = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario_encontrado
    }

    contas_correntes.append(conta_corrente)

    print(f"\nConta corrente criada com sucesso!")
    print(f"\nAgência: {conta_corrente['agencia']}")
    print(f"Conta: {conta_corrente['numero_conta']}")
    print(f"Titular: {conta_corrente['usuario']['nome']}")
    print("".center(40, "="))

    return contas_correntes

while True:

    opcao = menu()

    #Cadastrar usuário
    if opcao == "c":
        cadastrar_usuario(usuarios)

    #Listar usuários
    if opcao == "l":
        listar_usuarios(usuarios)

    #Criar Conta Corrente
    if opcao == "cc":
        criar_conta_corrente(usuarios, contas_correntes)

    #Depósito
    if opcao == "d":

        #Mostrando o saldo atual
        print(f"\nSeu saldo atual é de R${saldo:.2f}")

        valor = float(input("\nDigite o valor a ser depositado: "))

        #Realiza o depósito através da função
        saldo, extrato = depositar(saldo, valor, extrato)

    #Saque
    if opcao == "s":

        #Mostrando o valor limite de saque
        print("O limite para saque é de R$500.00")

        #Mostrando o saldo atual
        print(f"\nSeu saldo atual é de R${saldo:.2f}")

        valor = float(input("\nDigite o valor a ser sacado: "))

        #Realiza o saque através da função
        saldo, extrato = sacar(saldo=saldo, 
                               valor=valor, 
                               extrato=extrato, 
                               limite=limite, 
                               numero_saques=numero_saques, 
                               limite_saques=LIMITE_SAQUES)
        

    #Extrato
    if opcao == "e":
        print(" EXTRATO ".center(40, "="))

        #Realiza o extrato através da função
        mostrar_extrato(saldo, extrato=extrato)
        
    #Sair
    if opcao == "q":
        break

else: 
    print("Operação inválida, por favor selecione uma operação válida.")