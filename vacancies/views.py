from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render

from vacancies.models import Specialty, Company, Vacancy


def main_view(request):
    specialties = Specialty.objects.annotate(num_vacancy=Count('vacancies')).all()
    companies = Company.objects.annotate(num_vacancy=Count('vacancies')).all()

    return render(request, 'index.html', {
        'specialties': specialties,
        'companies': companies
    })


def jobs_views(request, specialty_code=None):
    # CR: нет аннотаций к функции, не понятно какая бизнес-логика подразумевается.
    # CR: Для получения specialty лучше использовать get_object_or_404(),
    # это функция "из коробки" джанго, которая под капотом
    # содержит схожий функционал - на четыре строчки меньше, а делает то же самое!
    if specialty_code:
        try:
            specialty = Specialty.objects.get(code=specialty_code)
        except:
            raise Http404()
        vacancies = Vacancy.objects.filter(specialty__code=specialty_code).all()
        # CR: здесь можно обойтись без all(), результатом всё равно будет QuerySet.
    else:
        specialty = None
        vacancies = Vacancy.objects.all()

    return render(request, 'vacancies.html', {
        'vacancies': vacancies,
        'specialty_code': specialty_code,
        'specialty': specialty,
    })


def company_view(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except:
        raise Http404()
    vacancies = Vacancy.objects.filter(company__id=company_id).all()

    return render(request, 'company.html', {
        'company': company,
        'vacancies': vacancies,
    })


def vacancy_view(request, job_id):
    # CR: переменную job_id лучше назвать vacancy_id по названию сущности.
    # CR: Рекомендую хорошую статью про нейминг: https://habr.com/ru/companies/dododev/articles/714512/
    # CR: нет аннотаций к функции, не понятно какая бизнес-логика подразумевается.
    # CR: Лучше использовать get_object_or_404(), это функция "из коробки" джанго, которая под капотом содержит схожий функционал.
    try:
        vacancy = Vacancy.objects.get(id=job_id)
    except:
        raise Http404()

    return render(request, 'vacancy.html', {
        'vacancy': vacancy,
    })


def custom_handler404(request, exception):
    return HttpResponseNotFound('<br/><h1>Ошибка 404</h1><h2>Запрашиваемый ресурс не найден</h2>')


def custom_handler500(request):
    return HttpResponseServerError('<br/><h1>Ошибка 500</h1><h2>Ошибка запроса. Отказано в обработке</h2>')
