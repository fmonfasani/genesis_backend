import asyncio

async def send_request(*args, **kwargs):
    await asyncio.sleep(0)
    class Response:
        result = ""
        success = True
    return Response()
