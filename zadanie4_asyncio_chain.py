import asyncio

# ZADANIE 4 Chain coroutine (jedna funkcja wywołuje kolejną)
# Uzupełnij kod tak, by outer() czekało na inner() i wypisało wynik jej działania.

async def inner():
    await asyncio.sleep(1)
    return "zakończono inner"

async def outer():
    # wynik = await inner()
    # print("Wynik:", wynik)

asyncio.run(outer())
