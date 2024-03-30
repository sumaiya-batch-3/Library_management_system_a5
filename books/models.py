from django.db import models
from django.contrib.auth.models import User
from user.models import publisherInfo

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length = 100, unique = True, null = True, blank = True)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    publisher = models.ForeignKey(publisherInfo, on_delete=models.CASCADE, null = True , blank = True)
    title = models.CharField(max_length=50)
    # category = models.ManyToManyField(Category , null = True , blank = True)
    category = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quntity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='books/media/uploads', height_field=None, width_field=None, max_length=None,default='')
    # image = models.ImageField(upload_to='books/media/uploads/', blank = True, null = True)
    isProduct_Stock = models.BooleanField(default=True, null =True, blank=True)
        
    def __str__(self):
            return self.title
    
class review(models.Model):
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return f"reviwe by {self.name}"

START_CHOICES = [
    ('★☆☆☆☆',1),
    ('★★☆☆☆',2),
    ('★★★☆☆',3),
    ('★★★★☆',4),
    ('★★★★★',5),
]
class Ratings(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.CharField(choices = START_CHOICES ,max_length=50)
    def __str__(self):
            return f"Rating by {self.rating}"
    
class Purchase_history(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    Book = models.ForeignKey(Book,on_delete=models.CASCADE)
    isBorrowd = models.BooleanField(default=True, null = True, blank = True)

    def __str__(self):
        return f"{self.user.first_name} borrowed this book name: {self.Book.title}"