from django.db import models
from django.db.models import Avg
from rest_framework.response import Response
# =================================================================================
class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.product_set.count()
# =================================================================================
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True)
    def __str__(self):
        return self.title

    @property
    def category_name(self):
        try:
            return self.category.name
        except:
            return ''

    @property
    def reting(self, request):
        average_rating = Review.objects.all().aggregate(Avg('rating'))
        return Response({'average_rating': average_rating['rating__avg']})
# =================================================================================
class Review(models.Model):
    CHOICES = ((i, '* ' * i) for i in range(1, 6))
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    stars = models.IntegerField(choices=CHOICES)
    text = models.TextField()

    def __str__(self):
        return self.text
