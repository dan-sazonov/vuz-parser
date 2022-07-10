import config
import requests
from bs4 import BeautifulSoup

c = config.ColorMethods()


def scrap_guap():
    url = 'https://priem.guap.ru/_lists/List_1693_14'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data_raw = str(soup.select('#tablestat tbody')[0])
    data_arr = []

    for abt in data_raw.split('</tr><tr class="warning">'):
        data_arr.append(int(abt.split('</td><td>')[2]))

    return sorted(data_arr, reverse=True)


def main():
    print(scrap_guap())


if __name__ == '__main__':
    main()
