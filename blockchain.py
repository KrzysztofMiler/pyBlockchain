import functools
import hashlib as hl
import json
from collections import OrderedDict
# Stat blockchain'a
MINING_REWARD = 10

genesis_block = {'previous_hash': '',
                 'index': 0,
                 'transactions': [],
                 "proof": 100}
blockchain = [genesis_block]
open_transactions = []
owner = 'me'
participants = {'me'}


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hl.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[0:2] == '00'  # nasz warunek na poprawy hash


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def hash_block(block):
    return hl.sha256(json.dumps(block,sort_keys=True).encode()).hexdigest()
# json.dumps tworzy string z bloku i jeszcze trzeba dać .encode() aby ztranslatować na binarny i potem.hexdigest() na str


def get_balance(participant):
    sender = [[tx["amount"] for tx in block['transactions']
               if tx['sender'] == participant]for block in blockchain]

    open_sender = [tx['amount']
                   for tx in open_transactions if tx['sender'] == participant]
    sender.append(open_sender)
    amt_sent = functools.reduce(
        lambda suma, amt: suma + sum(amt) if len(amt) > 0 else suma + 0, sender, 0)

    recepient = [[tx["amount"] for tx in block['transactions']
                  if tx['recipient'] == participant]for block in blockchain]
    amt_recieved = functools.reduce(
        lambda suma, amt: suma + sum(amt) if len(amt) > 0 else suma + 0, recepient, 0)

    return amt_recieved - amt_sent


def get_last_blockchain_val():
    """Zwraca ostatnią warość w danym blokchainie"""
    if len(blockchain) < 1:
        return None
    else:
        return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    else:
        return False


def add_transaction(recipient, sender=owner, amount=1.0):
    """Dodaj nową wartość na koniec blokchaina

    Arg:
        :sender: wysyłajacy transakcje

        :recipient: odbierający transakcje
        :amount: wartość transakcji (domyślnie 1.0)
    """
    #transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    transaction = OrderedDict([('sener',sender),('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    """Tworzy natępny blok w blockchain"""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)  # tutaj optymalizacja
    proof = proof_of_work()

    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = OrderedDict([('sender', 'MINING'),('recipient', owner),('amount', MINING_REWARD)])

    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_transaction,
             'proof': proof}
    blockchain.append(block)
    return True


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
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print("Niepoprawny proof_of_work")
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


wait_for_input = True


while wait_for_input:
    print("Wybierz akcje ")
    print('1 Nowa wartość transakcji \n2 Mine nowy blok \n3 Wyświetl bloki blockchaina \n4 Podaj użytkowników \n5 Sprawdź ważność transakcji \nh Aby zmodyfikować \nq Aby wyjść')
    user_choice = get_user_choice()
    if user_choice == '1':
        recepient, amount = get_transaction_val()
        if add_transaction(recepient, amount=amount):
            print('Dodano transakcje')
        else:
            print('Niepowodznie w dodawaniu transakcji')
        # print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print("Transakcje są poprawne")
        else:
            print("Transakcje błędne")
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

    print("Bilans konta {} : {:6.2f}".format('Ja', get_balance('me')))
else:
    print("Użytkownik wyszedł")
