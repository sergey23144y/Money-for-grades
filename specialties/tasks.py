from celery import shared_task
import requests
import time
from specialties.models import Specialty


@shared_task(name='get_salary_information')
def get_salary_information():
    vacancies_url = 'https://api.hh.ru/vacancies'
    total_specializations = 174
    for number in range(1, total_specializations + 1):
        if Specialty.objects.filter(number=number).exists():
            params = {'only_with_salary': 'true',
                      'professional_role': number,
                      'area': '113',
                      'clusters': 'true',
                      'per_page': '0',
                      'schedule': 'fullDay',
                      'employment': 'full'}

            vacancies_request = requests.request('get', url=vacancies_url, params=params)
            response_vacancies = vacancies_request.json()

            minimum_rate = int(response_vacancies['clusters'][1]['items'][0]['name'].split()[1]) / 160
            maximum_rate = int(response_vacancies['clusters'][1]['items'][-1]['name'].split()[1]) / 160
            average_rate = ((minimum_rate + maximum_rate) / 2)

            Specialty.objects.filter(number=number).update(minimum_rate=minimum_rate,
                                                           maximum_rate=maximum_rate,
                                                           average_rate=average_rate)
            time.sleep(0.2)
