import socket, os
import threading, wave, pickle, struct


def set_client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_name = socket.gethostname()
    client_ip = socket.gethostbyname(client_name)
    socket_address = (client_ip, port)
    print('server listening at',socket_address)
    client.connect(socket_address)
    print("CLIENT CONNECTED TO",socket_address)
    packet = client.recv(2048)
    print(packet)


set_client(3000)
