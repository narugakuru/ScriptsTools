import asyncio

async def fetch_data(n):
    print(f"Start fetching {n}")
    await asyncio.sleep(2)  # 模拟网络请求
    print(f"Finished fetching {n}")
    return f"Data {n}"

async def main():
    # 并发执行三个 fetch_data 任务
    tasks = [fetch_data(1), fetch_data(2), fetch_data(3)]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
