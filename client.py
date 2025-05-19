# client.py

# importam socket pt conexiunea cu serverul si threading pt a primi mesaje in paralel
import socket
import threading

# IP-ul si portul serverului la care ne conectam (localhost sau IP din retea)
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345


# functie care asculta si afiseaza mesajele primite de la server
def receive_messages(sock):
    while True:
        try:
            # primim mesajul de la server si il decodam
            message = sock.recv(1024).decode()
            if not message:
                print("🔌 Serverul s-a inchis.")
                break
            # afisam mesajul pe ecran
            print(message.strip())
        except:
            # daca conexiunea s-a inchis fortat
            print("❌ Conexiune intrerupta.")
            break


# functia principala a clientului
def main():
    # cream un socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # incercam sa ne conectam la server
        client_socket.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print(f"[!] Eroare la conectare: {e}")
        return

    # pornim un thread separat care va asculta mesaje de la server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    #target = fct care va fi rulata in thread
    #argumentele transmise functiei
    #daemon thread ul se inchide automat cand programul principal se inchide 
    receive_thread.start()

    print("🎮 Poti incepe sa trimiti incercari (ex: 1234)\n")

    while True:
        try:
            # citim un input de la utilizator
            guess = input("> Trimite un numar: ").strip()
            # verificam daca este valid: 4 cifre diferite
            if len(guess) == 4 and guess.isdigit() and len(set(guess)) == 4:
                # trimitem catre server
                client_socket.sendall(guess.encode())
            else:
                print("❗ Introdu exact 4 cifre diferite.")
        except KeyboardInterrupt:
            # daca apasam Ctrl+C, iesim din aplicatie
            print("\n[!] Inchidere client...")
            break
        except Exception as e:
            print(f"[!] Eroare: {e}")
            break

    # inchidem conexiunea la final
    client_socket.close()


# daca rulam fisierul direct, apelam main()
if __name__ == "__main__":
    main()
