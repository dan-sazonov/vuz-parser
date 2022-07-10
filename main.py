import requests
from bs4 import BeautifulSoup

import config

c = config.ColorMethods()


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


class GUAP:
    def __init__(self):
        self.univer_name = 'ГУАП'
        self.interesting = {
            'Информационные системы и технологии': ('https://priem.guap.ru/_lists/List_1698_14', 42),
            'Информатика и вычислительная техника': ('https://priem.guap.ru/_lists/List_1693_14', 79),
            "Прикладная математика и информатика": ("https://priem.guap.ru/_lists/List_1370_14", 16),
            "Математическое обеспечение и администрирование информационных систем": (
                "https://priem.guap.ru/_lists/List_1404_14", 12),
            "Прикладная информатика": ("https://priem.guap.ru/_lists/List_1413_14", 126),
            "Программная инженерия": ("https://priem.guap.ru/_lists/List_1414_14", 42),
            "Информационная безопасность": ("https://priem.guap.ru/_lists/List_1415_14", 42),
            "Инфокоммуникационные технологии и системы связи": ("https://priem.guap.ru/_lists/List_1694_14", 84),
            "Управление в технических системах": ("https://priem.guap.ru/_lists/List_1385_14", 21),
            "Инноватика": ("https://priem.guap.ru/_lists/List_1384_14", 16),
        }
        self.predefined_data = []  # for future versions

    def scrap(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        data_raw = str(soup.select('#tablestat tbody')[0])
        data_arr = self.predefined_data.copy()

        for abt in data_raw.split('</tr><tr class="warning">'):
            data_arr.append(int(abt.split('</td><td>')[2]))

        return sorted(data_arr, reverse=True)

    #  да, я слышал про DRY. Интересно, почему код должен быть сухим?
    def get(self):
        for spec in self.interesting:
            last_point, highest_place, usr_place = format_arr(self.scrap(self.interesting[spec][0]),
                                                              self.interesting[spec][1])
            print(f"{spec}: {last_point}; {usr_place}-{highest_place}/{self.interesting[spec][1]}")


class LETI:
    def __init__(self):
        self.univer_name = 'ЛЭТИ'
        self.interesting = {
            'Инфокоммуникационные технологии и системы связи': ('https://abit.etu.ru/ru/postupayushhim/bakalavriat-i-specialitet/spiski-podavshih-zayavlenie/spisok-postupayushhih?list=4-183', 70)
        }
        self.predefined_data = []  # for future versions

    def scrap(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        data_raw = str(soup.select('#accepted-application tbody'))
        data_arr = self.predefined_data.copy()

        for abt in data_raw.split('</tr>\n<tr>'):
            abt = BeautifulSoup(abt, 'lxml')
            if abt.select('.group')[0].text == 'ОК':
                data_arr.append(int(abt.select('.ball')[0].text))

        return sorted(data_arr, reverse=True)

    def get(self):
        for spec in self.interesting:
            last_point, highest_place, usr_place = format_arr(self.scrap(self.interesting[spec][0]),
                                                              self.interesting[spec][1])
            print(f"{spec}: {last_point}; {usr_place}-{highest_place}/{self.interesting[spec][1]}")


class SPBGEU:
    def __init__(self):
        self.univer_name = 'СПбГЭУ'
        self.interesting = {
            'Информационная безопасность': ('https://priem.unecon.ru/stat/stat_konkurs.php?filial_kod=1&zayav_type_kod=1&obr_konkurs_kod=0&recomend_type=null&rec_status_kod=all&ob_forma_kod=1&ob_osnova_kod=1&konkurs_grp_kod=4245&prior=all&status_kod=all&has_agreement=all&show=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C', 6)
        }
        self.predefined_data = []  # for future versions

    def scrap(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        data_raw = str(soup.select('tbody')[1])
        data_arr = self.predefined_data.copy()

        for abt in data_raw.split('</tr><tr'):
            data_arr.append(int(abt.split('</td><td')[4].strip('>')))

        return sorted(data_arr, reverse=True)

    def get(self):
        for spec in self.interesting:
            last_point, highest_place, usr_place = format_arr(self.scrap(self.interesting[spec][0]),
                                                              self.interesting[spec][1])
            print(f"{spec}: {last_point}; {usr_place}-{highest_place}/{self.interesting[spec][1]}")


def main():
    usr_input = int(input('Введите номер вуза: '))
    universities = {
        1: GUAP,
        2: LETI,
        3: SPBGEU
    }
    if usr_input in universities.keys():
        univer = universities[usr_input]()
        print(univer.univer_name)
        univer.get()


if __name__ == '__main__':
    main()
