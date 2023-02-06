import requests
from bs4 import BeautifulSoup

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


def extract_max_page(url):
    if url:
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            pages = []
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                paginator = soup.find('div', attrs={'data-qa': 'pager-block'})
                if paginator:
                    reference = paginator.find_all('a')
                    for page in reference:
                        pages.append(page.text)
                    return int(pages[-2])
                return 1
    return None


def get_value(div):
    url = div.find('h3', attrs={'class': 'bloko-header-section-3'}).find('a')['href']
    title = div.find('a', attrs={'class': 'serp-item__title'}).text
    company = 'Неизвестно'
    comp = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).find('a')
    if comp:
        company = comp.text
    city = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
    description = 'Без описания'
    desc = div.find('div', attrs={'class': 'g-user-content'})
    if desc:
        description = desc.text
    return {'url': url, 'title': title, 'company': company, 'city': city, 'description': description}


def extract_jobs(last_page, url):
    jobs = []
    errors = []
    if last_page and url:
        for page in range(last_page):
            request = requests.get(f'{url}&page={page}', headers=headers)
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'html.parser')
                main_div = soup.find('div', id='a11y-main-content')
                if main_div:
                    div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
                    for div in div_lst:
                        job = get_value(div)
                        jobs.append(job)
                else:
                    errors.append({'url': url, 'title': 'Div does not exists'})
            else:
                errors.append({'url': url, 'title': 'Page do not responce'})
    else:
        errors.append({'url': url, 'title': f'URL does not exists'})
    return jobs, errors


def get_jobs(keyword):
    url = f'https://hh.ru/search/vacancy?text={keyword}&area=113'
    max_page = extract_max_page(url)
    jobs, errors = extract_jobs(max_page, url)
    return jobs, errors
