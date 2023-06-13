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
    return list_devices
    
        


def list_songs(client_socket):
    msg = {'service':'list_songs'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    songs_list = client_socket.recv(BUFFER_SIZE).decode()
    print("Lista de músicas disponíveis:")
    print(songs_list)


def play_music_with_server(client_socket, song_choice, device = None):
    if device:
        msg = {'service': 'play_music', 'music': f'{song_choice}','device':device}
        msg_bytes = json.dumps(msg).encode('utf-8')
    else:
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
    client_socket.connect(("192.168.1.8", 12345))
    clientname = socket.gethostname()
    client_ip_address = socket.gethostbyname(clientname)
    sock_address = client_socket.getsockname()
    socket_port = sock_address[1]
    print(clientname, client_ip_address, socket_port)
    while True:
        command = input('1 - Listar dispositivos disponíveis\n2 - Listar músicas disponíveis\n3 - Tocar Música\n4 -  Ficar disponível para reproduzir músicas\n5 - Encerrar Conexão\n')
        match (command):
            case '1':
                devices = list_devices(client_socket)
                print(devices)
            case '2':
                list_songs(client_socket)
            case '3':

                song_choice = input("Digite o nome da música que deseja reproduzir: ")
                devices = list_devices(client_socket)
                k = 0
                for i in devices:
                    print(f"{k} - Host:{i[0]}, Port:{i[1]}")
                    k += 1
                device_choice = input("Em qual dispositivo deseja reproduzir (indice) ? ")
                print(f'escolha de dispositivo {devices[int(device_choice)]}')
                print(devices[int(device_choice)][0])
                print(client_ip_address)
                if devices[int(device_choice)][0] == sock_address[0] and devices[int(device_choice)][1] == sock_address[1]:
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
                else:
                    print("Música não encontrada na lista de cache local, transmitindo pelo servidor...")
                    play_music_with_server(client_socket, song_choice,device=devices[int(device_choice)])
            case '4':
                music_choice = client_socket.recv(BUFFER_SIZE)
                play_music_with_server(client_socket,music_choice)
            case '5':
                end_connection(client_socket)
                break

start_client()