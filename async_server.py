
import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup
import aiofiles

async def get_item(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            a = await response.text()
            soup = BeautifulSoup(a, 'html.parser')
            product_elements = soup.find_all('div', class_='set-card block')
            for i in product_elements:
                with open('data.txt', 'w') as file:
                    a = soup.find_all('a', class_='di_b c_b')
                    #file.write("a")
            #return product_elements

async def main():
    a = await get_item("https://dental-first.ru/catalog/stomatologicheskie-materialy/plombirovochnye-materialy-shpritsy/shpritsy-estelite-/estelite-posterior/")
    print(a)

async def handler(request):
    await get_item("https://dental-first.ru/catalog/stomatologicheskie-materialy/plombirovochnye-materialy-shpritsy/shpritsy-estelite-/estelite-posterior/")
    data = []
    return web.json_response(data)

app = web.Application()
app.router.add_get('/', handler)

def server():
    web.run_app(app, host='127.0.0.1', port=8080)

if __name__ == '__main__':
    server()