from datetime import datetime

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def registrar(self, conta):
        raise NotImplementedError("Subclass must implement abstract method")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito:\tR$ {self.valor:.2f}")
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        if isinstance(conta, ContaCorrente):
            if self.valor > conta.saldo:
                print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
                return False
            elif self.valor > conta.limite:
                print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
                return False
            elif conta.numero_saques >= conta.limite_saques:
                print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
                return False
            else:
                conta.saldo -= self.valor
                conta.numero_saques += 1
                conta.historico.adicionar_transacao(f"Saque:\t\tR$ {self.valor:.2f}")
                print("\n=== Saque realizado com sucesso! ===")
                return True
        else:
            if self.valor > conta.saldo:
                print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
                return False
            else:
                conta.saldo -= self.valor
                conta.historico.adicionar_transacao(f"Saque:\t\tR$ {self.valor:.2f}")
                print("\n=== Saque realizado com sucesso! ===")
                return True

class Conta:
    def __init__(self, cliente, numero, agencia):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    @staticmethod
    def nova_conta(cliente, numero, agencia):
        return Conta(cliente, numero, agencia)

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = datetime.strptime(data_nascimento, "%d-%m-%Y")

# Exemplo de uso
def main():
    cliente = PessoaFisica("10103030303", "Pedro Gustavo ", "04-08-2005", "Rua Exemplo, 123 - Bairro - Cidade/UF")
    conta_corrente = ContaCorrente(cliente, 1, "0001", 500, 3)
    cliente.adicionar_conta(conta_corrente)

    cliente.realizar_transacao(conta_corrente, Deposito(1500))
    cliente.realizar_transacao(conta_corrente, Saque(1000))
    cliente.realizar_transacao(conta_corrente, Saque(600))  # Deverá falhar devido ao limite
    cliente.realizar_transacao(conta_corrente, Saque(300))

    print("\nExtrato da Conta:")
    for transacao in conta_corrente.historico.transacoes:
        print(transacao)
    print(f"Saldo atual: R$ {conta_corrente.saldo:.2f}")

if __name__ == "__main__":
    main()
