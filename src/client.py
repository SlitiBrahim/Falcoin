from blockchain import Block
from blockchain import GenesisBlock
from blockchain import ProofOfWork
from blockchain import Blockchain
from blockchain import Transaction
from blockchain import CoinbaseTransaction
from blockchain import Input
from blockchain import Output
from blockchain import crypto
from blockchain import utils
from db import Hydrator
from db import Repository
import time
import os
import argparse
from api import api
import time
from p2p import utils as p2p_utils
from p2p import Node

def main():
    parser = argparse.ArgumentParser(description='Client for Falcoin Blockchain.')
    parser.add_argument('--expose-api', dest='exposeApi', action='store_true',
                        help='If set will expose http API to allow communication with blockchain. Default is true.')
    parser.set_defaults(exposeApi=False)
    parser.add_argument('--node', choices=['light', 'full'],
                        help='Run client as light or full node. Light node will not mine blocks.'
                             ' Will run a full node by default.')
    parser.set_defaults(node='full')
    parser.add_argument('--hc-node', dest='is_hc_node', action='store_true',
                        help='If set will define this node as an hard-coded one.'
                             ' Standard node connects to hard-coded nodes to get list of node IPs.')
    parser.set_defaults(is_hc_node=False)

    args = parser.parse_args()

    blockchain = Blockchain()

    if args.exposeApi:
        print("Expose api")
        thread_api = api.init_thread(blockchain)
        thread_api.start()

    print("run client as {} node.".format(args.node))
    if args.is_hc_node:
        print("This node is an hard-coded node.")

    host = '127.0.0.1'
    port = os.environ.get('PORT')
    if port is None:
        raise Exception("Please set 'PORT' env var with the port used by the app.")
    else:
        port = int(port)

    node = Node(host, port)
    node.init_server()
    # Start server
    node.start()

    # if not hc node, connect to hc node to get IPs list
    if not args.is_hc_node:
        hc_node_addr = (host, 51001)
        res_data = node.send(*hc_node_addr, node.format_msg(Node.MSG_REGISTER_ME))
        print("Received:", res_data)
        res_data = node.send(*hc_node_addr, node.format_msg(Node.MSG_GET_NODES))
        nodes = Node.parse_nodes_msg(res_data)
        print("nodes:", nodes)
        # TODO: Get IP list, test and save it (in-memory)


    # br_private_key, br_public_key = crypto.generate_key_pair()
    # yanis_private_key, yanis_public_key = crypto.generate_key_pair()
    # miner_private_key, miner_public_key = crypto.generate_key_pair()
    #
    # txs = [
    #     CoinbaseTransaction(CoinbaseTransaction.generate_default_output(yanis_public_key))
    # ]
    #
    # genesis_block = GenesisBlock(Transaction.extract_valid_transactions(txs, blockchain))
    # pow = ProofOfWork.run(genesis_block)
    # genesis_block.set_proof_of_work(pow)
    # genesis_block.set_hash(pow.get_hash())
    # genesis_block.set_timestamp(time.time())
    #
    # blockchain.add_block_to_chain(genesis_block)
    #
    # input = Input(txs[0].get_hash(), 0, txs[0].get_output(index=0))
    # input.set_pubsig(Input.generate_pubsig(input, yanis_private_key))
    #
    # txs1 = [
    #     CoinbaseTransaction(CoinbaseTransaction.generate_default_output(miner_public_key)),
    #     Transaction(inputs=[input], outputs=[Output(50, br_public_key), Output(50, yanis_public_key)]),
    # ]
    #
    # block1 = Block(Transaction.extract_valid_transactions(txs1, blockchain))
    # block1.set_index(1)
    # block1.set_prev_hash(genesis_block.get_hash())
    # pow = ProofOfWork.run(block1)
    # block1.set_proof_of_work(pow)
    # block1.set_hash(pow.get_hash())
    # block1.set_timestamp(time.time())
    #
    # blockchain.add_block_to_chain(block1)
    #
    # input = Input(txs1[1].get_hash(), 0, txs1[1].get_output(index=0))
    # input.set_pubsig(Input.generate_pubsig(input, br_private_key))
    #
    # txs2 = [
    #     CoinbaseTransaction(CoinbaseTransaction.generate_default_output(miner_public_key)),
    #     Transaction(inputs=[input], outputs=[Output(30, yanis_public_key), Output(20, br_public_key)], fees=0.0),
    # ]
    #
    # block2 = Block(Transaction.extract_valid_transactions(txs2, blockchain))
    # block2.set_index(1)
    # block2.set_prev_hash(block1.get_hash())
    # pow = ProofOfWork.run(block2)
    # block2.set_proof_of_work(pow)
    # block2.set_hash(pow.get_hash())
    # block2.set_timestamp(time.time())
    #
    # blockchain.add_block_to_chain(block2)
    #
    # print("br_pubkey", br_public_key)
    # print("yanis_pubkey", yanis_public_key)
    # print("miner_pubkey", miner_public_key)

    # my_txs = blockchain.get_transactions(my_public_key)

    # ========= DB =========

    # abs_db_path = os.path.abspath('../db/blockchain.db')
    # repository = Repository()
    # repository.connect_to_db(abs_db_path)
    #
    # # repository.add(block1)
    # repository.db_sync(blockchain)
    #
    # block_docs = repository.get_all_docs()
    # block_objs = list(map(lambda doc: Hydrator.hydrate_block(doc), block_docs))

    print("debug")

if __name__ == '__main__':
    main()