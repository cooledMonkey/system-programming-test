import asyncio

import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup
import aiofiles

total_total_price = 0.0
price_lock = asyncio.Lock()


async def get_item(url):
    global total_total_price
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            name_blocks = soup.find_all('a', class_='di_b c_b')
            total_price = 0.0
            total_text = ""
            for i in name_blocks:
                total_text += str(i.contents[0]) + "\n"
            async with aiofiles.open("data_async.txt", 'a') as file:
                await file.write(total_text)
            for i in soup.find_all('span', class_='set-card__price'):
                total_price += float((i.get_text(strip=True)).replace("₽", "").split()[0])
    async with price_lock:
        total_total_price += total_price
    return total_price


async def handler(request):
    url = request.query.get('url')
    total_prices = await get_item(url)
    return web.json_response(total_prices)


app = web.Application()
app.router.add_get('/', handler)


def server():
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    server()
