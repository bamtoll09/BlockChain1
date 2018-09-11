from Block import Block
import datetime as date
import json
from flask import Flask
from flask import request
node = Flask(__name__)

def create_genesis_block():
    return Block(0, date.datetime.now(), 
        { "proof-of-work": 1, "transactions": [] }, "0")

blockchain = [create_genesis_block()]
this_nodes_transactions = []

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)
        print "New transaction"
        print "FROM: {}".format(new_txion['from'])
        print "TO: {}".format(new_txion['to'])
        print "AMOUT: {}".format(new_txion['amount'])
        return "Transaction submission successful\n"

def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']

    proof = proof_of_work(last_proof)

    this_nodes_transactions.append(
        { "from": "network", "to": miner_address, "amount": 1 }
        )
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
        }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    this_nodes_transactions[:] = []
        
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
        )
    blockchain.append(mined_block)

    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain
    send = []
    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        send.append({
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
                })
    # chain_to_send = json.dumps(chain_to_send)
    return json.dumps(send)

def find_new_chains():
    other_chains = []
    for node_url in peer_nodes:
        block = requests.get(node_url + "/blocks").content
        block = json.loads(block)
        other_chains.append(block)
    return other_chains

def consensus():
    other_chains = find_new_chains()
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain

    blockchain = longest_chain

node.run()
