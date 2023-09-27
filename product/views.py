from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.tasks import scrape_products
from product.utils import clock_file


class ProductScrapingView(APIView):
    def get(self, request):
        clock_file()
        scrape_products.delay()
        data = {
            "success": True,
            "status": 200,
            "message": "Task is running in background.",
            "data": None
        }
        return Response(data, status=status.HTTP_200_OK)
