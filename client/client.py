import socket
import threading
import pyaudio
import os

def play_audio(client_socket, song_choice):
    chunk_size = 1024
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    frames_per_buffer=4096,
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
    if not os.path.isdir("cache"):
        os.makedirs("cache")
    songs_cache = os.listdir('cache') 

    # Recuperar a lista de músicas do servidor
    songs_list = client_socket.recv(2048).decode()
    print("Lista de músicas disponíveis:")
    print(songs_list)

    # Escolher uma música para reproduzir
    song_choice = input("Digite o nome da música que deseja reproduzir: ")
    if song_choice in songs_cache:
        chunk_size = 1024
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(3),
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

        # Iniciar a reprodução da música em uma thread separada
        audio_thread = threading.Thread(target=play_audio, args=(client_socket, song_choice))
        audio_thread.start()

        # Aguardar a reprodução da música
        audio_thread.join()

        # Fechar a conexão com o servidor
        client_socket.close()

start_client()
