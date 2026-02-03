import socket
import threading
import time
import json
import xml.etree.ElementTree as ET

CONFIG = json.load(open("util/config.json"))

clients = {}
last_activity = {}

def log_event(text):
    tree = ET.parse("util/log.xml")
    root = tree.getroot()
    log = ET.SubElement(root, "log")
    log.text = text
    tree.write("util/log.xml")

def udp_discovery():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", CONFIG["udp_port"]))
    print(f"[UDP] Discovery attiva sulla porta {CONFIG['udp_port']}")
    while True:
        msg, addr = s.recvfrom(1024)
        if msg.decode() == "DISCOVER_AURA":
            s.sendto(b"AURA_SERVER", addr)
            print(f"[UDP] Risposta inviata a {addr}")

def handle_client(conn, addr):
    try:
        client_id = conn.recv(1024).decode()
        clients[client_id] = conn
        last_activity[client_id] = time.time()
        log_event(client_id + " connected")
        print(f"[TCP] {client_id} connesso da {addr}")

        while True:
            if time.time() - last_activity[client_id] > 120:
                print(f"[TCP] {client_id} disconnesso per inattività")
                break
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                last_activity[client_id] = time.time()

                if data.upper() == "TIME":
                    conn.send(time.ctime().encode())

                elif data.upper() == "EXIT":
                    break

                elif data.upper().startswith("CHAT"):
                    parts = data.split(' ', 2)  # CHAT ID testo
                    if len(parts) < 3:
                        conn.send(b"Errore: usa CHAT <ID> <messaggio>")
                    else:
                        _, target, message = parts
                        if target in clients:
                            clients[target].send(f"{client_id}: {message}".encode())
                            print(f"[TCP] {client_id} ha inviato un messaggio a {target}")
                        else:
                            conn.send(f"Errore: utente {target} non connesso".encode())

            except:
                break

    finally:
        conn.close()
        if client_id in clients:
            del clients[client_id]
        log_event(client_id + " disconnected")
        print(f"[TCP] {client_id} disconnesso")

def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", CONFIG["tcp_port"]))
    s.listen()
    print(f"[TCP] AURA SERVER in attesa sulla porta {CONFIG['tcp_port']}...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
        print(f"[TCP] Connessione accettata da {addr}")

# AVVIO SERVER
print("=== AVVIO AURA SERVER ===")
print(f"Porte TCP: {CONFIG['tcp_port']}, UDP: {CONFIG['udp_port']}")

# Thread UDP discovery
udp_thread = threading.Thread(target=udp_discovery)
udp_thread.start()

# Thread TCP principale
tcp_server()
