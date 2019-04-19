import functools
import hashlib as hl
import json
import pickle
from block import Block
from transaction import Transaction
from utility.hash_util import hash_block
from utility.verification import Verification

# Stat blockchain'a
MINING_REWARD = 10


class Blockchain:
    def __init__(self,hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []        
        self.load_data()
        self.hosting_node =hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]
    
    @chain.setter
    def chain(self,val):
        self.__chain =val

    def get_open_transactions(self):
        return self.__open_transactions

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()

                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    # converted_tx = [OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), (
                    #     'amount', tx['amount'])]) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                __open_transactions = json.loads(file_content[1])

                updated_transactions = []
                for tx in __open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['amount'])
                    # updated_transaction = OrderedDict(
                    #     [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            print('Nie znaleziono pliku')

        except ValueError:
            print('Nieporpawna wartość')
        except:
            print('Coś poszło nie tak podczas odczytywania pliku')
        finally:
            print('Połączenie z plikiem zatrzymane')


    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                                                                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                # save_data ={
                #     'chain':blockchain,
                #     'ot':__open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Niepowodzenie przy zapisywaniu')


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        participant = self.hosting_node
        sender = [[tx.amount for tx in block.transactions
                if tx.sender == participant]for block in self.__chain]

        open_sender = [tx.amount
                    for tx in self.__open_transactions if tx.sender == participant]
        sender.append(open_sender)
        amt_sent = functools.reduce(
            lambda suma, amt: suma + sum(amt) if len(amt) > 0 else suma + 0, sender, 0)

        recipient = [[tx.amount for tx in block.transactions
                    if tx.recipient == participant]for block in self.__chain]
        amt_recieved = functools.reduce(
            lambda suma, amt: suma + sum(amt) if len(amt) > 0 else suma + 0, recipient, 0)

        return amt_recieved - amt_sent


    def get_last_blockchain_val(self):
        """Zwraca ostatnią warość w danym blokchainie"""
        if len(self.__chain) < 1:
            return None
        else:
            return self.__chain[-1]


    def add_transaction(self,recipient, sender, amount=1.0):
        """Dodaj nową wartość na koniec blokchaina

        Arg:
            :sender: wysyłajacy transakcje

            :recipient: odbierający transakcje
            :amount: wartość transakcji (domyślnie 1.0)
        """
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient, amount)
        # transaction = OrderedDict(
        #     [('sender', sender), ('recipient', recipient), ('amount', amount)])
        
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False


    def mine_block(self):
        """Tworzy natępny blok w blockchain"""
        if self.hosting_node == None:
            return False
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)  # tutaj optymalizacja
        proof = self.proof_of_work()

        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        # reward_transaction = OrderedDict(
        #     [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])

        copied_transaction = self.__open_transactions[:]
        copied_transaction.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transaction, proof)
        self.__chain.append(block)
        self.__open_transactions =[]
        self.save_data()
        return True
