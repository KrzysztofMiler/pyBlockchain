# Stat blockchain'a
blockchain = []


def get_last_blockchain_val():
    """Zwraca ostatnią warość w danym blokchainie"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def add_transaction(transaction_amount, last_transaction=get_last_blockchain_val()):
    """Dodaj nową wartość na koniec blokchaina

    Arg:
        :transaction_amount: wartość dodawanej transakcji

        :last_transaction: wartość ostatniej transakcji (domyślnie wywołuje get_last_blockchain_val() która zwraaca ostanią wartoś,
        jeśli jest to pierwsze wywołanie i blokchain jest pusty to wstawi domyslną wartość [1])
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_val():
    """Przyjmuje liczbę od użytkownika ,zamienia na float i zwraca"""
    return float(input("Podaj wartość transakcji "))


def get_user_choice():
    """Pobiera od użytkownika wartość ,wypisuje na ekranie również 'Twój wybór '"""
    return input('Twój wybór ')


def print_blockchain_elements():
    """Wypisuje w pętli wszystkie bloki w blockchainie"""
    for block in blockchain:
        print(block)

def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid

while True:
    print("Wybierz akcje ")
    print('1 Nowa wartość transakcji \n2 Wyświetl bloki blockchaina \nh Aby zmodyfikować \nq Aby wyjść')
    user_choice = get_user_choice()
    if user_choice == '1':
        add_transaction(get_transaction_val(), get_last_blockchain_val())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'q':
        break
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0]=[2]
    else:
        print('Niepoprawna cyfra ')

    if not verify_chain():
        print("Blockchain został zmanipulowany!")
        break

    print("Zarejestrowano wybór")
