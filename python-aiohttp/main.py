import aiohttp
import asyncio


def url(port: int, scenario: int):
    return f'http://localhost:{port}/{scenario}'


# request creation code is intentionally not shared across scenarios
async def scenario1(session: aiohttp.ClientSession, port: int):
    async def req():
        async with session.get(url(port, 1)) as response:
            return await response.text()

    req1 = asyncio.create_task(req())
    req2 = asyncio.create_task(req())
    reqs = [req1, req2]
    done, pending = await asyncio.wait(reqs, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return await list(done)[0]

# not working
async def scenario2(session: aiohttp.ClientSession, port: int):
    async def req():
        async with session.get(url(port, 2)) as response:
            return await response.text()

    req1 = asyncio.create_task(req())
    req2 = asyncio.create_task(req())
    reqs = [req1, req2]
    done, pending = await asyncio.wait(reqs, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return await list(done)[0]


# currently not working
async def scenario3(session: aiohttp.ClientSession, port: int):
    async def req():
        async with session.get(url(port, 3)) as response:
            return await response.text()

    try:
        async with asyncio.timeout(5):  # temporary timeout to avoid blocking here
            reqs = [asyncio.create_task(req()) for _ in range(10_000)]
            iterable = await asyncio.wait(reqs, return_when=asyncio.FIRST_COMPLETED)
            done = next(iterable)
            print(done)
            return await done
    except asyncio.exceptions.TimeoutError:
        return "wrong"


# currently not working
async def scenario4(session: aiohttp.ClientSession, port: int):
    async def req():
        async with session.get(url(port, 4)) as response:
            return await response.text()

    req1 = asyncio.create_task(req())
    req2 = asyncio.wait_for(asyncio.create_task(req()), timeout=1)
    reqs = [req1, req2]

    done, pending = await asyncio.wait(reqs, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return await list(done)[0]


# note: this does not cancel any other losers
async def scenario5(session: aiohttp.ClientSession, port: int):
    async def req():
        async with session.get(url(port, 5)) as response:
            if response.status != 200:
                raise Exception("invalid response")
            return await response.text()

    req1 = asyncio.create_task(req())
    req2 = asyncio.create_task(req())
    results = await asyncio.gather(req1, req2, return_exceptions=True)

    for result in results:
        if not isinstance(result, Exception):
            return result


async def scenario6(session: aiohttp.ClientSession, port: int):
    async def req():
        async with session.get(url(port, 6)) as response:
            return await response.text()

    async def hedge():
        await asyncio.sleep(3)
        return await req()

    req1 = asyncio.create_task(req())
    req2 = asyncio.create_task(hedge())
    reqs = [req1, req2]
    done, pending = await asyncio.wait(reqs, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return await list(done)[0]


# currently not working
async def scenario7(session: aiohttp.ClientSession, port: int):
    async def req():
        async with session.get(url(port, 6)) as response:
            return await response.text()

    async def hedge():
        await asyncio.sleep(3)
        return await req()

    req1 = asyncio.create_task(req())
    req2 = asyncio.create_task(hedge())
    reqs = [req1, req2]
    done, pending = await asyncio.wait(reqs, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return await list(done)[0]


async def main():
    async with aiohttp.ClientSession() as session:
        # result1 = await scenario1(session, 8080)
        # print(result1)
        #
        # result2 = await scenario2(session, 8080)
        # print(result2)
        #
        # result3 = await scenario3(session, 8080)
        # print(result3)
        #
        # result4 = await scenario4(session, 8080)
        # print(result4)
        #
        # result5 = await scenario5(session, 8080)
        # print(result5)

        result6 = await scenario6(session, 8080)
        print(result6)

        # result7 = await scenario7(session, 8080)
        # print(result7)

if __name__ == "__main__":
    asyncio.run(main())