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


def format_arr(arr, adm_amount):
    last_point = arr[adm_amount]
    highest_place = 0
    usr_place = 0
    for i in range(len(arr)):
        if not highest_place and arr[i] <= config.TOTAL_POINTS:
            highest_place = i + 1
        if arr[i] < config.TOTAL_POINTS:
            usr_place = i + 1
            break

    return last_point, highest_place, usr_place


def get_guap():
    specialties = {
        'Информационные системы и технологии': ('https://priem.guap.ru/_lists/List_1698_14', 42),
        'Информатика и вычислительная техника': ('https://priem.guap.ru/_lists/List_1693_14', 79)
    }
    for spec in specialties:
        # points = scrap_guap(specialties[spec][0])
        # last_point = points[specialties[spec][1]]
        last_point, highest_place, usr_place = format_arr(scrap_guap(specialties[spec][0]), specialties[spec][1])
        print(f"{spec}: {last_point}; {usr_place}-{highest_place}/{specialties[spec][1]}")


def main():
    usr_input = int(input('Введите номер вуза: '))
    if usr_input == 1:
        get_guap()


if __name__ == '__main__':
    main()
