
import asyncio
import time
async def fetch_data(time, num):
    print(f"Fetch nr {num}")
    await asyncio.sleep(time)
    print(f"Koniec fetcha nr {num}")
    return f"Wynik {num}"


async def main():
    start = time.time()

    evaluated = await asyncio.gather(fetch_data(2,1), fetch_data(3,2), fetch_data(1,3))
    for result in evaluated:
        print(result)
    end = time.time()
    print(f"{end-start:.2f}s")

asyncio.run(main())