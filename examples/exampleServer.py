#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            try:
                client.send(bytes("{quit}", "utf8"))
            except ConnectionResetError:
                userquit(name)
            client.close()
            del clients[client]
            userquit(name)
            break

def userquit(name):
    broadcast(bytes("%s has left the chat." % name, "utf8"))


def broadcast(msg, prefix=""):
    # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf8") + msg)
        except ConnectionResetError:
            print("Cannot send to ",prefix," Connection has been reset")


clients = {}
addresses = {}

HOST = ''
PORT = 31337
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen()
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()