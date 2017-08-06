# A async redis driver .just for play

## current only suport key-value operation

## only for linux

## how to start


```
from asy_redis.client import Client
import asyncio

async def task():
    cli = Client(host="127.0.0.1")
    await cli.connect()
    resp = await cli.set("test", 1)
    print(resp)
    resp = await cli.get("test1")
    print(resp)
    await cli.disconnet()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task())
    loop.close()
```