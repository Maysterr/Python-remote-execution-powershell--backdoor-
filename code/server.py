# Potrzebne biblioteki
import socket
import threading
import firebase_admin
from firebase_admin import credentials
import socket
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid
import datetime
import json
import win32gui
import win32con
import time

# Klucze biblioteki google firebase
cred = credentials.Certificate(
    {
#your certificate
    }
)
firebase_admin.initialize_app(cred, {
#your firebase addres
})

# zmienne przechowujące aktywne połącznia i ich liczbę
connections = []
total_connections = 0

# funkcja przyjmująca nowe połącznia i je zapisująca


class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # funkcja przyjmująca dane
    def run(self):
        while self.signal:
            try:
                # przyjmowanie pakietów danych
                data = self.socket.recv(32)
            except:
                # jeżeli nie da się pobrać pakietu znaczyz że użytkowk się rozłączył.
                # podawanie tej informacji w konsoli
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                # usuwanie nowego połącznie
                connections.remove(self)
                # ustawianie zmiennej x na 0
                x = 0
                # ustwianie ścieżki do danych w bazie firebase
                ref = db.reference("ngrok/users")
                # usuwanie tych danych
                ref.delete()
                # pętla wykonywane tyle razy ile jest aktynych połączeń
                for i in connections:

                    # ustawianie ścieżki do danych w bazie firebase
                    ref = db.reference("ngrok/users")
                    # aktualizwanie tych danych i dodawanie do listy aktywne połącznia
                    ref.update({
                        "id": str(x),
                        "dt": str(i),
                    })
                    # dodawanie do zmiennej x 1
                    x = x+1
                # pętla wykonywane tyle razy ile jest aktynych połączeń
                for i in connections:
                    # wysyłanie do innych użytkowników informację aby odświeżyli swoje listy oraz podawanie im ich id
                    i.socket.sendall(str.encode("///,"+str(i.id)))
                # przerywnaie funkcji
                break
            # jeżeli dane nie są puste
            if data != "":
                # wyświetla się przyjętą wiadmość
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                # dekodowanie wiadomości
                datas = data.decode("utf-8")
                # dzielnie wiadmości na sekcje
                odb = datas.split("~")

                try:
                    print(odb[0]+" send command to  " +
                          odb[1]+" saying: "+odb[2])

                    # pętla wykonywane tyle razy ile jest aktynych połączeń
                    for client in connections:
                        # sprawdzanie czy połącznie "i" to odbiorca
                        if str(client.id) == odb[1]:
                            # wysłanie wiadmości od nadawcy do odbiory podając id na dawancy
                            client.socket.sendall(
                                str.encode(odb[0]+"~"+odb[2]))
                            print("już")
                except:
                    # wyśiwtlanie w konsoli informacji iż nie znaleziono odbiorcy
                    print("nie znaleziono odbiorcy")

# funkcja przyjmująca nowe połącznie


def newConnections(socket):
    while True:
        # przyjęcie połącznia
        sock, address = socket.accept()
        global total_connections
        # dowdawnie nowgo połącznia do listy
        connections.append(
            Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        # wysyłanie informacji w konsoli o nowycm połączniu
        print("New connection at ID " + str(connections[len(connections) - 1]))
        # dowanie 1 do zmiennej liczącej połącznia
        total_connections += 1
        # ustalanie zmiennej x na 0
        x = 0
        # ustalnie ścieżki do danych w bazie firebase
        ref = db.reference("ngrok/users")
        # usuwanie tych danych
        ref.delete()
        # pętla wykonywane tyle razy ile jest aktynych połączeń
        for i in connections:
            # ustalnie ścieżki do danych w bazie firebase
            ref = db.reference("ngrok/users")
            # aktualizowanie tych danych
            ref.push({
                "id": str(x),
                "dt": str(i),
            })

            x = x+1
        # przerwa na prztworzenie
        time.sleep(5)
        # pętla wykonywane tyle razy ile jest aktynych połączeń
        for i in connections:
            # wysyłanie do innych użytkowników informację aby odświeżyli swoje listy oraz podawanie im ich id
            i.socket.sendall(str.encode("///,"+str(i.id)))
# funkcja główna


def main():
    # pobieranie ip i portu połącznia
    host = input("Host: ")
    port = int(input("Port: "))

    # tworznie nowego wejścia na dane
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    # nasłuchiwanie
    sock.listen(5)

    # ustawianaie nowej funkcji odpowiadającej za przyjmowanie połącznień
    newConnectionsThread = threading.Thread(
        target=newConnections, args=(sock,))
    newConnectionsThread.start()


# uruchamianie funkcji main
main()
