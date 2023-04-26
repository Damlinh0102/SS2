from flask import Response
from flask import request
from mempool import Mempool
from blockchain import Blockchain
import requests
import threading
import json
from transaction import Transaction
import time
from certificate import Certificate
import hashlib
import simple_rsa as rsa
import base64
from block import Block


class Node:
    def __init__(self, config):
        self.node_id = config['port']
        self.pubkey = config['pubkey']
        self.privkey = config['privkey']
        self.peers = config['peers']
        self.mempool = Mempool()
        self.blockchain = Blockchain(self.mempool.mempool)

    def thread_function(self, url, data):
        requests.post(url, json=data)

    def make_transaction_and_forward_to_peers(self):
        receiver = request.get_json()['receiver']
        certName = request.get_json()['certName']
        certType = request.get_json()['certType']
        organization = request.get_json()['organization']
        certContent = request.get_json()['certContent']
        fee = request.get_json()['fee']
        tsType = request.get_json()['transactionType']
        certificate = Certificate(receiver, certName, int(time.time()),
                                  certType, organization, certContent)
        tx_string = certificate.to_json()
        tx_hash = hashlib.sha256(tx_string.encode())
        signature = rsa.encrypt(tx_hash.digest(), self.privkey)
        transaction = Transaction(int(time.time()),
                                  self.node_id, certificate, fee, tsType,
                                  base64.b64encode(signature).decode(),
                                  self.pubkey, 3, self.node_id)
        self.mempool.add_to_mempool(transaction)
        for index in range(len(self.mempool.mempool)):
            print("In mempool: transaction " + str(index) + " " +
                  str(self.mempool.mempool[index].to_json()))
        for port in self.peers:
            if (str(port) != str(transaction.sender) and
                str(port) != str(transaction.forwarder)
               and transaction.age > 0):
                transaction.age -= 1
                transaction.forwarder = self.node_id
                x = threading.Thread(target=self.thread_function,
                                     args=("http://localhost:" + str(port) +
                                           "/receive_transaction",
                                           transaction.to_json()))
                x.start()
                print("Sending to http://127.0.0.1:" + str(port) + "...")
        return Response(
            'Transaction has been broadcast to peers',
            mimetype='text/plain'
        )

    def receive_transaction(self):
        tx = request.get_json()
        transaction = json.loads(tx, object_hook=Transaction.from_json)
        if (Transaction.verify_transaction(transaction,)):
            self.mempool.add_to_mempool(transaction)
            for port in self.peers:
                if (str(port) != str(transaction.sender) and
                    str(port) != str(transaction.forwarder)
                        and transaction.age > 0):
                    transaction.age -= 1
                    transaction.forwarder = self.node_id
                    x = threading.Thread(target=self.thread_function,
                                         args=("http://localhost:" + str(port)
                                               + "/receive_transaction",
                                               transaction.to_json()))
                    x.start()
                    print("Sending to http://127.0.0.1:" + str(port) + "...")
        else:
            print("Transaction not verified")
        return Response('Receive transaction from ' + str(transaction.sender),
                        mimetype='text/plain')

    def mine(self):
        block = self.blockchain.new_block(self.node_id)
        for index in range(len(self.blockchain.chain)):
            print("Chain after mine: block " + str(index) + " " +
                  str(self.blockchain.chain[index].to_json()))
        if (block is None):
            return Response("No transaction in mempool to mine")
        if (block is not None and block.is_mining == False):
            for port in self.peers:
                if (str(port) != str(block.forwarder)
                    and str(port) != str(block.miner)
                        and block.age > 0):
                    block.age -= 1
                    block.forwarder = self.node_id
                    x = threading.Thread(target=self.thread_function,
                                         args=("http://localhost:" + str(port)
                                               + "/receive_block",
                                               block.to_json()))
                    x.start()
                    print("Sending to http://127.0.0.1:" + str(port) + "...")
        return Response("Mining the block from lastest transaction",
                        mimetype='text/plain')

    def receive_block(self):
        tx = request.get_json()
        block = json.loads(
            tx, object_hook=Block.from_json)
        valid_new_block = True
        if (len(self.blockchain.chain) == 0):
            self.blockchain.chain.append(block)
        elif (block.index == len(self.blockchain.chain)):
            self.blockchain.chain.append(block)
            if (not self.blockchain.is_valid_chain()):
                valid_new_block = False
                self.blockchain.chain.pop(-1)
        elif (block.index == len(self.blockchain.chain)-1 and
              block.to_json_without_age_and_forwarder() !=
              self.blockchain.chain[-1].to_json_without_age_and_forwarder()):

            clone_chain = self.blockchain.chain.copy()
            self.blockchain.chain[len(self.blockchain.chain)-1] = block
            if (not self.blockchain.is_valid_chain()):
                valid_new_block = False
                self.blockchain.chain = clone_chain
        if (valid_new_block):
            for port in self.peers:
                if (str(port) != str(block.forwarder)
                    and str(port) != str(block.miner)
                        and block.age > 0):
                    block.age -= 1
                    block.forwarder = self.node_id
                    x = threading.Thread(target=self.thread_function,
                                         args=("http://localhost:" + str(port)
                                               + "/receive_block",
                                               block.to_json()))
                    x.start()
                    print("Sending to http://127.0.0.1:" + str(port) + "...")
        return Response("Receiving block", mimetype='text/plain')
