from django.contrib import admin
from . models import Book,review,Ratings,Purchase_history,Category

# Register your models here.
admin.site.register(Book)
admin.site.register(review)
admin.site.register(Purchase_history)
admin.site.register(Ratings)
admin.site.register(Category)
