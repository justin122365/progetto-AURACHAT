import socket
import threading

UDP_PORT = 40404
TCP_PORT = 50505

def discover_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(5)
    try:
        s.sendto(b"DISCOVER_AURA", ("<broadcast>", UDP_PORT))
        msg, addr = s.recvfrom(1024)
        return addr[0]
    except:
        print("Server non trovato via UDP")
        return None
    finally:
        s.close()

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(f"\n{data}")
        except:
            break

server_ip = discover_server()
if not server_ip:
    print("Impossibile connettersi al server")
    exit()

print(f"Server trovato: {server_ip}")

client_id = input("Inserisci ID client (c1, c2, ecc.): ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, TCP_PORT))
s.send(client_id.encode())
print("Connesso al server")

# Thread per ricevere messaggi in tempo reale
threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

while True:
    cmd = input("> ").strip()
    if not cmd:
        continue
    s.send(cmd.encode())
    if cmd.upper() == "EXIT":
        break

s.close()
print("Client chiuso")
