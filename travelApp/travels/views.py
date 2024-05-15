from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Tour, News, Ticket, User, Comment, Like, Rating, Booking, Payment
from .serializer import CategorySerializer, TourSerializer, NewsSerializer, TicketSerializer, UserSerializer, \
    CommentSerializer, NewsSerializerDetail, RatingSerializer, BookingSerializer, PaymentSerializer
from .paginator import TourPaginator, NewsPaginator
from .import permission
# Create your views here.


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=True) #categories/{id}/
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

    @action(methods=['post'], url_path="rating", detail=True)
    def add_rating(self, request, pk):
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
        comment = Comment.objects.create(user=request.user,
                                         news=self.get_object(),
                                         content=request.data.get('content'))
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
    permission_classes = [permissions.AllowAny()]

    def get_permissions(self):
        if self.action in ['add_booking']:
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    @action(methods=['post'], url_path="booking", detail=True)# /tickets/{id}/booking
    def add_booking(self, request, pk):
        # Lấy thông tin của tour dựa vào pk
        tour = self.get_object()
        ticket = self.get_object()
        # Tính toán tổng giá
        ticket_price = ticket.price
        adult_quantity = int(request.data.get('adult_quantity', 1))
        child_quantity = int(request.data.get('child_quantity', 0))
        # total_price = ticket_price * (adult_quantity + 0.7 * child_quantity)
        # Chuyển đổi child_quantity thành kiểu Decimal
        child_quantity_decimal = Decimal(child_quantity)

        # Tính tổng giá
        total_price = ticket_price * (adult_quantity + Decimal('0.75') * child_quantity_decimal)

        # Tạo đối tượng booking
        booking = Booking.objects.create(
            adult_quantity=adult_quantity,
            child_quantity=child_quantity,
            total_price=total_price,
            user=request.user,
            ticket=self.get_object()
        )
        booking.save()

        return Response(BookingSerializer(booking, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]


    def get_permissions(self): #chứng thực current user moi duoc thay doi
        if self.action in ['get_current']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['booking']:
            return [permission.UserPermission()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False) # /user/current/ thay doi thong tin user
    def get_current(self, request):
        return Response(UserSerializer(request.user, context={
            "request": request
        }).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)  # /users/{id}/booking xem thong tin cac booking cua user
    # def booking(self, request, pk):
    #     l = self.get_object().booking_set.filter(active=True)
    #     return Response(BookingSerializer(l, many=True, context={
    #         'request': request
    #     }).data, status=status.HTTP_200_OK)
    def booking(self, request, pk):
        user = self.get_object()
        bookings = user.booking_set.filter(active=True)
        return Response(BookingSerializer(bookings, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):#chỉ xoá và update
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permission.OwnerPermission] #chứng thực chỉ user tạo mới có thể sửa, xoá


class RatingViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permission.OwnerPermission]


class BookingViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = permission.OwnerPermission

    # class OwnerPermission(permissions.BasePermission):
    #     def has_object_permission(self, request, view, obj):
    #         return request.user == obj.user

    permission_classes = [permissions.IsAuthenticated, permission.ViewPermission]

    @action(methods=['post'], detail=True, url_path="payment") # /booking/{id}/payment
    def add_payment(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            booking=booking,
            payment_method_id=request.data.get('payment_method_id'),
            payment_status=request.data.get('payment_status', True)
        )

        # Calculate the total quantity to deduct
        total_quantity = booking.adult_quantity + booking.child_quantity

        # Deduct the total quantity from the tour's remaining quantity
        ticket = booking.ticket
        tour = ticket.tour

        if tour.remaining_quantity < total_quantity:
            return Response({"detail": "Not enough remaining quantity for this tour."},
                            status=status.HTTP_400_BAD_REQUEST)

        tour.remaining_quantity -= total_quantity
        tour.save()

        payment.save()

        return Response(PaymentSerializer(payment,
                                          context={'request': request}).data, status=status.HTTP_201_CREATED)



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