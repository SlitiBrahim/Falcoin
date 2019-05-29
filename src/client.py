import argparse
from api import api
import time

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

    blockchain = [90, 2, 3]

    if args.exposeApi:
        print("Expose api")
        thread_api = api.get_thread(blockchain)
        thread_api.start()

    print("run client as {} node.".format(args.node))

    time.sleep(10)
    print("update db")
    blockchain[0] = 30

    print("debug")

if __name__ == '__main__':
    main()