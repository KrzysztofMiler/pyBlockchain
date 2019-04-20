"""Dodaje możliwość weryfikacji blockchaina"""

from utility.hash_util import hash_block, hash_string_256
from wallet import Wallet

class Verification:
    @classmethod
    def verify_chain(cls, blockchain):
        """Weryfikuje blockchain za pomocą sprawdzenia czy poprzednie fragmenty są takie same, zwraca bool True jeśli jest porawny i False jeśli jest zmanipulowany"""
        for (index, block) in enumerate(blockchain):
            if index == 0:  # zobaczyć czy się nie da inaczej by nie marnować cykli
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Niepoprawny proof_of_work")
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance,check_funds=True):
        if check_funds:
            sender_balance = get_balance()
            if sender_balance >= transaction.amount and Wallet.verify_transactions(transaction):
                return True
            else:
                return False
        else:
            return Wallet.verify_transactions(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]
                     ) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        #print(guess_hash)
        return guess_hash[0:2] == '00'  # nasz warunek na poprawy hash
