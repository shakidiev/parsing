import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='col-sm-16').find_all('a')[-1].get('href')
    total_pages = pages.split('=')[-1]

    return int(total_pages)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='col-sm-16').find_all('div',
                                                        class_='thumbnail')

    for ad in ads:
        # project,stage,website,date_published

        try:
            project = ad.find('div', class_='caption').find('h3').text
        except:
            project = ''

        try:
            stage = ad.find('div', class_='caption').find(
                'p', class_='startup-stage').text
        except:
            stage = ''

        data = {'project': project, 'stage': stage}
        return data


def write_csv(data):

    with open('startups.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['project'], data['stage']))
        print(data['project'], data['stage'])


def main():
    url = 'https://www.allstartups.info/Startups'
    page_part = 'p='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages):
        url_gen = url + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        data = get_page_data(html)
        write_csv(data)


if __name__ == '__main__':
    main()
