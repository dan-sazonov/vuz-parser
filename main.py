import requests
from bs4 import BeautifulSoup

import config

c = config.ColorMethods()


def scrap_guap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data_raw = str(soup.select('#tablestat tbody')[0])
    data_arr = []

    for abt in data_raw.split('</tr><tr class="warning">'):
        data_arr.append(int(abt.split('</td><td>')[2]))

    return sorted(data_arr, reverse=True)


def get_guap():
    specialties = {
        'Информационные системы и технологии': 'https://priem.guap.ru/_lists/List_1698_14',
        'Информатика и вычислительная техника': 'https://priem.guap.ru/_lists/List_1693_14'
    }
    for spec in specialties:
        print(f"{spec}: {scrap_guap(specialties[spec])}")


def main():
    usr_input = int(input('Введите номер вуза: '))
    if usr_input == 1:
        get_guap()


if __name__ == '__main__':
    main()
