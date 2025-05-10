import socket

BROADCAST_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('', BROADCAST_PORT))  # '' = wszystkie interfejsy

print(f"Nasłuchiwanie broadcastów na porcie {BROADCAST_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"[ODBIÓR] Od {addr}: {data.decode(errors='ignore')}")
