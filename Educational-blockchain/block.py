import json
import hashlib
from transaction import Transaction


class Block:
    def __init__(self, timestamp, index, transaction, nonce,
                 previous_hash,
                 age, forwarder, miner, is_mining):
        self.timestamp = timestamp
        self.index = index
        self.transaction = transaction
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.age = age
        self.forwarder = forwarder
        self.miner = miner
        self.is_mining = is_mining

    def to_json(self):
        tran_dict = {
            'timestamp': self.timestamp,
            'index': self.index,
            'transaction': self.transaction.to_json_without_age_and_forwarder(),
            'nonce': self.nonce,
            'previous_hash': self.previous_hash,
            'age': self.age,
            'forwarder': self.forwarder,
            'miner': self.miner,
            'is_mining': self.is_mining
        }
        return json.dumps(tran_dict, sort_keys=True)

    def to_json_without_age_and_forwarder(self):
        tran_dict = {
            'timestamp': self.timestamp,
            'index': self.index,
            'transaction': self.transaction.to_json_without_age_and_forwarder(),
            'nonce': self.nonce,
            'previous_hash': self.previous_hash,
            'miner': self.miner
        }
        return json.dumps(tran_dict, sort_keys=True)

    def from_json(json_dict):
        tx_transaction = json_dict['transaction']
        transaction = json.loads(tx_transaction,
                                 object_hook=Transaction.from_json_without_age_and_forwarder)
        return Block(json_dict['timestamp'],
                     json_dict['index'],
                     transaction,
                     json_dict['nonce'],
                     json_dict['previous_hash'],
                     json_dict['age'],
                     json_dict['forwarder'],
                     json_dict['miner'],
                     json_dict['is_mining'])

    def hash(block):
        tran_dict = {
            'timestamp': block.timestamp,
            'index': block.index,
            'transaction': block.transaction.to_json_without_age_and_forwarder(),
            'nonce': block.nonce,
            'previous_hash': block.previous_hash
        }
        string_object = json.dumps(tran_dict, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash
