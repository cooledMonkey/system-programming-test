
import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup
import aiofiles

async def get_item(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            name_blocks = soup.find_all('a', class_='di_b c_b')
            for i in name_blocks:
                title = str(i.contents[0])
                async with aiofiles.open("data_async.txt", 'a') as file:
                    await file.write(title + "\n")

async def handler(request):
    url = request.query.get('url')
    await get_item(url)
    return web.json_response()

app = web.Application()
app.router.add_get('/', handler)

def server():
    web.run_app(app, host='127.0.0.1', port=8080)

if __name__ == '__main__':
    server()