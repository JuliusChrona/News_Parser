from bs4 import BeautifulSoup
import requests as req
import csv

CATEGORIES = {
    'main': 'daynews/',
    'minsk': 'geonews/minsk/',
    'exclusive': 'top5news/',
    'economics': 'economics/',
    'society': 'society/',
    'world': 'world/',
    'culture': 'culture/',
    'accidents': 'accidents/',
    'auto': 'auto/'
}

HOST = "https://news.tut.by/"
HEADERS  = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def makeurl(*args):
    return "".join(args)

def get_content(url, category):
    response = req.get(url, headers=HEADERS)

    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.find_all('div', class_="news-entry big annoticed time ni")

    content = []
    for n in news:

        title = n.find('span', class_='entry-head _title').text
        description = n.find('span', class_='entry-note').text
        linux_date = n.find('span', class_='entry-time').span['data-ctime']
        preview_url = n.find('span', class_='entry-pic').img['src']
        n_url = n.find('a', class_='entry__link')['href']


        print(f"Append {title} - {category} in content")
        content.append(
            {
                'title': title,
                'description': description,
                'category': category,
                'date': linux_date,
                'preview_url': preview_url,
                'url': n_url
            })

    return content


def create_csv():
    with open('tutby.csv', 'w', newline='', encoding='utf-8') as file:
        datawriter = csv.writer(file, delimiter=',')
        datawriter.writerow(
                ['title', 'description', 'category', 'date', 'preview_url', 'url']
                )


def write_csv(data):
    with open('tutby.csv', 'a', newline='', encoding='utf-8') as file:
        datawriter = csv.writer(file, delimiter=',')
        for news in data:
            datawriter.writerow(
                [news['title'], news['description'], news['category'], news['date'], news['preview_url'], news['url']]
            )



def main():
    create_csv()
    for category in CATEGORIES:
        url = makeurl(HOST, CATEGORIES[category])
        data = get_content(url, category)
        write_csv(data)


if __name__ == '__main__':
    main()
