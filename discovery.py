import asyncio
import json
import socket

BROADCAST_PORT = 9999
BROADCAST_INTERVAL = 2  # seconds

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

async def broadcast_server_info(name, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    ip = get_local_ip()

    while True:
        message = json.dumps({"name": name, "host": ip, "port": port}).encode()
        sock.sendto(message, ('<broadcast>', BROADCAST_PORT))
        sock.sendto(message, ('127.0.0.1', BROADCAST_PORT))
        await asyncio.sleep(BROADCAST_INTERVAL)

async def listen_for_servers(callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', BROADCAST_PORT))
    sock.setblocking(False)
    loop = asyncio.get_event_loop()

    while True:
        try:
            data, addr = await loop.sock_recvfrom(sock, 1024)
            info = json.loads(data.decode())
            await callback(info)
        except Exception:
            pass
        await asyncio.sleep(2)
