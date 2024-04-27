from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Category


# Create your views here.

class CategoryView(View):

    def get(self, request):
        cats = Category.objects.all()
        return render(request, 'tours/list.html', {
            'categories': cats
        })

    def post(self, request):
        pass


def index(request):
    return HttpResponse('TEST')


def list(request, tour_id):
    return HttpResponse(f'TOUR {tour_id}')