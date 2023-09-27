import requests
from bs4 import BeautifulSoup
from celery import shared_task
from datetime import datetime
from celery import Celery
from celery.schedules import crontab
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from product.models import ProductModel, ScheduleModel


@shared_task
def scrape_products():
    url = 'https://alifshop.uz/uz/events/rasprodaja'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_containers = soup.find_all('div', class_='h-full grid grid-cols-1 content-between')
        for container in product_containers[:4]:
            title = container.find('p',
                                   class_='max-w-xs text-sm text-grey-900 line-clamp-2 text-ellipsis mb-1').text.strip()
            real_price = container.find('p', class_='text-grey-400 text-sm')
            discount = container.find('p', class_='text-red text-sm')
            image_url = container.find('img', class_='w-full h-full object-contain')['src']
            price = real_price if real_price else discount

            ProductModel.objects.create(title=title, price=price.text.split(" ")[0].replace("\xa0", ''),
                                        image=image_url)
    else:
        print('Ошибка при получении страницы:', response.status_code)


@shared_task
def schedule():
    schedule = ScheduleModel.objects.all()
    for i in schedule:
        if datetime.now().strftime("%H:%M") == i.time.strftime("%H:%M"):
            scrape_products.delay()
