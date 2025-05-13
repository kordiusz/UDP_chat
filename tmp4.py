import asyncio
import time
lock = asyncio.Lock()

#lock kontrolujemy przez acquire i release. Lub blokiem with.
shared_res = 0
async def modify_shared():
    global shared_res
    async with lock:
        print(f"przed modyfikacja: {shared_res}")
        shared_res += 1
        await asyncio.sleep(1)
        print(f"Po modyfikcaji: {shared_res}")

async def main():
    start = time.time()
    await asyncio.gather(*[modify_shared() for _ in range(5)])
    end = time.time()
    print(f"{end-start:.2f}s")

asyncio.run(main())