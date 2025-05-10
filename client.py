
import socket

BROADCAST_PORT = 9999

class Client:

    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('', BROADCAST_PORT))  # '' = wszystkie interfejsy

        print(f"Nasłuchiwanie broadcastów na porcie {BROADCAST_PORT}...")
    def loop(self):
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"[ODBIÓR] Od {addr}: {data.decode(errors='ignore')}")


if __name__ =="__main__":
    c = Client()
    c.loop()