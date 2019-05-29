from flask import Flask, jsonify, request
from threading import Thread

app = Flask(__name__)

def run():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)

def get_thread():
    return Thread(target=run)

@app.route('/transactions/<string:tx_id>', methods=['GET'])
def index_tx(tx_id):
    # TODO: Use Blockchain.find_block(tx_id)
    return jsonify({'transaction': 'tx id {}'.format(tx_id)})

@app.route('/transactions', methods=['GET'])
def list_tx():
    args = request.args
    pubkey = args.get('pubkey')
    # TODO: call blockchain.get_transactions(pubkey)

    return jsonify({'transactions': '...'})

@app.route('/transactions', methods=['POST'])
def create_tx():
    # TODO: add tx to transaction pool and share through p2p
    return jsonify("new tx")

@app.route('/balance/<string:pubkey>', methods=['GET'])
def balance(pubkey):
    # TODO: call blockchain.count_balance(pubkey)
    return jsonify({'balance': 50})