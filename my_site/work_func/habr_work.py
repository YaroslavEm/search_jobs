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


def get_value(div):
    domen = 'https://career.habr.com/'
    url = domen + div.find('a')['href']
    title = div.find('a', attrs={'class': 'vacancy-card__title-link'}).text
    company = 'Неизвестно'
    comp = div.find('div', attrs={'class': 'vacancy-card__company-title'})
    if comp:
        company = comp.text
    city = 'Неизвестно'
    ct = div.find('div', attrs={'class': 'vacancy-card__meta'}).find('a', attrs={
        'class': 'link-comp link-comp--appearance-dark'})
    if ct:
        city = ct.text
    description = div.find('div', attrs={'class': 'vacancy-card__skills'}).text
    return {'url': url, 'title': title, 'company': company, 'city': city, 'description': description}


def extract_jobs(url):
    jobs = []
    errors = []
    page = 1
    while page:
        request = requests.get(f'{url}&page={page}', headers=headers)
        if url:
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'html.parser')
                main_div = soup.find('div', attrs={'class': 'section-group section-group--gap-medium'})
                if main_div:
                    no_content = main_div.find('div', attrs={'class': 'no-content__title'})
                    if no_content is None:
                        div_lst = main_div.find_all('div', attrs={'class': 'vacancy-card__inner'})
                        for div in div_lst:
                            job = get_value(div)
                            jobs.append(job)
                        page += 1
                    else:
                        page = 0
                else:
                    errors.append({'url': url, 'title': 'Div does not exists'})
            else:
                errors.append({'url': url, 'title': 'Page do not responce'})
        else:
            errors.append({'url': url, 'title': f'URL does not exists'})
    return jobs, errors


def get_jobs(keyword):
    url = f'https://career.habr.com/vacancies?q={keyword}&type=all'
    jobs, errors = extract_jobs(url)
    return jobs, errors
