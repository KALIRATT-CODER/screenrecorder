import socket
import os

SERVER_IP = "127.0.0.1"  # À changer par l'IP de ton PC
SERVER_PORT = 9999

def send_file(filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    
    # Envoie le nom
    s.send(filename.encode())
    s.recv(1024)
    
    # Envoie la taille
    s.send(str(filesize).encode())
    s.recv(1024)
    
    # Envoie le fichier
    with open(filepath, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            s.send(data)
    
    s.close()
    print(f"[+] Fichier envoyé : {filename}")

# Test avec la dernière vidéo enregistrée
if __name__ == "__main__":
    for f in os.listdir("recordings"):
        filepath = os.path.join("recordings", f)
        send_file(filepath)