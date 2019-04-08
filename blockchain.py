blockchain = [1]


def get_last_blockchain_val():
    return blockchain[-1]


def add_value(transaction_amount):
    blockchain.append([get_last_blockchain_val(), transaction_amount])


add_value(5)

print(blockchain)

