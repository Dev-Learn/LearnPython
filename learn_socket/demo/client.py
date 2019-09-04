#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json

def receive():
    """Handles receiving of messages."""
    global isClose
    global isInput
    while not isClose:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg:
                print(msg + "\n")
            if msg == 'quit':
                break
            if msg == 'Input':
                isInput = True
        except OSError:  # Possibly client has left the chat.
            break


def send(msg):  # event is passed by binders.
    """Handles sending of messages."""
    client_socket.send(bytes(str(msg), "utf8"))
    if msg == "quit":
        client_socket.close()
        return True
    return False


#----Now comes the sockets part----


HOST = '10.144.130.118'
PORT = 3000

BUFSIZ = 1024
ADDR = (HOST, PORT)
isClose = False

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

# send("TV")
isInput = False

send("REMOTE")
while not isClose:
    if isInput:
        holder = "Input : \n"
    else:
        holder = "Typing Remote : \n"
    msg = input(holder)
    msgJson = {}
    if isInput:
        msgJson["type"] = "KEY_INPUT"
        isInput = False
    else:
        msgJson["type"] = "KEY_NAVIGATION"
    msgJson["data"] = msg
    if send(msgJson):
        break

    # send(msg)
