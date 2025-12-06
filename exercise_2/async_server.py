import asyncio

from aiohttp import web
import aiofiles
import os


async def get_str_count(file_name):
    async with aiofiles.open(file_name, 'rb') as f:
        count = 0
        async for _ in f:
            count += 1
    return count


async def analyze_file_async(file_name):
    return await get_str_count(file_name)


async def handler(request):
    files = []
    dir_name = request.query.get('dir_name')
    directory = os.fsencode(dir_name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            files.append(dir_name + "/" + filename)
    results = await asyncio.gather(*(analyze_file_async(file_path) for file_path in files))
    result = sum(results)
    return web.json_response(result)


app = web.Application()
app.router.add_get('/', handler)


def server():
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    server()
