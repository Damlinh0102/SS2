import simple_rsa as rsa
import json
import hashlib
import base64
from certificate import Certificate


class Transaction:
    def __init__(self, time, sender, certificate,
                 fee, tsType, signature, pubkey, age, forwarder):
        self.time = time
        self.fee = fee
        self.sender = sender
        self.certificate = certificate
        self.tsType = tsType
        self.signature = signature
        self.pubkey = pubkey
        self.age = age
        self.forwarder = forwarder

    def verify_transaction(transaction):
        bin_signature = base64.b64decode(transaction.signature)
        hash1 = base64.b64encode(rsa.decrypt(
            bin_signature, transaction.pubkey)).decode()
        tx_string = transaction.certificate.to_json()
        hash2 = base64.b64encode(hashlib.sha256(
            tx_string.encode()).digest()).decode()
        if (hash1 == hash2):
            return True
        else:
            return False

    def to_json(self):
        tran_dict = {
            'time': self.time,
            'sender': self.sender,
            'fee': self.fee,
            'tsType': self.tsType,
            'certificate': self.certificate.to_json(),
            'signature': self.signature,
            'pubkey': self.pubkey,
            'age': self.age,
            'forwarder': self.forwarder
        }
        return json.dumps(tran_dict, sort_keys=True)

    def to_json_without_age_and_forwarder(self):
        tran_dict = {
            'time': self.time,
            'sender': self.sender,
            'fee': self.fee,
            'tsType': self.tsType,
            'certificate': self.certificate.to_json(),
            'signature': self.signature,
            'pubkey': self.pubkey
        }
        return json.dumps(tran_dict, sort_keys=True)

    def from_json(json_dict):
        certificate = json.loads(
            json_dict['certificate'], object_hook=Certificate.from_json)
        return Transaction(json_dict['time'],
                           json_dict['sender'],
                           certificate,
                           json_dict['fee'],
                           json_dict['tsType'],
                           json_dict['signature'],
                           json_dict['pubkey'],
                           json_dict['age'],
                           json_dict['forwarder'])

    def from_json_without_age_and_forwarder(json_dict):
        certificate = json.loads(
            json_dict['certificate'], object_hook=Certificate.from_json)
        return Transaction(json_dict['time'],
                           json_dict['sender'],
                           certificate,
                           json_dict['fee'],
                           json_dict['tsType'],
                           json_dict['signature'],
                           json_dict['pubkey'], 0, 1000)
