

respone = aiohttp.ClientSession().get("")
text = await response.json()
soup = BeautifulSoup(response.content, 'html.parser')
product_elements = soup.find_all('div', class_='set-card block')
