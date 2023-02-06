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
            main_div = soup.find('div', attrs={'class': '_3VMkc _3JfmZ UnlTV _3jfFx _3nFmX'})
            if main_div:
                paginator = main_div.find('div', attrs={'class': '_1d4Tz _9mI07 IlTIe _28lBi _1oBDC _22k99 _2hb0t'})
                if paginator:
                    reference = paginator.find_all('a')
                    for page in reference:
                        pages.append(page.text)
                    return int(pages[-2])
                return 1
    return None


def get_value(div):
    domen = 'https://russia.superjob.ru/'
    content = div.find('span', attrs={'class': '_2KHVB _3l13l _3l6qV _3PTah _3xCPT rygxv _17lam _2Ovds'})
    url = domen + content.a['href']
    title = content.text
    company = 'Неизвестно'
    comp = div.find('span', attrs={
        'class': '_3nMqD f-test-text-vacancy-item-company-name _2jHyi rygxv _17lam _3GtUQ _2WkWi'})
    if comp:
        company = comp.text
    city = div.find('div', attrs={'class': 'WDWTW bWi1w _5RkIk _3MV7d _28VU-'}).find('div',
                                                                                     attrs={'class': 'V4aa2'}).text
    description = div.find('span', attrs={'class': '_11xeD rygxv _17lam _3GtUQ _2WkWi'}).text
    return {'url': url, 'title': title, 'company': company, 'city': city, 'description': description}


def extract_jobs(last_page, url):
    jobs = []
    errors = []
    if last_page and url:
        for page in range(1, last_page + 1):
            request = requests.get(f'{url}&page={page}', headers=headers)
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'html.parser')
                main_div = soup.find('div', attrs={'class': '_3VMkc _3JfmZ UnlTV _3jfFx _3nFmX'})
                if main_div:
                    div_lst = main_div.find_all('div', attrs={'class': '_1wWd1 _3irGY'})
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
    url = f'https://russia.superjob.ru/vacancy/search/?keywords={keyword}'
    max_page = extract_max_page(url)
    jobs, errors = extract_jobs(max_page, url)
    return jobs, errors
