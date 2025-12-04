from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_item(url):
    response = requests.get(url)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    name_blocks = soup.find_all('a', class_='di_b c_b')
    for i in name_blocks:
        title = str(i.contents[0])
        with open('data_threading.txt', 'a') as file:
            file.write(title + "\n")

@app.route('/')
def handler():
    url = request.args.get('url')
    get_item(url)
    return jsonify("200 OK")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, threaded=True)
