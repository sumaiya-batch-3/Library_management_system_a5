from django.urls import path,include
from . import views
urlpatterns = [
    path('books/',views.booksShow, name='show_All_Books'),
    path('AddBook/',views.AddBookView.as_view(), name='Add_Book'),
    path('BookList/',views.BookList.as_view(), name='Book_list'),
    path('DeleteBook/<int:pk>/',views.DeleteBook.as_view(), name='DeleteBook'),
    path('EditBook/<int:pk>/',views.EditBook.as_view(), name='EditBook'),
    path('books/<slug:brand_slug>/', views.booksShow, name='cetagory'),
    path('Views_Details<int:id>/', views.ViewDetails,name='Views_Details'),
    path('borrow/<int:id>/<int:userid>/', views.borrow, name='buynow'),
    path('return/<int:id>/<int:userid>/<int:buyid>/', views.bookReturn, name='return'),
    path('search/', views.Search_Book_Fillter, name='search'),
    path('borrow/<int:id>/<int:userid>/', views.borrow, name='buynow'),
]


