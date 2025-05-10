import asyncio
clients = set()

async def handle_client(reader, writer):
    clients.add(writer)
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode()
            for client in clients:
                if client != writer:
                    client.write(message.encode())
                    await client.drain()
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def start_chat_server(host='0.0.0.0', port=8888):
    server = await asyncio.start_server(handle_client, host, port)
    print(f"[SERVER] Running on {host}:{port}")
    async with server:
        await server.serve_forever()

