from django.shortcuts import render,redirect
from . import models
from books.models import Book
from . import models
from . import forms
from books.models import review,Purchase_history,Ratings,Category
from books.forms import reviewForm
from user.models import UserAccount
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import Avg
from django.template.defaulttags import register
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
def send_transaction_email(user, subject, template):
        message = render_to_string(template, {
            'user' : user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

def symbol_to_numeric(symbol):

    symbol_mapping = {
        '★☆☆☆☆': 1,
        '★★☆☆☆': 2,
        '★★★☆☆': 3,
        '★★★★☆': 4,
        '★★★★★': 5,
    }
    return symbol_mapping.get(symbol, 0) 

def booksShow(request, brand_slug=None):
    data = Book.objects.all()

    if brand_slug is not None:
        brand_name = Category.objects.get(slug=brand_slug)
        data = Book.objects.filter(category=brand_name)

    book_ratings = {}
    for book in data:
        ratings = Ratings.objects.filter(Book=book)

        if ratings.exists():
            average_numeric_rating = sum(symbol_to_numeric(rating.rating) for rating in ratings) / len(ratings)
            book_ratings[book.id] = round(average_numeric_rating)
        else:
            book_ratings[book.id] = None
    allcategory = Category.objects.all()
    return render(request, 'books.html', {'data': data, 'Category': allcategory, 'ratings': book_ratings})

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
def ViewDetails(request, id):
    book = Book.objects.get(pk=id)
    comments = review.objects.all()

    if request.method == 'POST':
        comment_form = reviewForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = book
            comment.save()
    else:
        comment_form = reviewForm()
    if request.user.is_authenticated:
        is_borrowed = Purchase_history.objects.filter(user=request.user, Book=book, isBorrowd=True).exists()
        return render(request, 'view_details.html', {'object': book, 'comment_form': comment_form, 'comment': comments, 'isBorrowed': is_borrowed})
    else:
        return render(request, 'view_details.html', {'object': book})


def borrow(request, id, userid):
    # userid-=1
    # print(userid)
    data = Book.objects.get(pk=id)
    account = UserAccount.objects.get(pk=userid)  
    quntity = data.quntity
    price = data.price
    balance = account.balance
    purchase_history=False

    if balance > price and quntity > 1:
        quntity -= 1
        balance -= price
        account.balance = balance

        data.quntity = quntity
        data.save()

       
        purchase_history = Purchase_history.objects.create(user=request.user, Book=data)
        account.save()

        messages.success(
            request,
            f'You have successfully borrowed a book'
        )

        send_transaction_email(request.user, "Book Borrwed Message", "book_borrowed.html")
        return redirect('profile')
    else:
        messages.warning(
            request,
            f'Your balance is not enough to buy this book or the book is finished'
        )
        send_transaction_email(request.user, "Book Borrowed Message Failed", "book_borrow_failed.html")

    return render(request, 'view_details.html', {'object': data, 'isBorrowed': purchase_history})

def bookReturn(request, id,userid,buyid):
    # print(userid)
    data = models.Book.objects.get(pk=id)
    account = UserAccount.objects.get(pk=1)
    quntity = data.quntity
    price = data.price
    balance = account.balance
    if balance > price:
        if quntity > 1:
            quntity +=1
            balance+=price
            account.balance = balance
            data.quntity = quntity
            account.save()
            data.save()
            deleteHistory = models.Purcehase_history.objects.get(id = buyid)
            deleteHistory.delete()
            send_transaction_email(request.user, "Book Return Message succefully", "book_return.html")
            return redirect('profile')
    else:
        messages.warning(
            request,
            f'Your balance is not enough to buy this book or the book is finished'
        )
        send_transaction_email(request.user, "Book Return Message Failled", "book_return_failed.html")
    return render(request,'view_details.html', {'object': data})


def Search_Book_Fillter(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        data = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(category__name__icontains=search_query)
        )
    else:
        data = Book.objects.all()

    return render(request, 'search_book.html', {'data': data})

class AddBookView(LoginRequiredMixin, FormView):
    model = models.Book
    form_class = forms.Add_Books
    template_name = 'add_book.html'
    success_url = reverse_lazy('Book_list')
    context_object_name = 'form'
    success_message = "Your Book Successfully Posted"
    def form_valid(self, form):
        user_account = self.request.user.account.publisherAccount
        # Assign the UserAccount instance to the user field of the publisherInfo model
        form.instance.publihser = user_account
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class BookList(LoginRequiredMixin, ListView):
    model = models.Book
    template_name = 'book_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_account = self.request.user.account.publisherAccount

        books =  models.Book.objects.filter(publihser = user_account)
        # print(books)
        context['books'] = books 

        return context

class EditBook(LoginRequiredMixin, UpdateView):
    form_class = forms.Add_Books
    model = models.Book
    template_name = 'Edit_book.html'
    context_object_name = 'form'
    success_url = reverse_lazy('Book_list')
    success_message = "Your Book Successfully Updated"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    

class DeleteBook(LoginRequiredMixin, DeleteView):
    model = models.Book
    success_url = reverse_lazy('Book_list')
    template_name = "book_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your Book Successfully Deleted")
        return super().delete(request, *args, **kwargs)
    