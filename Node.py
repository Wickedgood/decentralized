"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import Config
import logging
import inspect
import time
import sys

PORT = 31337


class Node:
    serveraddress = None  # Type: tuple
    connections = None
    name = None
    buffersize = None
    serversocket = None

    def __init__(self, serveraddresstouse, clientaddresstouse):
        func = inspect.currentframe().f_back.f_code
        logging.debug("{},{}".format(serveraddresstouse, clientaddresstouse))
        self.connections = {}
        self.name = ""

        self.start_server(serveraddresstouse)
        logging.debug("server started")
        if clientaddresstouse is not None:
            logging.debug("client has started")
            self.connect_client(clientaddresstouse)


    def start_server(self, serveraddresstouse):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Starting server at {}".format(serveraddresstouse))
        server_addr = serveraddresstouse
        host, port = server_addr.split(":")
        port = int(port)
        self.buffersize = 1024
        self.serveraddress = (host, port)

        self.serversocket = socket(AF_INET, SOCK_STREAM)
        self.serversocket.bind(self.serveraddress)

        Thread(target=self.listen).start()

    def listen(self):
        func = inspect.currentframe().f_back.f_code
        self.serversocket.listen(1)
        logging.debug("Waiting for connection...")
        acceptthread = Thread(target=self.accept_incoming_connections)
        acceptthread.start()
        acceptthread.join()
        self.serversocket.close()


    # Listen for incomming connections
    def accept_incoming_connections(self):
        func = inspect.currentframe().f_back.f_code
        while True:
            client, client_address = self.serversocket.accept()
            # logging.debug("%s:%s has connected." % client_address)
            # Welcome message
            logging.debug("USE THIS PORT STRUCTURE {}".format(str(client)))
            client.send(bytes("Type your name and press enter: ", "utf8"))

            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):  # Takes client socket as argument.
        func = inspect.currentframe().f_back.f_code
        data = client.recv(self.buffersize).decode("utf8")
        if data[0] == '\x11':
            logging.debug("Got a registration? data ={}".format(str(data)))
            # print("register")
            check, address, name = data.split('|')
            if check != "\x11{Register}" and (address != self.server_addr):
                logging.debug("client.send bad friend?")
                client.send(bytes("\x10Bad friend, you have to register yourself.", "utf8"))
                return
            # print("peer",str(client.getpeername()))
            global PORT
            address = str(client.getpeername()[0]) + ":" + str(PORT)
            # print("sock", str(client.getsockname()))
            # logging.debug("craddr{} name{}".format(client.raddr,name))
            self.register(address, name)

        logging.debug("Before while loop")

        while True:
            logging.debug("Waiting for data")
            try:
                msg = client.recv(self.buffersize)
            except:
                break
            logging.debug("Got some data")
            if msg != bytes("\x13{quit}", "utf8"):
                logging.debug("printing {}".format(msg[1:].decode('utf8')))

                if client.getpeername()[0] != "127.0.0.1":
                    print("127", msg.decode('utf8'))

                else:
                    print("721", msg.decode('utf8'))
                '''
                msgDecode = msg.decode('utf8')
                if (msgDecode.split("|")[0] == "\x12{Peers}"):
                    added = self.update_peers(msgDecode)
                    if added:
                        self.broadcast(msg)
                else:
                    self.broadcast(msg, self.name + ": ")
                '''
                msg = ""
            else:
                try:
                    client.send(bytes("\x13{quit}", "utf8"))
                except ConnectionResetError:
                    self.userquit(name)
                client.close()
                self.userquit(name)
                break

    def register(self, address, name):
        func = inspect.currentframe().f_back.f_code

        ip, port = address.split(':')
        if ip != "127.0.0.1":
            logging.debug("Registering peer {0} at {1}".format(name, address))
            port = int(port)
            sock = socket(AF_INET, SOCK_STREAM)
            logging.debug("{}{}".format(address, name))
            sock.connect((ip, port))
            self.connections[name] = ((ip, port), sock)
            logging.debug("Connections: ")
            '''
            c = 0
            for key, value in self.connections.items():
                logging.debug("{}{}:{}".format(c, key, value))
                c += 1

            
            peers = "\x12{Peers}|" + ",".join(list(
                map(lambda x: x + ":" + self.connections[x][0][0] + ":" + str(self.connections[x][0][1]),
                    self.connections)))
            peers = peers + ",{0}:{1}".format(self.name, self.server_addr)
            self.broadcast(bytes(peers, 'utf8'))
            '''

        else:
            logging.debug("not registering a local connection, that's silly.")

    def broadcast(self, msg, prefix=""):
        func = inspect.currentframe().f_back.f_code
        sender = msg.decode('utf8').split(":")[0:-1]
        #logging.debug("sender={} msg={}".format(sender, msg))
        logging.debug("{}".format(str(self.connections)))
        c = 0
        for name, value in self.connections.items():
            logging.debug("to={} info={} msg={}".format(name, str(self.connections[name][0]), msg))
            socket = value[1]
            logging.debug("{}".format(str(socket)))
            socket.send(bytes(prefix, "utf8") + msg)
            c += 1

    '''
    ORIGINAL
    def broadcast(self, msg, prefix=""):
        func = inspect.currentframe().f_back.f_code
        logging.debug("{}".format(msg))
        sender = msg.decode('utf8').split(":")[0:-1]
        sender = list(map(lambda x: x.strip(), sender))
        for name in self.connections:
            if self.connections[name][0] != self.serveraddress and str(name) not in sender:
                # print("Broadcast: {3}|{0}|{1}|{2}|{4}".format(str(self.connections[name][0]), str(self.SERVER_ADDR), sender, name, str(name) not in sender))
                try:
                    logging.debug("to={} info={} msg={}".format(name, str(self.connections[name][0]), msg))
                    self.connections[name][1].send(bytes(prefix, "utf8") + msg)
                except ConnectionResetError:
                    logging.debug("Cannot send to ", prefix, " Connection has been reset")
    '''

    def userquit(self, name):
        func = inspect.currentframe().f_back.f_code
        logging.debug("{}".format(name))
        # Nodes need to note that a peer has left still, and remove it from their peer store
        logging.debug("{0} has quit.".format(name))
        del self.connections[name]
        # self.broadcast(bytes("%s has left the chat." % name, "utf8"))

    def input_loop(self):
        func = inspect.currentframe().f_back.f_code
        logging.debug(" ")
        """Handles sending of messages."""
        while True:
            msg = input("Get Input: ")
            logging.debug("Calling input")
            # self.client_sock.send(bytes("\x10" + msg, "utf8"))
            self.broadcast(bytes(msg, "utf-8"), 'b\x10')
            if msg == "\x13{quit}":
                self.client_sock.close()
                break

    def connect_client(self, client_addr):
        func = inspect.currentframe().f_back.f_code
        logging.debug("{}".format(client_addr))
        ip, port = client_addr.split(':')
        port = int(port)
        self.client_addr = (ip, port)
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.connect(self.client_addr)
        welcome_msg = self.client_sock.recv(self.buffersize).decode('utf8')
        self.name = input(welcome_msg)
        register_msg = bytes("\x11{Register}" + "|{0}:{1}|{2}".format(self.serveraddress[0], self.serveraddress[1], self.name), 'utf8')
        logging.debug("Sending the register message")
        # print("Client Register Msg: " + self.name)
        self.client_sock.send(register_msg)

        self.register(str(ip)+":"+str(port), "server-to-connect")
        logging.debug("registering the connection")
        self.input_loop()

    '''
    def update_peers(self, peer_str):
        func = inspect.currentframe().f_back.f_code
        logging.debug("Added peers!")
        # print(peer_str)
        peers_csv = peer_str.split("|")[1]
        peers = list(peers_csv.split(","))
        added = False
        for peer in peers:
            # print(peer)
            name, ip, port = peer.split(":")
            # print("{0}, {1}, {2}".format(name, ip, port))
            addr = ip + ":" + port
            if (name not in self.connections and addr != self.server_addr):
                self.register_conn(addr, name)
                added = True
        return added
    '''


serveraddress = "0.0.0.0:" + str(PORT)
if len(sys.argv) == 1:
    client_addr = input("client address (where this client will send to/recieve from): ")
else:
    client_addr = sys.argv[1]
# connect first client to its own server

if client_addr == "":
    # client_addr = server_addr
    client_addr = "127.0.0.1:" + str(PORT)
else:
    client_addr += ":" + str(PORT)

node = Node(serveraddress, client_addr)

'''
c = 0
for key, value in client_address.items():
    logging.debug("{}{}:{}".format(c,key,value))
    c+=1
'''
