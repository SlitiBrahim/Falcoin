import threading
import socket
import re
import random

class Node(threading.Thread):

    MSG_GET_NODES = "GET_NODES"
    MSG_REGISTER_ME = "REGISTER_ME"
    MSG_PING = "PING"

    RES_OK = "OK"
    RES_INVALID_MSG = "INVALID_MSG"
    RES_ALREADY_REGISTERED = "ALREADY_REGISTERED"

    def __init__(self, host, port):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__srv_sock = None
        self.__client_sock = None
        self.__stop_event = threading.Event()
        self.__nodes = []

    # def get_host(self):
    #     return self.__host
    #
    # def set_host(self, host):
    #     self.__host = host

    def get_nodes(self):
        return self.__nodes

    def add_node(self, node):
        self.__nodes.append(node)

        return self.__nodes

    def is_node_registered(self, node):
        for r_node in self.__nodes:
            if r_node == node:
                return True

        return False

    def register_node(self, node):
        if not self.is_node_registered(node):
            print("Registering node {}".format(Node.__print_addr(*node)))
            self.add_node(node)
            res = Node.RES_OK
        else:
            print("Node {} is already registered.".format(Node.__print_addr(*node)))
            res = Node.RES_ALREADY_REGISTERED

        return res

    def get_nodes_list(self, node=None):
        nodes = self.__nodes[:]

        if node is not None:
            curr_node_index = -1
            # removing the node asking for nodes from list
            for index, r_node in enumerate(nodes):
                if r_node == node:
                    curr_node_index = index
                    break

            if curr_node_index >= 0:
                nodes.pop(curr_node_index)

        print("debug:", nodes)
        res = ";".join(map(lambda n: "{}:{}".format(*n), nodes))
        if len(nodes) == 1:
            res += ';'

        return res

    def init_server(self):
        print("Initializing server on {}".format(Node.__print_addr(self.__host, self.__port)))
        self.__srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__srv_sock.bind((self.__host, self.__port))
        self.__srv_sock.listen(1)

    def treat_msg(self, msg):
        # match ex: "server_addr:127.0.0.1:51100;msg:REGISTER_ME"
        msg_reg = "^server_addr\:((?:[0-9]{1,3}\.){3}[0-9]{1,3})\:([0-9]+);msg\:(.+)$"
        host, port, msg = re.match(msg_reg, msg).groups()
        node = (host, port)

        if msg == Node.MSG_REGISTER_ME:
            return self.register_node(node)
        elif msg == Node.MSG_GET_NODES:
            return self.get_nodes_list(node)
        else:
            return Node.RES_INVALID_MSG

    @staticmethod
    def parse_str_node(str_node):
        # match ex: "127.0.0.1:51100"
        node_reg = "^((?:[0-9]{1,3}\.){3}[0-9]{1,3})\:([0-9]+)$"
        node = re.match(node_reg, str_node).groups()

        return node

    @staticmethod
    def parse_nodes_msg(nodes_msg):
        str_nodes = nodes_msg.split(';')
        print("str_nodes", str_nodes)
        str_nodes = filter(lambda str_n: str_n != '', str_nodes)

        nodes = list(map(lambda n: Node.parse_str_node(n), str_nodes))

        return nodes

    def run(self):
        """Will be run in a thread."""

        print("Listening for connections...")
        while not self.stopped():
            conn, addr = self.__srv_sock.accept()
            with conn:
                print("Connected by", Node.__print_addr(*addr))
                while True:
                    data = conn.recv(1024)
                    if data:
                        print("received data:", data)
                        res = self.treat_msg(data.decode('utf-8'))
                        print("res", res)
                        conn.sendall(str.encode(res))
                    else:
                        break

    def stop(self):
        """Stops the current thread."""
        self.__stop_event.set()

    def stopped(self):
        return self.__stop_event.is_set()

    def send(self, host, port, data):
        self.__client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.__client_sock as sock:
            print("Connecting to {}".format(Node.__print_addr(host, port)))
            sock.connect((host, port))
            print("Sending message: {}".format(data))
            sock.sendall(str.encode(data))
            data = sock.recv(1024)
            return data.decode('utf-8')

    def ping(self, node):
        print("Ping", Node.__print_addr(*node))
        nonce = random.randint(1, 1001)
        msg = "{};nonce={}".format(self.format_msg(Node.MSG_PING), nonce)

        return self.send(*node, msg)

    def format_msg(self, msg):
        return "server_addr:{}:{};msg:{}".format(self.__host, self.__port, msg)

    @staticmethod
    def __print_addr(host, port):
        return "{}:{}".format(host, port)