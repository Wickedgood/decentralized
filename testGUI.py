from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import queue
import logging
import inspect

def accept_incoming_connections():

    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #msg_list.insert(tkinter.END, msg)
            msglistqueue.put(msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    try:
        client_socket.send(bytes(msg, "utf8"))
    except ConnectionResetError:
        pass
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def userquit(name):
    broadcast(bytes("%s has left the chat." % name, "utf8"))


def broadcast(msg, prefix=""):
    # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf8") + msg)
        except ConnectionResetError:
            print("Cannot send to ", prefix, " Connection has been reset")


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


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

def after_callback():
    try:
        msg = msglistqueue.get(block=False)
    except queue.Empty:
        # let's try again later
        top.after(100, after_callback)
        return
    if msg is not None:
        # we're not done yet, let's do something with the message and
        # come back ater
        msg_list.insert(tkinter.END, msg)
        top.after(100, after_callback)


clients = {}
addresses = {}

HOST = ''
PORT = 31337
BUFSIZ = 1024
ADDR = (HOST, PORT)

msglistqueue = queue.Queue()

SERVER = socket(AF_INET, SOCK_STREAM)
try:
    SERVER.bind(ADDR)
except OSError:
    print("Server is already running?")

if __name__ == "__main__":
    top = tkinter.Tk()
    top.title("Noyz")
    try:
        SERVER.listen()
    except OSError:
        print("Server is already running?")
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)



    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    # ----Now comes the sockets part----
    # HOST = input('Enter host: ')
    HOST = "127.0.0.1"
    PORT = 31337

    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    try:

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)
    except ConnectionRefusedError:
        print("You sure about that?")

    ACCEPT_THREAD.start()
    receive_thread = Thread(target=receive)
    receive_thread.start()
    top.after(100, after_callback)
    tkinter.mainloop()  # Starts GUI execution.

    ACCEPT_THREAD.join()
    SERVER.close()
