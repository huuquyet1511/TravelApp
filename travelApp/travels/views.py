from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Tour, News, Ticket, User, Comment, Like, Rating, Booking
from .serializer import CategorySerializer, TourSerializer, NewsSerializer, TicketSerializer, UserSerializer, \
    CommentSerializer, NewsSerializerDetail, RatingSerializer
from .paginator import TourPaginator, NewsPaginator
from .import permission
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
    permission_classes = [permissions.AllowAny()]

    def get_permissions(self):
        if self.action in ['add_comment', 'add_rating']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes
    def get_queryset(self): #tìm kiếm với q là từ khoá
        queries = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queries = queries.filter(tour_name__icontains=q)
        return queries

    @action(methods=['get'], detail=True) #/tour/{id}/tickets xem thong tin cac ticket cua tour
    def tickets(self, request, pk):
        l = self.get_object().ticket_set.filter(active=True)
        return Response(TicketSerializer(l, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path="comments", detail=True) #/tour/{id}/comments
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user = request.user, tour = self.get_object(), content=request.data.get('content'))
        comment.save()

        return Response(CommentSerializer(comment, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)

    # @action(methods=['post'], url_path="rating", detail=True)
    # def add_rating(self, request, pk):
    #     rating = Rating.objects.create(user=request.user, tour=self.get_object(), rating=request.data.get('rating'))
    #     rating.save()
    #
    #     return Response(RatingSerializer(rating, context={
    #         'request': request
    #     }).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path="rating", detail=True)
    def add_rating(self, request, pk):
        # Kiểm tra xem người dùng đã đăng nhập hay chưa
        # if not request.user.is_authenticated:
        #     return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # # Lấy tour từ pk
        # tour = self.get_objects()
        #
        # # Kiểm tra xem người dùng đã thanh toán cho tour đó chưa
        # if not tour.booking.filter(user=request.user, payment__payment_status=True).exists():
        #     return Response({"message": "Chua thanh toan"}, status=status.HTTP_403_FORBIDDEN)
        # Lấy tour từ pk
        tour = Tour.objects.get(pk=pk)

        # Kiểm tra xem người dùng đã thanh toán cho tour đó chưa
        booking_exists = Booking.objects.filter(user=request.user, ticket__tour=tour,
                                                payment__payment_status=True).exists()
        if not booking_exists:
            return Response({"message": "Khong có quyen danh gia"}, status=status.HTTP_403_FORBIDDEN)

        # Tạo đánh giá
        rating = Rating.objects.create(user=request.user, tour=tour, rating=request.data.get('rating'))
        rating.save()

        return Response(RatingSerializer(rating, context={'request': request}).data, status=status.HTTP_201_CREATED)

class NewsViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializerDetail
    # pagination_class = NewsPaginator
    permission_classes = [permissions.AllowAny()]

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    @action(methods=['post'], url_path="comments", detail=True)  # /news/{id}/comments
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user=request.user, news=self.get_object(), content=request.data.get('content'))
        comment.save()

        return Response(CommentSerializer(comment, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)  # /news/{id}/like
    def like(self, request, pk):
        like, create = Like.objects.get_or_create(user=request.user, news=self.get_object())
        if not create:
            like.liked = not like.liked
            like.save()

        return Response(NewsSerializerDetail(self.get_object(), context={
            "request": request
        }).data, status=status.HTTP_200_OK)


class TicketViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView): #xem duoc danh sach va xem tung id
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]

    def get_permissions(self): #chứng thực current user moi duoc thay doi
        if self.action in ['get_current']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False) # /user/current/ thay doi thong tin user
    def get_current(self, request):
        return Response(UserSerializer(request.user, context={
            "request": request
        }).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):#chỉ xoá và update
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permission.OwnerPermission]


class RatingViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permission.OwnerPermission]



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