from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    # username = models.CharField(max_length=50)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.CharField(max_length=50)
    # address = models.CharField(max_length=200)
    # role = models.CharField(max_length=20)

    pass
    avatar = models.ImageField(upload_to="image/avatar")


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(BaseModel): #địa điểm tour
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return  self.tag_name

class Tour(BaseModel):
    tour_name = models.CharField(max_length=100)
    description = models.TextField()
    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="image/tours")
    remaining_quantity = models.IntegerField()  # số lượng vé còn lại
    departure_date = models.DateField()  # ngày khởi hành
    duration = models.CharField(max_length=50)  # thời gian kéo dài của tour

    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(Tag)

    class Meta:
        unique_together = ('tour_name', 'category')

    def __str__(self):
        return self.tour_name


class Booking(BaseModel): #ticket
    adult_quantity = models.IntegerField(default=1)
    child_quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)


class Rating(BaseModel):
    rating = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)


class News(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    content = models.TextField()

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(BaseModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Payment(BaseModel):
    payment_status = models.CharField(max_length=20)

    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)


