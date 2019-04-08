blockchain = []


def get_last_blockchain_val():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount])


add_value(5)


tx_amount = float(input("Podaj wartość transakcji "))
add_value(tx_amount)
add_value(last_transaction=get_last_blockchain_val(), transaction_amount=tx_amount)
print(blockchain)
