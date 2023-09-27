from celery.schedules import crontab
from django.db import models
import uuid
from root.celery import app
from django_celery_beat.models import CrontabSchedule, PeriodicTask


# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ScheduleModel(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    time = models.TimeField(unique=True)

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        db_table = 'schedule'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=self.time.minute,
            hour=self.time.hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
        if created:
            PeriodicTask.objects.create(
                crontab=schedule,
                name=self.title,
                task='product.tasks.scrape_products',
            )
        super().save(force_insert, force_update, using, update_fields)


class ProductModel(BaseModel):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'product'
