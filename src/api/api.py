from flask import Flask, jsonify, request, Response
from threading import Thread
from blockchain import Transaction
from blockchain import Output
import json

app = Flask(__name__)

# global blockchain used in read-only here
# blockchain wich will be updated by p2p nodes
blockchain = None
tx_pool = None

def run():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

def init_thread(global_blockchain, global_tx_pool):
    # use the blockchain declared in the module outside of any function
    global blockchain
    # set global blockchain
    blockchain = global_blockchain

    global tx_pool
    tx_pool = global_tx_pool

    return Thread(target=run)

@app.route('/transactions/<string:tx_id>', methods=['GET'])
def index_tx(tx_id):
    global blockchain

    tx = Transaction.get_tx_by_hash(tx_id, blockchain)
    res = None
    if tx is not None:
        res = tx.serialize(with_txo_spent_prop=True, blockchain=blockchain)

    return jsonify(res)

@app.route('/transactions', methods=['GET'])
def list_tx():
    global blockchain

    args = request.args
    pubkey = args.get('pubkey')

    txs = blockchain.get_transactions(pubkey)
    # serialize transactions
    s_txs = [tx.serialize(with_txo_spent_prop=True,
                          blockchain=blockchain) for tx in txs]

    return jsonify({'transactions': s_txs})

@app.route('/transactions', methods=['POST'])
def create_tx():
    global tx_pool

    data = request.json
    try:
        transaction = Transaction.deserialize(data)
    except:
        return jsonify({'error': 'Invalid Transaction JSON object.'})

    # TODO: Share to other nodes through p2p
    tx_pool.append(transaction)

    print(tx_pool)

    return Response("Transaction added to transaction pool.", status=200)

@app.route('/balance/<string:pubkey>', methods=['GET'])
def balance(pubkey):
    global blockchain

    balance = blockchain.count_balance(pubkey)

    return jsonify({'balance': balance})

@app.route('/output_information', methods=['POST'])
def get_output_info():
    global blockchain

    # get output from body req
    data = request.form
    try:
        output = Output.deserialize(data)
    except:
        return jsonify({'error': 'Invalid Output JSON object.'})

    output_block, output_tx = blockchain.find_output_block(output)
    if output_block is None:
        return jsonify({'error': 'Could not find block of the given output.'})

    txo_index = output_tx.get_index(output)

    return jsonify({'tx_hash': output_tx.get_hash(), 'txo_index': txo_index})