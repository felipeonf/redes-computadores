
import socket
import os
import wave
from _thread import *
import json
import pickle
devices = []

def handle_client(client_socket, client_address):
    print(f"Conexão estabelecida com o cliente {client_address}")

    while True:

        # Recuperar a lista de músicas disponíveis no servidor
        songs = os.listdir('resource')
        songs = [song for song in songs if song.endswith(".wav")]
        songs_str = "\n".join(songs)
        initial_cmd = client_socket.recv(1024).decode()
        request = json.loads(initial_cmd)
        print(request)
        if request['service'] == 'list_devices':
            print('devices')
            client_socket.send(pickle.dumps(devices))
        if request['service'] == 'list_songs':
            print('songs')
            client_socket.send(songs_str.encode())
            # Receber a música escolhida pelo cliente
            song_choice = client_socket.recv(1024).decode()

            if os.path.exists(f"resource/{song_choice}"):
                with wave.open(f"resource/{song_choice}", "rb") as song_file:
                    data = 1
                    while data != b'':
                        data = song_file.readframes(1024)
                        client_socket.send(data)
                        # print(data)
                        # print("Deseja continuar?")
                    break
    client_socket.close()
    devices.remove(client_address)
    print(f"Conexão encerrada com o cliente {client_address}")

                
        
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 10000))
    server_socket.listen(5)

    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, client_address = server_socket.accept()
        devices.append(client_address)
        start_new_thread(handle_client,(client_socket, client_address))

start_server()