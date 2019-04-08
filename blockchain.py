# Stat blockchain'a
genesis_block = {'previous_hash': '',
                 'index': 0,
                 'transactions': []}
blockchain = [genesis_block]
open_transactions = []
owner = 'me'


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_last_blockchain_val():
    """Zwraca ostatnią warość w danym blokchainie"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """Dodaj nową wartość na koniec blokchaina

    Arg:
        :sender: wysyłajacy transakcje

        :recipient: odbierający transakcje
        :amount: wartość transakcji (domyślnie 1.0)
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    open_transactions.append(transaction)


def mine_block():
    """Tworzy natępny blok w blockchain"""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)  # tutaj optymalizacja

    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': open_transactions}
    blockchain.append(block)


def get_transaction_val():
    """Przyjmuje adres odbierającego i liczbę od użytkownika ,zwraca str adresata i float wartości"""
    return (input('Podaj odbierającego transkcje '), float(input("Podaj wartość transakcji ")))


def get_user_choice():
    """Pobiera od użytkownika wartość ,wypisuje na ekranie również 'Twój wybór '"""
    return input('Twój wybór ')


def print_blockchain_elements():
    """Wypisuje w pętli wszystkie bloki w blockchainie"""
    for block in blockchain:
        print(block)
    else:
        print('-'*30)


def verify_chain():
    """Weryfikuje blockchain za pomocą sprawdzenia czy poprzednie fragmenty są takie same, zwraca bool True jeśli jest porawny i False jeśli jest zmanipulowany"""
    for (index, block) in enumerate(blockchain):
        if index == 0:  # zobaczyć czy się nie da inaczej by nie marnować cykli
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


wait_for_input = True


while wait_for_input:
    print("Wybierz akcje ")
    print('1 Nowa wartość transakcji \n2 Mine nowy blok \n3 Wyświetl bloki blockchaina \nh Aby zmodyfikować \nq Aby wyjść')
    user_choice = get_user_choice()
    if user_choice == '1':
        recepient, amount = get_transaction_val()
        add_transaction(recepient, amount=amount)
        # print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'q':
        wait_for_input = False
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '',
                             'index': 0,
                             'transactions': [{'sender': 'XD', 'recipient': 'dsad', 'amount': 1e6}]}
    else:
        print('Niepoprawna cyfra ')

    if not verify_chain():
        print("Blockchain został zmanipulowany!")
        break

    print("Zarejestrowano wybór")
else:
    print("Użytkownik wyszedł")
