from node import Node
from flask import Flask
from block import Block
from flask import Response

node = Node({'port': 8004, 'pubkey': [691, 21952669],
             'privkey': [8637051, 21952669],
             'peers': [8002, 8003]})

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


@app.route("/test", methods=['GET'])
def test():
    print("Hash 1" + Block.hash("Hash 1"))
    print("Hash 1" + Block.hash("Hash 1"))
    return Response("Res")


app.run(port=node.node_id)
