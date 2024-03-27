import os
import asyncio
from dotenv import load_dotenv
import redis.asyncio as async_redis

load_dotenv()


async def get_available_redis_streams(
    redis_server: async_redis.StrictRedis, streams: str = None
) -> list:
    i = 0
    all_streams = list()
    while True:
        i, streams = await redis_server.scan(i, _type="STREAM")
        all_streams += streams
        if i == 0:
            return all_streams


async def clear_streams():
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_client = async_redis.Redis(
        host=redis_host, port=redis_port, decode_responses=True
    )
    streams = await get_available_redis_streams(redis_client)
    for stream in streams:
        await redis_client.delete(stream)
        print(f"Cleared {stream} stream")


loop = asyncio.get_event_loop()
loop.run_until_complete(clear_streams())
