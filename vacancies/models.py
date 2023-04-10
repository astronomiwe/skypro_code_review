from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    picture = models.URLField(default='https://place-hold.it/100x60')


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)   # CR: неверное название поля. Смотри коммент в urls.py с рекомендациями по избеганию подобных ошибок :)
    location = models.CharField(max_length=20) # CR: Что, если вакансия открыта в городе "Железногорск-Илимский" (21 символ) ?
    # ТЗ додумано, дополнительные атрибуты полей, такие как длина, стоит уточнять у заказчика (в данном случае у куратора группы).
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    posted = models.DateField()  # CR: неверное название поля. Смотри коммент в urls.py с рекомендациями по избеганию подобных ошибок :)
