from node import Node
from flask import Flask

node = Node({'port': 8002, 'pubkey': [1571, 13578793],
             'privkey': [13518731, 13578793],
             'peers': [8001, 8003, 8004]})

app = Flask(__name__)


@app.route("/make_transaction", methods=['POST'])
def make_transaction():
    return node.make_transaction_and_forward_to_peers()


@app.route("/receive_transaction", methods=['POST'])
def receive_transaction():
    return node.receive_transaction()


@app.route("/mine", methods=['POST'])
def mine():
    return node.mine()


@app.route("/receive_block", methods=['POST'])
def receive_block():
    return node.receive_block()


app.run(port=node.node_id)
