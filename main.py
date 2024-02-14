import requests
import bs4
from urllib.parse import quote

title = 'Ин'
encoded = quote(title)

headers = {
    'authority': 'cosmobase.ru',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://cosmobase.ru',
    'referer': 'https://cosmobase.ru/handbook',
    'sec-ch-ua': '"Chromium";v="118", "YaBrowser";v="23", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.971 '
                  'YaBrowser/23.11.3.971 (beta) Yowser/2.5 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = f'hbSearch={encoded}&hbGroup=0&hlbFrom=&hlbTo=&factor=&hbEffects=0&hbSkin=0&hbNatural=false&lookDesc=false&start=0&searchType=standart'

url = 'https://cosmobase.ru/handbook/search'

response = requests.post(url, headers=headers, data=data)

response_json = response.json()

if response_json['status'] != 'success':
    print('Status is not "success"')
else:
    response_data = response_json['data']
    soup = bs4.BeautifulSoup(response_data, "html.parser")
    result = soup.select('a.componentLink')

    uris = []

    for i in result:
        uris.append(i.attrs.get('href'))

    for uri in uris:
        current_url = f'https://cosmobase.ru/{uri}'
        print(current_url)
        current_response = requests.get(current_url)
        f = open(f'../{uri.split("/")[-1]}.html', 'w')
        f.write(current_response.text)
        f.close()
