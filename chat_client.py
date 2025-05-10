import asyncio
import sys

async def read_messages(reader):
    while True:
        data = await reader.readline()
        if not data:
            break
        print(data.decode().strip())

async def send_messages(writer):
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(None, sys.stdin.readline)
        writer.write(message.encode())
        await writer.drain()

async def run_chat_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    print("[CLIENT] Connected. Start chatting:")
    await asyncio.gather(read_messages(reader), send_messages(writer))

