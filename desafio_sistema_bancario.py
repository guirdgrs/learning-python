menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


print ("Bem-vindo(a) ao sistema bancário!")
print ("\nSelecione a operação desejada:")  

while True:

    opcao = input(menu)

    #Depósito
    if opcao == "d":

        #Mostrando o saldo atual
        print(f"\nSeu saldo atual é de R${saldo:.2f}")

        valor = float(input("\nDigite o valor a ser depositado: "))

        #Verifica se o valor a ser depositado é um número válido
        if valor > 0:
            #Realiza o depósito somando o valor ao saldo
            saldo += valor
            #Adiciona o depósito ao extrato
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! Por favor, digite um valor válido.")

    #Saque
    if opcao == "s":

        #Mostrando o valor limite de saque
        print("O limite para saque é de R$500.00")

        #Mostrando o saldo atual
        print(f"\nSeu saldo atual é de R${saldo:.2f}")

        valor = float(input("\nDigite o valor a ser sacado: "))

        #Vericia se o valor a ser sacado é maior que o saldo disponível
        if valor > saldo:
            print("Operação falhou! O saldo é insuficiente.")

        #Verifica se o valor a ser sacado é maior que o limite estabelecido
        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")

        #Verifica se o número de saques atingiu o limite diário
        elif numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")

        #Se todas as verificações forem verdadeiras, realiza o saque
        else:
            #Subtrai o valor do saque do saldo
            saldo -= valor
            #Adiciona o saque ao extrato
            extrato += f"Saque: R$ {valor:.2f}\n"
            #Incrementa o número de saques para controle de limite
            numero_saques += 1

    #Extrato
    if opcao == "e":
        print(" EXTRATO ".center(40, "="))

        #Verifica se o extrato está vazio
        if extrato == "":
            print("Não foram realizadas movimentações na sua conta.")
        else:
            print(extrato)

        print(f"\nSaldo: R$ {saldo:.2f}")
        print("".center(40, "="))
        
    #Sair
    if opcao == "q":
        break

else: 
    print("Operação inválida, por favor selecione uma operação válida.")