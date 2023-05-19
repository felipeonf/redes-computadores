import socket
import threading, wave, pickle, struct





def set_server(port):
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    name_server = socket.gethostname()
    ip_server = socket.gethostbyname(name_server)
    socketServer.bind((ip_server, port))

    print(socketServer)
    print(f"Servidor sendo escutado no endereço {ip_server} e na porta {port}")
    return socketServer


def audio_stream(port):
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    name_server = socket.gethostname()
    ip_server = socket.gethostbyname(name_server)
    socketServer.bind((ip_server, port))

    print(socketServer)
    print(f"Servidor sendo escutado no endereço {ip_server} e na porta {port}")
    try:
        socketServer.listen(1)
        CHUNK = 1024
        wav_file = wave.open('beep-01a.wav', 'rb')

        # play_instance = pyaudio.PyAudio()

        # stream = play_instance.open(format=play_instance.get_format_from_width(wav_file.getsampwidth()),
        #             channels=wav_file.getnchannels(),
        #             rate=wav_file.getframerate(),
        #             input=True,
        #             frames_per_buffer=CHUNK)
        
        client_socket, addr = socketServer.accept()
        data = None

        while True:
            if client_socket:
                while True:
                    data = wav_file.readframes(CHUNK)
                    a = pickle.dumps(data)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)

    except Exception as error:
        print("Ocorreu um erro", error)




if __name__ == "__main__":
    # server = set_server(3000)
    t1 = threading.Thread(target=audio_stream(3000), args=())
    t1.start()


