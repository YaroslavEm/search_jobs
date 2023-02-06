from django.core.paginator import Paginator
from django.shortcuts import render, reverse, redirect

from .models import *
from .forms import *
from start_parsing import start_parsing, save_data

import json


def home_view(request):
    form = SearchForm()
    global_form = GlobalSearchForm()
    context = {
        'form': form,
        'global_form': global_form,
    }
    return render(request, 'parsing/home.html', context=context)


def list_view(request):
    form = SearchForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {
        'city': city,
        'language': language,
        'form': form,
    }
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['len_vacancies'] = len(qs)
    return render(request, 'parsing/list.html', context=context)


def global_view(request):
    global_form = GlobalSearchForm()
    keyword = request.GET.get('keyword').lower()
    save_keyword = request.GET.get('save_keyword')
    context = {
        'global_form': global_form,
        'keyword': keyword,
    }
    if save_keyword:
        jobs, errors = start_parsing(keyword)
        save_data(jobs, errors, keyword)
        reverse_url = f"{reverse('list')}?city=&language={keyword}"
        return redirect(reverse_url)
    else:
        try:
            with open(f'json_files/{keyword}.json', mode='a+', encoding='utf-8') as file:
                file.seek(0)
                data = file.read()
                if not data:
                    jobs, errors = start_parsing(keyword)
                    file.write(json.dumps(jobs, ensure_ascii=False))
                    file.seek(0)
                    data = file.read()
            data_list = json.loads(data)
        except:
            print('Ошибка!')
        paginator = Paginator(data_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['len_vacancies'] = len(data_list)
    return render(request, 'parsing/global_list.html', context=context)


def BadRequest(request, exception):
    return render(request, '400.html')


def AccessForbidden(request, exception):
    return render(request, '403.html')


def pageNotFound(request, exception):
    return render(request, '404.html')


def ServerError(request):
    return render(request, '500.html')
