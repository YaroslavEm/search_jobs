import os, sys
import datetime as dt
from transliterate import slugify

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'my_site.settings'

import django

django.setup()

from work_func.habr_work import get_jobs as habr_get_jobs
from work_func.hh_work import get_jobs as hh_get_jobs
from work_func.superjob_work import get_jobs as superjob_get_jobs

from parsing.models import City, Language, Vacancy, Error

parsers = (habr_get_jobs, hh_get_jobs, superjob_get_jobs)


def save_city(job):
    city = job.get('city')
    ct = City(title=city)
    try:
        ct.save()
    except DatabaseError:
        pass


def save_language(keyword):
    ln = Language(title=keyword)
    try:
        ln.save()
    except DatabaseError:
        pass


def save_vacancy(job, keyword):
    city = slugify(job.pop('city'))
    job['city_id'] = City.objects.filter(slug=city).first().pk
    job['language_id'] = Language.objects.filter(title=keyword).first().pk
    qs = Vacancy(**job)
    try:
        qs.save()
    except DatabaseError:
        pass


def start_parsing(keyword):
    jobs = []
    errors = []
    for func in parsers:
        j, e = func(keyword)
        jobs += j
        errors += e

    return jobs, errors


def save_data(jobs, errors, keyword):
    for job in jobs:
        save_city(job)
        save_language(keyword)
        save_vacancy(job, keyword)

    if errors:
        qs = Error.objects.filter(time_create=dt.date.today())
        if qs.exists():
            err = qs.first()
            err.data.update({'errors': errors})
            err.save()
        else:
            Error(data=f'errors: {errors}').save()
