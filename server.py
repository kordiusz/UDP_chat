import asyncio
import socket
import json
import time

BROADCAST_PORT = 9999
COMMUNICATION_PORT = 8888
BROADCAST_INTERVAL = 2

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

            # Send to all other clients
            for client in self.clients:
                if client != addr:
                    self.transport.sendto(data, client)

        except Exception as e:
            print(f"[ERROR] decoding message: {e}")

async def broadcast_server(ip, name):
    loop = asyncio.get_running_loop()

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

    # Start the server
    print(f"[STARTING] UDP Chat Server on {ip}:{COMMUNICATION_PORT}")
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ChatProtocol(),
        local_addr=(ip, COMMUNICATION_PORT)
    )

    try:
        await broadcast_server(ip, name)  # never-ending
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
