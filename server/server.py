
import socket
import os
import wave
from _thread import *
import json
import pickle


devices = []
BUFFER_SIZE = 1024
sockets = {}

def list_devices(client_socket):
    print('devices')
    print(sockets)
    client_socket.send(pickle.dumps(devices))


def list_songs(client_socket):
    print('songs')
    songs = os.listdir('resource')
    songs = [song for song in songs if song.endswith(".wav")]
    songs_str = "\n".join(songs)
    client_socket.send(songs_str.encode())

# msg = {'service': 'play_music', 'music': f'{song_choice},'device':'198.0.1.1' '}


def play_music_server(client_socket, song_choice):
    if os.path.exists(f"resource/{song_choice}"):
         with wave.open(f"resource/{song_choice}", "rb") as song_file:
            data = song_file.readframes(BUFFER_SIZE)
            while data != b'':
                client_socket.send(data)
                data = song_file.readframes(BUFFER_SIZE)
            song_file.close()
            end_message = "\nnn".encode()
            client_socket.send(end_message)


def handle_client(client_socket, client_address):
    print(f"Conexão estabelecida com o cliente {client_address}")

    while True:
        command = client_socket.recv(1024).decode()
        request = json.loads(command)
        print(request)
        if request['service'] == 'list_devices':
            list_devices(client_socket)
        elif request['service'] == 'list_songs':
            list_songs(client_socket)
        elif request['service'] == 'play_music':
            music = request['music']
            if  'device' in request:
                ip_device_target = request['device']
                play_music_server(devices[ip_device_target],music)
                pass
            else:
                play_music_server(client_socket, music)
        elif request['service'] == 'end_connection':
            client_socket.close()
            devices.remove(client_address)

            print(f"Conexão encerrada com o cliente {client_address}")
            break

                        
def start_server():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("192.168.1.8",hostname)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.1.8', 12345))
    server_socket.listen(5)
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(client_socket)
        sockets[client_address[0]] = client_socket
        devices.append([client_address[0],client_address[1]])
        start_new_thread(handle_client,(client_socket, client_address))

start_server()