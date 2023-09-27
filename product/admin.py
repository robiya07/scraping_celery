from django.contrib import admin

from product.models import ScheduleModel, ProductModel

# Register your models here.
admin.site.register(ScheduleModel)

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'created_at', 'updated_at']