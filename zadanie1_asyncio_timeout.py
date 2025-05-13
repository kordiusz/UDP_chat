import asyncio

# ZADANIE 1 Oczekiwanie na coroutine z timeoutem
# Uzupełnij kod tak, by asyncio.wait_for ograniczało czas wykonania zadanie() do 2 sekund.

async def zadanie():
    await asyncio.sleep(5)
    print("Zakończone")

async def main():
    # uzupełnij kod

asyncio.run(main())
