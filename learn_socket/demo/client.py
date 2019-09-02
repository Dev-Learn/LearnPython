#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    global isClose
    while not isClose:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg + "\n")
            if msg == 'quit':
                break
        except OSError:  # Possibly client has left the chat.
            break


def send(msg):  # event is passed by binders.
    """Handles sending of messages."""
    client_socket.send(bytes(msg, "utf8"))
    if msg == "quit":
        client_socket.close()
        return True
    return False


#----Now comes the sockets part----


HOST = '192.168.1.84'
PORT = 5000

BUFSIZ = 1024
ADDR = (HOST, PORT)
isClose = False

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()


# send("TV")

send("REMOTE")
while not isClose:
    msg = input("Typing Remote : \n")
    if send(msg):
        break
