import asyncio
import socket
import json
import aiofiles
from datetime import datetime

BROADCAST_PORT = 9999
COMMUNICATION_PORT = 8888
BROADCAST_INTERVAL = 2
LOG_INTERVAL = 10  # co ile sekund zapisywać logi
LOG_FILE = "chat_log.txt"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

def calc_broadcast(ip):
    index = ip.rfind('.') + 1
    return ip[:index] + "255"

class ChatProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.clients = set()
        self.message_buffer = []
        self.lock = asyncio.Lock()

    def connection_made(self, transport):
        self.transport = transport
        print("[SERVER] UDP server started.")

    def datagram_received(self, data, addr):
        try:
            message = data.decode()
            print(f"[RECV] From {addr}: {message}")

            if addr not in self.clients:
                self.clients.add(addr)
                print(f"[NEW CLIENT] {addr}")
                info = {"type": "admin", "msg": "NOWA OSOBA DOLACZA"}
                for client in self.clients:
                    if client != addr:
                        self.transport.sendto(json.dumps(info).encode(), client)

            # Log the message
            asyncio.create_task(self.add_to_buffer(message))

            # Relay message to all other clients
            for client in self.clients:
                if client != addr:
                    self.transport.sendto(data, client)

        except Exception as e:
            print(f"[ERROR] decoding message: {e}")

    async def add_to_buffer(self, message):
        async with self.lock:
            self.message_buffer.append(message)

    async def save_logs_periodically(self):
        while True:
            await asyncio.sleep(LOG_INTERVAL)
            await self.save_logs_to_file()

    async def save_logs_to_file(self):
        async with self.lock:
            if self.message_buffer:
                async with aiofiles.open(LOG_FILE, "a", encoding="utf-8") as f:
                    for msg in self.message_buffer:
                        await f.write(f"{msg}\n")
                print(f"[LOG] Zapisano {len(self.message_buffer)} wiadomości do {LOG_FILE}")
                self.message_buffer.clear()

async def broadcast_server(ip, name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setblocking(False)

    broadcast_ip = calc_broadcast(ip)
    message = json.dumps({
        "name": name,
        "host": ip,
        "port": COMMUNICATION_PORT
    }).encode()

    while True:
        sock.sendto(message, (broadcast_ip, BROADCAST_PORT))
        print(f"[BROADCAST] {name} @ {ip}:{COMMUNICATION_PORT}")
        await asyncio.sleep(BROADCAST_INTERVAL)

async def main():
    ip = get_local_ip()
    name = "MojCzatUDP"

    print(f"[STARTING] UDP Chat Server on {ip}:{COMMUNICATION_PORT}")
    loop = asyncio.get_running_loop()
    protocol_instance = ChatProtocol()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: protocol_instance,
        local_addr=(ip, COMMUNICATION_PORT)
    )

    # Start logging task
    asyncio.create_task(protocol_instance.save_logs_periodically())

    try:
        await broadcast_server(ip, name)
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
