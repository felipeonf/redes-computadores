import socket
import threading
import os

def handle_client(client_socket, client_address):
    print(f"Conexão estabelecida com o cliente {client_address}")

    # Recuperar a lista de músicas disponíveis no servidor
    songs = os.listdir("songs")
    songs = [song for song in songs if song.endswith(".mp3")]
    songs_str = "\n".join(songs)
    client_socket.send(songs_str.encode())

    # Receber a música escolhida pelo cliente
    song_choice = client_socket.recv(1024).decode()

    # Verificar se a música está presente no cache local
    if os.path.exists(f"cache/{song_choice}"):
        client_socket.send("OK".encode())
    else:
        client_socket.send("NOT FOUND".encode())

    # Enviar a música para o cliente em blocos de 30 segundos
    if os.path.exists(f"songs/{song_choice}"):
        with open(f"songs/{song_choice}", "rb") as song_file:
            data = song_file.read(1024)
            while data:
                client_socket.send(data)
                data = song_file.read(1024)

    # Fechar a conexão com o cliente
    client_socket.close()
    print(f"Conexão encerrada com o cliente {client_address}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8000))
    server_socket.listen(5)

    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

start_server()
