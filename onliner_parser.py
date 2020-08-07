import requests
import csv
from bs4 import BeautifulSoup


HOST = 'https://tech.onliner.by/'
HEADERS  = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

def get_html(url, params=''):
	html_page = requests.get(url, params=params, headers=HEADERS)
	return html_page

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='news-tidings__item')
	news = []
	for item in items:
		try:
			news.append(
				{
				    'title': item.find('div', class_='news-tidings__subtitle').find('span').get_text(),
				    'description': item.find('div', class_='news-tidings__speech').get_text(strip=True),
				    'preview_img': item.find('div', class_='news-tidings__image').get('style').replace(');','').split('url(')[1],
				    'url': HOST + item.find('a').get('href')
				}
			)
		except AttributeError:
			print('Empty div block')
	return news

def save_file(file_name, news):
	with open(file_name, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Title', 'description', 'image', 'new\'s link'])
		for new in news:
			writer.writerow([new['title'], new['description'], new['preview_img'], new['url']])


def main():
	html = get_html(HOST)
	if html.status_code == 200:
		data = get_content(html.text)
		save_file('news.csv', data)
	else:
		print(f'Error: You don\t manage to get access. WebPage - {HOST}')


if __name__ == '__main__':
	main()
