from blockchain import Blockchain
from uuid import uuid4
from utility.verification import Verification
from wallet import Wallet


class Node:

    def __init__(self):
        #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()  # temp, jak będzie portfel to będzie j.w.
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def listen_for_input(self):
        wait_for_input = True

        while wait_for_input:
            print("Wybierz akcje ")
            print('1 Nowa wartość transakcji \n2 Mine nowy blok \n3 Wyświetl bloki blockchaina \n4 Sprawdź ważność transakcji \n5 Stwórz portfel \n6 Wczytaj portfel \n7 Zapisz klucze\nq Aby wyjść')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                recipient, amount = self.get_transaction_val()
                signature = self.wallet.sign_transaction(
                    self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Dodano transakcje')
                else:
                    print('Niepowodznie w dodawaniu transakcji')
                # print(open_transactions)
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Niepowodzenie miningu, sprawdź czy posiadasz portfel')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("Transakcje są poprawne")
                else:
                    print("Transakcje błędne")
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == 'q':
                wait_for_input = False
            else:
                print('Niepoprawna cyfra ')
            if not Verification.verify_chain(self.blockchain.chain):
                print("Blockchain został zmanipulowany!")
                break

            print("Bilans konta {} : {:6.2f}".format(
                self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print("Użytkownik wyszedł")

    def print_blockchain_elements(self):
        """Wypisuje w pętli wszystkie bloki w blockchainie"""
        for block in self.blockchain.chain:
            print(block)
        else:
            print('-'*30)

    def get_transaction_val(self):
        """Przyjmuje adres odbierającego i liczbę od użytkownika ,zwraca str adresata i float wartości"""
        return (input('Podaj odbierającego transkcje '), float(input("Podaj wartość transakcji ")))

    def get_user_choice(self):
        """Pobiera od użytkownika wartość ,wypisuje na ekranie również 'Twój wybór '"""
        return input('Twój wybór ')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()

# print(__name__)
