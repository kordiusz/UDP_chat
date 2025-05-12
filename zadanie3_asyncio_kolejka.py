import asyncio

# ZADANIE 3 Producent i konsument z ograniczoną kolejką
# Uzupełnij kod, by producent nie dodawał więcej niż 2 elementy jednocześnie (kolejka maxsize=2).

async def producent(q):
    for i in range(5):
        await q.put(i)
        print("Dodano:", i)

async def konsument(q):
    for _ in range(5):
        item = await q.get()
        print("Odebrano:", item)
        await asyncio.sleep(0.5)

async def main():
    # q = asyncio.Queue(maxsize=2)
    # await asyncio.gather(producent(q), konsument(q))

asyncio.run(main())
