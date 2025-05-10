import socket
import asyncio
import json

BROADCAST_PORT = 9999

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setblocking(False)  
        self.sock.bind(('', BROADCAST_PORT))
        print(f"Nasłuchiwanie broadcastów na porcie {BROADCAST_PORT}...")

    async def loop(self):
        loop = asyncio.get_event_loop()
        data = await loop.sock_recv(self.sock, 1024)
        decoded = json.loads(data.decode())
        print(f"[ODBIÓR] Od : {data.decode(errors='ignore')}. Wyslij cos.")
        await asyncio.gather(
            self.handle_receive(decoded['name'], decoded['host'], decoded['port']),
            self.handle_send(decoded['name'], decoded['host'], decoded['port'])
        )

    async def handle_receive(self, name, host, port):
        loop = asyncio.get_event_loop()
        servsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servsock.setblocking(False)
        servsock.bind(('', 0))
        while True:
            data, addr = await loop.sock_recvfrom(servsock, 1024)
            print(f"Odebrano od {addr}: {data.decode(errors='ignore')}")

    async def handle_send(self, name, host, port):
        loop = asyncio.get_event_loop()
        servsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servsock.setblocking(False)
        while True:
            content = await asyncio.to_thread(input, ": ")
            await loop.sock_sendto(servsock, content.encode(), (host, int(port)))

if __name__ == "__main__":
    c = Client()
    asyncio.run(c.loop())
