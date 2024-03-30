from django.shortcuts import render
from books.models import Book
from books.models import Category

def home(request, brand_slug = None):
    data = Book.objects.all()
    if brand_slug is not None:
        brand_name = Category.objects.get(slug = brand_slug)
        data = Book.objects.filter(category = brand_name)
        print(data)
    Books = Category.objects.all()
    return render(request, 'home.html',{'data': data , 'Books': Books})


def aboutus(request):
    return render(request, 'aboutus.html')