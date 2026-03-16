import socket
import os

HOST = "0.0.0.0"  # Écoute sur toutes les interfaces
PORT = 9999
SAVE_DIR = "received"

os.makedirs(SAVE_DIR, exist_ok=True)

def receive_file(conn):
    # Reçoit le nom du fichier
    filename = conn.recv(1024).decode().strip()
    conn.send(b"OK")
    
    # Reçoit la taille du fichier
    filesize = int(conn.recv(1024).decode().strip())
    conn.send(b"OK")
    
    # Reçoit le fichier
    filepath = os.path.join(SAVE_DIR, filename)
    with open(filepath, "wb") as f:
        received = 0
        while received < filesize:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)
            received += len(data)
    
    print(f"[+] Fichier reçu : {filepath}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"[*] Serveur en écoute sur le port {PORT}...")

while True:
    conn, addr = server.accept()
    print(f"[+] Connexion de {addr}")
    receive_file(conn)
    conn.close()