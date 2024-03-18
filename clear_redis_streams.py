import asyncio
import redis.asyncio as async_redis


async def get_available_redis_streams(
    redis_server: async_redis.StrictRedis, streams: str = None
) -> list:
    i = 0
    all_streams = list()
    while True:
        i, streams = await redis_server.scan(i, _type="STREAM", match=streams)
        all_streams += streams
        if i == 0:
            return all_streams


async def clear_streams():
    redis_host = helpers.HOST
    redis_port = helpers.REDIS_PORT
    redis_client = async_redis.Redis(
        host=redis_host, port=redis_port, decode_responses=True, ssl=True
    )
    streams = await helpers.get_available_redis_streams(redis_client)
    for stream in streams:
        await redis_client.delete(stream)
        print(f"Cleared {stream} stream")


asyncio.run(clear_streams())
