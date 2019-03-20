import aiohttp
import asyncio

async def main():
    # 好像必须写一个并发数，否则无法return
    # async with asyncio.Semaphore(5):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://baidu.com") as html:
                response = await html.text(encoding = 'utf-8')
                print(response)
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
