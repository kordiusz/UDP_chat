import asyncio
import socket
import json
import time

class Server:

    def __init__(self):
        self.clients = set()  # Set of (ip, port)
        self.BROADCAST_PORT = 9999
        self.BROADCAST_INTERVAL = 2
        self.communication_port = 8888
        self.messages = []
        self.ip = ""
        self.brsock = None

    def calc_broadcast(self, ip):
        index = ip.rfind('.') + 1
        return ip[:index] + "255"

    async def broadcast_server(self, name):
        self.brsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.brsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.brsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        broadcast_addr = self.calc_broadcast(self.ip)

        while True:
            message = json.dumps({
                "name": name,
                "host": self.ip,
                "port": self.communication_port
            }).encode()
            self.brsock.sendto(message, (broadcast_addr, self.BROADCAST_PORT))
            print(f"[BROADCAST] {name} @ {self.ip}:{self.communication_port}")
            await asyncio.sleep(self.BROADCAST_INTERVAL)

    async def handle_messages(self):
        loop = asyncio.get_event_loop()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.communication_port))


        print(f"[LISTENING] UDP socket on {self.ip}:{self.communication_port}")

        while True:
            try:
                data, addr = await loop.sock_recv(sock, 1024)
                message = data.decode('utf-8')
                print(f"[RECV] From {addr}: {message}")

                if addr not in self.clients:
                    self.clients.add(addr)
                    print(f"[NEW CLIENT] {addr}")

                self.messages.append((time.time(), addr, message))
                await self.spread_new_msg(sock, message, sender=addr)

            except Exception as e:
                print(f"[ERROR] {e}")


    async def spread_new_msg(self, sock, msg, sender=None):
        for client in self.clients:
            sock.sendto(msg.encode('utf-8'), client)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

async def main():
    server = Server()
    server.ip = get_local_ip()
    name = "MojCzatUDP"

    await asyncio.gather(
        server.broadcast_server(name),
        server.handle_messages(),
    )

asyncio.run(main())
