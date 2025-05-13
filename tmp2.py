
import asyncio
import time
async def fetch_data(time, num):
    print(f"Fetch nr {num}")
    await asyncio.sleep(time)
    print(f"Koniec fetcha nr {num}")


async def main():
    start = time.time()

    task1 = fetch_data(1,1)
    task2 = fetch_data(2,2)
    await task1
    await task2
    
    end = time.time()
    print(f"{end-start:.2f}s")

asyncio.run(main())