#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        if len(clients) == LIMIT:
            client.send(bytes('close', "utf8"))
            client.close()
            return
        # client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        # addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    print(name)
    # welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    # client.send(bytes(welcome, "utf8"))
    # msg = "%s has joined the chat!" % name
    # broadcast(bytes(msg, "utf8"))
    clients[client] = name

    isQuit = False
    while not isQuit:
        msg = client.recv(BUFSIZ)
        if not msg:
            continue
        print(str(msg))
        isQuit = (msg == bytes("quit", "utf8"))
        for sock in clients:
            if isQuit:
                if clients[sock] == "REMOTE".strip():
                    sock.close()
                    continue
                sock.send(msg)
                continue
            if clients[sock] == "TV".strip():
                sock.send(msg)
        if isQuit:
            clients.clear()


clients = {}
# addresses = {}

HOST = '192.168.1.84'
PORT = 5000
BUFSIZ = 4096
LIMIT = 2
ADDR = ((HOST,PORT))

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# https://stackoverflow.com/questions/12362542/python-server-only-one-usage-of-each-socket-address-is-normally-permitted

if __name__ == "__main__":
    SERVER.listen(2)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
