from blockchain import Blockchain
from uuid import uuid4
from verification import Verification

class Node:

    def __init__(self):
        #self.id = str(uuid4())
        self.id = 'JA'#temp, jak będzie portfel to będzie j.w.
        self.blockchain = Blockchain(self.id)
        

    def listen_for_input(self):
        wait_for_input = True

        while wait_for_input:
            print("Wybierz akcje ")
            print('1 Nowa wartość transakcji \n2 Mine nowy blok \n3 Wyświetl bloki blockchaina \n4 Sprawdź ważność transakcji \nq Aby wyjść')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                recipient, amount = self.get_transaction_val()
                if self.blockchain.add_transaction(recipient,self.id, amount=amount):
                    print('Dodano transakcje')
                else:
                    print('Niepowodznie w dodawaniu transakcji')
                # print(open_transactions)
            elif user_choice == '2':
                self.blockchain.mine_block()                    
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':                
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("Transakcje są poprawne")
                else:
                    print("Transakcje błędne")
            elif user_choice == 'q':
                wait_for_input = False
            else:
                print('Niepoprawna cyfra ')            
            if not Verification.verify_chain(self.blockchain.chain):
                print("Blockchain został zmanipulowany!")
                break

            print("Bilans konta {} : {:6.2f}".format(self.id, self.blockchain.get_balance()))
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

node = Node()
node.listen_for_input()