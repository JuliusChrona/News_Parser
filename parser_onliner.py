import csv
import time
import requests
from bs4 import BeautifulSoup


MENU = {'tech.': (r'/tag/it-belarus', r'/gadgets', r'/tests', r'/tag/apple',
                  r'/games', r'/cinema', r'/tag/kriptovalyuty', r'/fun')}
SITE = 'onliner.by'
PROTOCOL = r'https://'
FILE_NAME = 'onliner'


def get_url(section, subsection):
    return f'{PROTOCOL}{section}{SITE}{subsection}'


def get_news(news_list, url):
    news_recording = []
    for news in news_list:
        date_post = news.get('data-post-date')
        news_url = f'{url}{news.a["href"]}'
        subtitle = news.find('div', 'news-tidings__subtitle') or news.find(
            'div', 'news-tiles__subtitle')
        subtitle_text = next(subtitle.stripped_strings)
        speech_tag = news.find('div', 'news-tidings__speech')
        if speech_tag:
            speech = speech_tag.string.strip()
        else:
            speech = ''
        news_recording.append({'date_post': date_post, 'news_url': news_url,
                               'subtitle': subtitle_text, 'speech': speech})
    return news_recording


def create_csv():
    with open(f'./{FILE_NAME}.csv', 'w', newline='', encoding='utf-8') as file:
        datawriter = csv.writer(file, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(['date_post'] + ['news_url'] +
                            ['subtitle'] + ['speech'])


def write_csv(news_recording):
    with open(f'./{FILE_NAME}.csv', 'a', newline='', encoding='utf-8') as file:
        datawriter = csv.writer(file, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        for news in news_recording:
            datawriter.writerow(
                [news.get('date_post')] + [news.get('news_url')] +
                [news.get('subtitle')] + [news.get('speech')]
            )


def main():
    create_csv()
    for section, subsections in MENU.items():
        for subsection in subsections:
            url = get_url(section, subsection)
            response = requests.get(f'{url}')
            soup = BeautifulSoup(response.text, 'html.parser')
            news_list = soup.find_all(attrs={'data-post-date': True})
            news_recording = get_news(news_list, url)
            write_csv(news_recording)
            time.sleep(3)


if __name__ == '__main__':
    main()
