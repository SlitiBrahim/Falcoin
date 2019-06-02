import threading
import socket
import re

class Node(threading.Thread):

    MSG_IPLIST = "IPLIST"
    MSG_REGISTER_ME = "REGISTER_ME"

    RES_OK = "OK"
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

    def init_server(self):
        print("Initializing server on {}".format(Node.__print_addr(self.__host, self.__port)))
        self.__srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__srv_sock.bind((self.__host, self.__port))
        self.__srv_sock.listen(1)

    def treat_msg(self, msg):
        # match ex: "server_addr:127.0.0.1:51100;msg:REGISTER_ME"
        msg_reg = "^server_addr\:((?:[0-9]{1,3}\.){3}[0-9]{1,3})\:([0-9]+);msg\:(.+)$"
        host, port, msg = re.match(msg_reg, msg).groups()

        if msg == Node.MSG_REGISTER_ME:
            return self.register_node((host, port))

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
            return data

    @staticmethod
    def __print_addr(host, port):
        return "{}:{}".format(host, port)