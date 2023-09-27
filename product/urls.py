from django.urls import path
from product import views

urlpatterns = [
    path('product-scraping/', views.ProductScrapingView.as_view(), name='product_scraping'),
]