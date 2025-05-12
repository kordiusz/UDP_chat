import asyncio
import random

# ZADANIE 2 Równoległe zadania z opóźnieniami, uporządkowane wyniki
# Zmodyfikuj funkcję tak, aby wyniki były zwracane i sortowane rosnąco mimo równoległego uruchomienia.

async def oblicz(i):
    await asyncio.sleep(random.uniform(0.1, 1))
    return i * i

async def main():
    # tasks = [asyncio.create_task(oblicz(i)) for i in range(5)]
    # wyniki = await asyncio.gather(*tasks)
    # wyniki.sort()
    # print("Posortowane wyniki:", wyniki)

asyncio.run(main())
