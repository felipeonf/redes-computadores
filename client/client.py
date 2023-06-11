import socket
import threading
import pyaudio
import os
import wave
import json
import pickle

def list_devices(client_socket):
    msg = {'service':'list_devices'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    devices = client_socket.recv(1024)
    list_devices = pickle.loads(devices)
    print(list_devices)

def list_songs(client_socket):
    msg = {'service':'list_songs'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    songs_list = client_socket.recv(2048).decode()
    if not os.path.isdir("cache"):
        os.makedirs("cache")
    # Recuperar a lista de músicas do servidor
    print("Lista de músicas disponíveis:")
    print(songs_list)

def choose_music():
    pass

    

def play_audio(client_socket, song_choice):
    chunk_size = 1024
    FORMAT = pyaudio.paInt16
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=2,
                    rate=44100,
                    frames_per_buffer=1024,
                    output=True)
    
    data_of_file = b""
    while True:
        data = client_socket.recv(chunk_size)
        data_of_file += data
        if not data:
            break
        stream.write(data)
    
    if len(data_of_file) != 0:
        file = open(f'cache/{song_choice}', 'wb')
        len(data_of_file)
        file.write(data_of_file)
        file.close()
    stream.stop_stream()
    stream.close()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 10000))
    while True:
        initial_command = input('1 - Listar dispositivos disponíveis\n2 - Listar músicas disponíveis\n3 - Tocar Música\n4 - Encerrar conexão\n')
        match (initial_command):
            case '1':
                list_devices(client_socket)
            case '2':
                list_songs(client_socket)
            case '3':
                # Escolher uma música para reproduzir
                song_choice = input("Digite o nome da música que deseja reproduzir: ")
                songs_cache = os.listdir('cache')
                if song_choice in songs_cache:
                    chunk_size = 1024
                    p = pyaudio.PyAudio()
                    stream = p.open(format=p.get_format_from_width(2),
                                    channels=2,
                                    rate=44100,
                                    output=True)
                    print("Reproduzindo do cache!")
                    with open(f'cache/{song_choice}', 'rb') as file:
                        while True:
                            data = file.read(chunk_size)
                            buffer_size = len(data)  # Tamanho atual do buffer
                            print(f"Tamanho do buffer: {buffer_size}")
                            if not data:
                                    break
                            stream.write(data)
                    
                else:
                    client_socket.send(song_choice.encode())
                    play_audio(client_socket, song_choice)
                    client_socket.close()
            case _:
                break;

start_client()