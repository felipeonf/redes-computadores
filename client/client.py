import socket
import threading
import pyaudio
import os

def receive_audio(client_socket):
    chunk_size = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    output=True)

    while True:
        data = client_socket.recv(chunk_size)
        if not data:
            break
        stream.write(data)

    stream.stop_stream()
    stream.close()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 10000))
    if not os.path.isdir("cache"):
        os.makedirs("cache")

    # Recuperar a lista de músicas do servidor
    songs_list = client_socket.recv(1024).decode()
    print("Lista de músicas disponíveis:")
    print(songs_list)

    # Escolher uma música para reproduzir
    song_choice = input("Digite o nome da música que deseja reproduzir: ")
    client_socket.send(song_choice.encode())

    # Verificar se a música está no cache local
    # cache_status = client_socket.recv(1024).decode()
    # if cache_status == "OK":
    #     print("Música encontrada no cache local.")
    # elif cache_status == "NOT FOUND":
    #     print("Música não encontrada no cache local. Buscando no servidor...")

    # Iniciar a reprodução da música em uma thread separada
    audio_thread = threading.Thread(target=receive_audio, args=(client_socket,))
    audio_thread.start()

    # Aguardar a reprodução da música
    audio_thread.join()

    # Fechar a conexão com o servidor
    client_socket.close()

start_client()
