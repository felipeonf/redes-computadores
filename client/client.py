import socket
import threading
import pyaudio
import os
import json
import pickle


BUFFER_SIZE = 1024
CHANNELS = 2
FORMAT = pyaudio.paInt16
RATE = 44100


def list_devices(client_socket):
    msg = {'service':'list_devices'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    devices = client_socket.recv(BUFFER_SIZE)
    list_devices = pickle.loads(devices)
    print(list_devices)


def list_songs(client_socket):
    msg = {'service':'list_songs'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    songs_list = client_socket.recv(BUFFER_SIZE).decode()
    print("Lista de músicas disponíveis:")
    print(songs_list)


def play_music_with_server(client_socket, song_choice):
    msg = {'service': 'play_music', 'music': f'{song_choice}'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, frames_per_buffer=BUFFER_SIZE, output=True)
    data_of_file = b''
    end_message = b'\nnn'
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        data_of_file += data
        if data[-3:] == end_message:
            break
        stream.write(data)

    if os.path.isdir("cache") == False:
        os.makedirs("cache")

    if len(data_of_file) != 0:
        file = open(f'cache/{song_choice}', 'wb')
        file.write(data_of_file)
        file.close()

    stream.stop_stream()
    stream.close()


def play_music_with_cache(song_choice):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    print("Reproduzindo do cache...")
    with open(f'cache/{song_choice}', 'rb') as file:
        while True:
            data = file.read(BUFFER_SIZE)
            if not data:
                break
            stream.write(data)


def end_connection(client_socket):
    msg = {'service': 'end_connection'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    client_socket.close()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 10000))
    while True:
        command = input('1 - Listar dispositivos disponíveis\n2 - Listar músicas disponíveis\n3 - Tocar Música\n4 - Encerrar conexão\n')
        match (command):
            case '1':
                list_devices(client_socket)
            case '2':
                list_songs(client_socket)
            case '3':
                song_choice = input("Digite o nome da música que deseja reproduzir: ")
                if os.path.isdir("cache"):
                    songs_cache = os.listdir('cache')
                    if song_choice in songs_cache:
                        play_music_with_cache(song_choice)
                    else:
                        print("Música não encontrada na lista de cache local, transmitindo pelo servidor...")
                        play_music_with_server(client_socket, song_choice)  
                else:
                    print("Música não encontrada na lista de cache local, transmitindo pelo servidor...")
                    play_music_with_server(client_socket, song_choice)      
            case '4':
                end_connection(client_socket)
                break

start_client()