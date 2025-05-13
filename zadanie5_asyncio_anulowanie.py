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
    # uzupełnij kod
    await asyncio.sleep(2) 
    # uzupełnij kod

asyncio.run(main())
