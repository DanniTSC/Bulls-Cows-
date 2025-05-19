# server.py

# importam modulele necesare: socket pt conexiuni, threading pt clienti multipli, random pt generare numar si uuid pt ID unic
import socket
import threading
import random
import uuid

# serverul asculta pe toate interfetele
HOST = '0.0.0.0'
PORT = 12345

# lista unde tinem clientii conectati
clients = []

# dictionar unde asociem fiecare client cu un nume si numarul de incercari
players = {}  # {conn: {"name": "PlayerX", "tries": N}}

# lock pentru acces sincronizat (evitam race conditions, doar un thread va putea modifica variabila, altfel va duce la rezultate neasteptate)
lock = threading.Lock()

# variabila globala cu numarul care trebuie ghicit
target_number = ""


# functie care genereaza un numar aleator format din 4 cifre unice
def generate_number():
    digits = random.sample(range(10), 4) # 4 cifre unice de la 0 la 9
    return ''.join(str(d) for d in digits) # le converteste in string si le concateneaza  


# functie care calculeaza cate cifre sunt centrate (corecte si pe pozitia buna)
# si cate sunt necentrate (cifre corecte dar pe pozitia gresita)
def calculate_feedback(secret, guess):
    centrate = sum(a == b for a, b in zip(secret, guess))
    #zip ia cate o cifra din fiecare in perechi si le comparam
    necentrate = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - centrate
    #comparam cate aparitii are cifra comuna in guess si secret si scadem pozitiile deja corecte => cifre corecte pe pozitii gresite 
    return centrate, necentrate


# functie care trimite un mesaj tuturor clientilor conectati (broadcast)
# optional putem exclude un socket (ex: sa nu primeasca si cel care a trimis)
def broadcast(message, exclude_socket=None):
    with lock:
        for client in clients:
            if client != exclude_socket:
                try:
                    client.sendall(message.encode())
                except:
                    # daca nu merge trimiterea, scoatem clientul
                    clients.remove(client)
                    if client in players:
                        del players[client]


# functie care gestioneaza un client conectat
def handle_client(conn, addr):
    global target_number

    # generam un id unic pentru client (ex: Playerc3d9)
    player_id = f"Player{str(uuid.uuid4())[:4]}"
    with lock:
        players[conn] = {"name": player_id, "tries": 0}
        clients.append(conn)

    print(f"[+] {player_id} conectat de la {addr}")
    conn.sendall(f"Bine ai venit la Centratea, {player_id}!\n".encode())
    conn.sendall("Ghiceste un numar de 4 cifre unice.\n".encode())

    while True:
        try:
            # citim datele trimise de client
            #1024 numar maxim de bytes ce pot fi cititi de la server intr-o primire singura, buffer
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            # validam ca e un numar format din 4 cifre diferite
            if len(data) != 4 or not data.isdigit() or len(set(data)) != 4:
                conn.sendall("❗ Numarul trebuie sa aiba 4 cifre diferite.\n".encode())
                continue

            # crestem numarul de incercari pt jucatorul curent
            with lock:
                players[conn]["tries"] += 1

            # calculam feedback si il trimitem inapoi
            centrate, necentrate = calculate_feedback(target_number, data)
            conn.sendall(f"{centrate} centrate, {necentrate} necentrate\n".encode())

            # daca a ghicit toate cele 4 cifre corect
            if centrate == 4:
                name = players[conn]["name"]
                tries = players[conn]["tries"]
                win_msg = f"🎉 {name} a ghicit numarul {target_number} in {tries} incercari!\n"
                print(win_msg.strip())
                broadcast(win_msg)

                # generam un nou numar si anuntam clientii
                target_number = generate_number()
                print(f"[~] Numar nou generat: {target_number}")
                broadcast("🔁 Joc nou! Ghiciti noul numar cu 4 cifre diferite.\n")

                # resetam scorurile tuturor
                with lock:
                    for p in players.values():
                        p["tries"] = 0

        except Exception as e:
            print(f"[!] Eroare cu {players[conn]['name']}: {e}")
            break

    # curatam conexiunea cand clientul se deconecteaza
    with lock:
        if conn in clients:
            clients.remove(conn)
        if conn in players:
            print(f"[-] {players[conn]['name']} deconectat.")
            del players[conn]

    conn.close()


# functie principala care porneste serverul
def start_server():
    global target_number
    # generam numarul de ghicit
    target_number = generate_number()
    print(f"[~] Numar de ghicit: {target_number}")

    # initializam socketul
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[🔌] Server asculta pe {HOST}:{PORT}")

    # bucla infinita de acceptare clienti
    while True:
        conn, addr = server.accept()
        # cream un thread pt fiecare client
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()


# daca fisierul este rulat direct, pornim serverul
if __name__ == "__main__":
    start_server()
