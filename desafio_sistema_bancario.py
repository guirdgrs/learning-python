from abc import ABC, abstractmethod
from datetime import datetime


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

class Conta:    

    # _nome para indicar que o atributo é privado

    def __init__(self, numero, cliente):
        #Valores padrão
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"

        self._cliente = cliente
        #Historico é instanciado na classe Historico
        self._historico = Historico()


    #@property é usado para criar um 'getter' que irá retornar os valores
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historic(self):
        return self._historico

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    #Método para sacar
    def sacar(self, valor):

        if valor > self.saldo:
            print("Operação falhou! O saldo é insuficiente.")
            return False

        elif valor < 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        else:
            print("Operação realizada com sucesso!")
            self._saldo -= valor
            return True

    #Método para depositar
    def depositar(self, valor):

        if valor < 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        else:
            print("Operação realizada com sucesso!")
            self._saldo += valor
            return True

#Iterador de contas
class ContaIterador:
    #Como parâmetro recebe contas
    def __init__(self, contas):
        self.contas = contas

        #Index é usado para percorrer o array
        self._index = 0
    
    def __iter__(self):
        pass

    def __next__(self):
        try:
            #Pega a conta do index
            conta = self.contas[self._index]

            #Retorna a conta e os valores
            return f"""\
            Agência: {conta.agencia}
            Número: {conta.numero}
            Proprietário: {conta.cliente._nome}
            Saldo: {conta.saldo:.2f}
            """
        
        #Caso o index seja maior que o tamanho do array
        except IndexError:
            #Para a iteração
            raise StopIteration
        finally:
            #Incrementa o index
            self._index += 1

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques

        #saques_realizados serve para contar quantos saques foram realizados
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self._limite_saques:
            print("Operação falhou! Limite de saques excedido.")
            return False
        
        elif valor > self._limite:
            print("Operação falhou! O valor do saque é maior que o limite.")
            return False
        
        else:
            self.saques_realizados += 1
            return super().sacar(valor)
        
    # __str__ é usado para mostrar os valores de uma classe
    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            Número: {self.numero}
            Proprietário: {self.cliente._nome}
        """

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):

        if len(conta._historico.transacoes_do_dia()) >= 10:
            print("Limite de transações diarias atingido.")
            return
        
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao._valor,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

    #Gerador de relatórios
    def gerar_relatorio(self, tipo_transacao = None):
        
        #Para cada transação em self._transacoes retorna a transação
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
               #yield é usado para retornar os valores em um gerador
                yield transacao

    def transacoes_do_dia(self):

        #Armazena a data atual
        data_atual = datetime.now().date()

        #Cria uma lista para armazenar as transações
        transacoes = []

        #Para cada transação em self._transacoes, verifica se a data da transação é igual a data atual
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%Y-%m-%d %H:%M:%S").date()
            
            if data_atual == data_transacao:
                transacoes.append(transacao)

        return transacoes
    
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta._historico.adicionar_transacao(self)
            return True

class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta._historico.adicionar_transacao(self)
            return True
    
def log_transacao(func):

    def wrapper(*args, **kwargs):

        #resultado armazena o retorno da função
        resultado = func(*args, **kwargs)

        #Printa a data e o nome da função
        print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {func.__name__}".upper())

        #Retorna o resultado
        return resultado

    return wrapper

#Função para realizar o saque
@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do titular da conta: ")
    usuario = verificar_se_usuario_existe(cpf, clientes)
    
    if not usuario:
        print("Operação falhou! Cliente nao encontrado.")
        return
    
    valor = float(input("Informe o valor a ser sacado: "))

    transacao = Saque(valor)

    conta = recuperar_conta_usuario(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta, transacao)

#Função para realizar o depósito
@log_transacao
def depositar(clientes):

    #Input para informar o CPF
    cpf = input("Informe o CPF do titular da conta: ")

    #Utilizando um metodo para verificar se o CPF informado existe
    usuario = verificar_se_usuario_existe(cpf, clientes)

    #Caso não exista, informa que a operação falhou
    if not usuario:
        print("Operação falhou! Cliente não encontrado.")
        return

    #Caso exista o titular da conta, realiza o depósito com base no input
    valor = float(input("Informe o valor a ser depositado: "))

    #Cria uma transação de depósito
    transacao = Deposito(valor)

    #Recupera a primeira conta do titular
    conta = recuperar_conta_usuario(usuario)
    if not conta:
        return

    #Realiza a transação
    usuario.realizar_transacao(conta,transacao)

#Método de verificação de CPF
def verificar_se_usuario_existe(cpf, clientes):
    for cliente in clientes:
        if cliente._cpf == cpf:
            return cliente
    return None
        
#Método de assimilação de conta
def recuperar_conta_usuario(cliente):
    if not cliente._contas:
        print("Operação falhou! Cliente nao possui contas cadastradas.")
        return
    else:
        #Retorna a primeira conta do cliente
        return cliente._contas[0]

#Função para mostrar o extrato
@log_transacao
def mostrar_extrato(clientes):

    cpf = input("Informe o CPF do titular da conta: ")
    usuario = verificar_se_usuario_existe(cpf, clientes)

    if not usuario:
        print("Operação falhou! Cliente nao encontrado.")
        return

    conta = recuperar_conta_usuario(usuario)
    if not conta:
        return
    
    print("".center(40, "="))

    #Cria o extrato com base nas transações: Tipo + Valor
    extrato = ""

    tem_transacao = False

    for transacao in conta._historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}: R$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato += "\nNenhuma transação realizada."

    #Exibe o extrato e o saldo
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("".center(40, "="))

    return extrato

#Função para cadastrar usuário
@log_transacao
def cadastrar_usuario(clientes):

    print("\nCadastrar Usuário")

    cpf = input("Digite o CPF do titular da conta: ")
    usuario = verificar_se_usuario_existe(cpf, clientes)

    if usuario:
        print("Operação falhou! Cliente ja cadastrado.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)

    clientes.append(usuario)

    print("".center(40, "="))
    print("Usuário cadastrado com sucesso!")
    print("".center(40, "="))
        
#Função para listar usuários
def listar_contas(contas):

    #Verifica se algum usuário foi cadastrado
    if not contas:
        print("Usuário não possui contas cadastradas.")
        return

    #Mostra todos os usuários
    for conta in ContaIterador(contas):
        print("".center(40, "="))
        print(conta)
        
#Função para criar uma conta corrente
@log_transacao
def criar_conta_corrente(clientes, contas):

    cpf = input("Informe o CPF do titular da conta: ")
    usuario = verificar_se_usuario_existe(cpf, clientes)

    if not usuario:
        print("Operação falhou! Cliente nao encontrado.")
        return
    
    numero_conta = len(contas) + 1
    #Cria uma nova conta
    conta = ContaCorrente.nova_conta(numero_conta, usuario)

    #Adiciona a nova conta ao array de contas
    contas.append(conta)

    #Adiciona a nova conta ao array de contas do titular
    usuario._contas.append(conta)

    print("Operação realizada com sucesso!")

def main():
    #Arrays para armazenar os usuários e contas
    usuarios = []
    contas = []


    while True:

        opcao = menu()

        #Cadastrar usuário
        if opcao == "c":
            cadastrar_usuario(usuarios)

        #Listar contas
        elif opcao == "l":
            listar_contas(contas)

        #Criar Conta Corrente
        elif opcao == "cc":
            criar_conta_corrente(usuarios, contas)

        #Depósito
        elif opcao == "d":
            depositar(usuarios)

        #Saque
        elif opcao == "s":
            sacar(usuarios)

        #Extrato
        elif opcao == "e":
            mostrar_extrato(usuarios)
        
        #Sair
        elif opcao == "q":    
            break

        else:
            print("Operação inválida, por favor selecione novamente a opção desejada.")

main()