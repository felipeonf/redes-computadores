import socket
import pyaudio
import os
import json
import pickle
import threading

BUFFER_SIZE = 1024
CHANNELS = 2
FORMAT = pyaudio.paInt16
RATE = 44100
is_paused =False
is_finished = False

'''
 TODO
 - Pause e retomada
 - Tocar em bloco de 30 segundos.
 - Interface web
'''

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
    print("-----------------------------------------------")
    print(songs_list)
    print("-----------------------------------------------")


def play_music_with_server(client_socket, song_choice, device = None):
    global is_paused, is_finished

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
        if not is_paused:
            data = client_socket.recv(BUFFER_SIZE)
            data_of_file += data
            if data[-3:] == end_message:
                is_finished = True # Verificando o ultimo trio de bytes da música.
                break
            stream.write(data)
        else:
            continue

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



def handle_user_input():
    global is_paused, is_finished

    while not is_finished:
        command = input("Digite 'p' para pausar ou 'r' para retomar a reprodução: ")
        if command == 'p':
            is_paused = True
            print("Reprodução pausada.")
        elif command == 'r':
            is_paused = False
            print("Reprodução retomada.")
        else:
            print("Comando inválido.")
    print("Reprodução concluída. Encerrando o programa.")

def end_connection(client_socket):
    msg = {'service': 'end_connection'}
    msg_bytes = json.dumps(msg).encode('utf-8')
    client_socket.send(msg_bytes)
    client_socket.close()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.1.67", 12345))
    sock_address = client_socket.getsockname()
    print(sock_address)

    while True:
        print("--------------------------------------------------------------------------------------------------")
        command = input('1 - Listar dispositivos disponíveis\n2 - Listar músicas disponíveis\n3 - Tocar Música\n4 - Ficar disponível para reproduzir músicas\n5 - Encerrar Conexão\n')
        print("--------------------------------------------------------------------------------------------------")
        match (command):
            case '1':
                devices = list_devices(client_socket)
                k = 0
                print("---------------------------------------")
                for i in devices:
                    print(f"{k} - Host: {i[0]}, PORT: {i[1]}")
                    k+=1
                print("---------------------------------------")
            case '2':
                list_songs(client_socket)
            case '3':
                song_choice = input("Digite o nome da música que deseja reproduzir: ")
                devices = list_devices(client_socket)
                k = 0
                for i in devices:
                    print(f"{k} - Host:{i[0]}, Port:{i[1]}")
                    k += 1

                device_choice = input("Digite o índice do dispositivo que deseja reproduzir. ")

                if devices[int(device_choice)][0] == sock_address[0] and devices[int(device_choice)][1] == sock_address[1]:
                    if os.path.isdir("cache"):
                        songs_cache = os.listdir('cache')
                        if song_choice in songs_cache:
                            thread_play_music = threading.Thread(target=play_music_with_cache, args=(song_choice,))
                            thread_play_music.daemon = True
                            thread_play_music.start()
                            user_input_thread = threading.Thread(target=handle_user_input)
                            user_input_thread.daemon = True
                            user_input_thread.start()
                        
                        else:
                            print("Música não encontrada na lista de cache local, transmitindo pelo servidor...")
                            thread_play_music = threading.Thread(target=play_music_with_server, args=(client_socket, song_choice,))
                            thread_play_music.daemon = True
                            thread_play_music.start()
                            user_input_thread = threading.Thread(target=handle_user_input)
                            user_input_thread.daemon = True
                            user_input_thread.start()
                    else:
                        print("Música não encontrada na lista de cache local, transmitindo pelo servidor...")
                        thread_play_music = threading.Thread(target=play_music_with_server, args=(client_socket, song_choice,))
                        thread_play_music.daemon = True
                        thread_play_music.start()
                        user_input_thread = threading.Thread(target=handle_user_input)
                        user_input_thread.daemon = True
                        user_input_thread.start()
                else:
                    print(f"Reproduzindo no dispositivo {device_choice[0]}...")
                    thread_play_music = threading.Thread(target=play_music_with_server, args=(client_socket, song_choice, devices[int(device_choice)],))
                    thread_play_music.daemon = True
                    thread_play_music.start()
                    user_input_thread = threading.Thread(target=handle_user_input)
                    user_input_thread.daemon = True
                    user_input_thread.start()
            case '4':
                music_choice = client_socket.recv(BUFFER_SIZE).decode()
                print(f"Reproduzindo {music_choice}... ")
                play_music_with_server(client_socket,music_choice)
            case '5':
                end_connection(client_socket)
                break

start_client()