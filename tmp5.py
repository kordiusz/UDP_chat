import asyncio

counter = 0  # zmienna współdzielona

async def race_increment():
    global counter
    temp = counter
    await asyncio.sleep(0.1)  # symuluje przełączenie kontekstu
    counter = temp + 1

async def main():
    global counter
    counter = 0
    tasks = [race_increment() for _ in range(1000)]
    await asyncio.gather(*tasks)
    print(f"Bez locka: counter = {counter}")

asyncio.run(main())
