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

def main():
    parser = argparse.ArgumentParser(description='Client for Falcoin Blockchain.')
    parser.add_argument('--expose-api', dest='exposeApi', action='store_true',
                        help='If set will expose http API to allow communication with blockchain. Default is true.')
    parser.set_defaults(exposeApi=False)
    parser.add_argument('--node', choices=['light', 'full'],
                        help='Run client as light or full node. Light node will not mine blocks.'
                             ' Will run a full node by default.')
    parser.set_defaults(node='full')

    args = parser.parse_args()

    if args.exposeApi:
        print("Expose api")

    print("run client as {} node.".format(args.node))

    print("debug")

if __name__ == '__main__':
    main()