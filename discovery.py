import asyncio
import json
import socket

BROADCAST_PORT = 9999
BROADCAST_INTERVAL = 2  # seconds

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def calc_broadcast(ip):
    index = ip.rfind('.')+1
    #dirty but works :)
    return ip[:index] + "255"

async def broadcast_server_info(name, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    ip = get_local_ip()
    broadcast_addr = calc_broadcast(ip)
    while True:
        message = json.dumps({"name": name, "host": ip, "port": port}).encode()
        sock.sendto(message, (broadcast_addr, BROADCAST_PORT))
        await asyncio.sleep(BROADCAST_INTERVAL)

async def listen_for_servers(callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', BROADCAST_PORT))
    sock.setblocking(False)
    loop = asyncio.get_event_loop()

    while True:
        try:
            data, addr = await loop.sock_recvfrom(sock, 1024)
            info = json.loads(data.decode())
            print(info)
            await callback(info)
        except Exception:
            pass
        await asyncio.sleep(2)
