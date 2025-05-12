import asyncio

# ZADANIE 5 Anulowanie zadania
# Uzupełnij kod, aby po 2 sekundach anulował działanie funkcji dlugie_zadanie.

async def dlugie_zadanie():
    try:
        print("Startuję")
        await asyncio.sleep(5)
        print("Zakończone")
    except asyncio.CancelledError:
        print("Zadanie anulowane")

async def main():
    task = asyncio.create_task(dlugie_zadanie())
    await asyncio.sleep(2)
    # task.cancel()
    # await task

asyncio.run(main())
