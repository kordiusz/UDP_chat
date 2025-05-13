import asyncio

async def fetch_data(time):
    print("Poczatek")
    await asyncio.wait(time)
    print("Koniec")


print(fetch_data(2))