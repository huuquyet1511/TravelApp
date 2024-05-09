from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Tour, News, Ticket, User
from .serializer import CategorySerializer, TourSerializer, NewsSerializer, TicketSerializer, UserSerializer
from .paginator import TourPaginator, NewsPaginator
# Create your views here.


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=True)
    def tours(self, request, pk):
        l = self.get_object().tour_set.filter(active = True)
        return Response(TourSerializer(l, many=True, context={
            'request':request
        }).data, status=status.HTTP_200_OK)


class TourViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = TourPaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queries = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queries = queries.filter(tour_name__icontains=q)
        return queries

    @action(methods=['get'], detail=True)
    def tickets(self, request, pk):
        l = self.get_object().ticket_set.filter(active=True)
        return Response(TicketSerializer(l, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class NewsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPaginator


class TicketViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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