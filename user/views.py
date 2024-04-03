# Create your views here.
# from django.shortcuts import render,redirect
# from . import forms
# from . import models
# from django.views.generic.edit import CreateView
# from django.views.generic import FormView
# from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.contrib.auth.views import LoginView,PasswordChangeView
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# from django.views import View
# from books.models import Purchase_history
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib import messages
# from django.views.generic.edit import CreateView
# from django.core.mail import send_mail
# from user.models import UserAccount
# from django.views.generic import ListView
# from django.db.models import Q
# from django.contrib.auth import logout
# from django.contrib.auth.mixins import LoginRequiredMixin


# class SignUpViewClass(SuccessMessageMixin, CreateView):
#     template_name = 'form.html'
#     success_url = reverse_lazy('login')
#     form_class = forms.RegistationForm
#     success_message = "Your account was created successfully "

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, self.success_message)
   

#         # Additional code for email verification
#         user = form.save()
#         user.is_active = False
#         user.save()

#         # Create UserAccount instance
#         UserAccount.objects.create(user=user)
    
#         # Send email verification
#         current_site = get_current_site(self.request)
#         subject = 'Activate Your Account'
#         message = render_to_string('verification_mail.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user),
#         })
#         user.email_user(subject, message)
#         send_mail(subject, message, 'ssumaiya@live.com', [user.email])
#         messages.success(self.request, 'Account Created Successfully. Please check your email to activate your account.')
#         return response
    
# class EmailVerificationView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user and default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request, 'Email verification successful. You can now log in.')
#         else:
#             messages.warning(request, 'Email verification failed.')
#         return redirect('login')
    
# # This Class based user Login  

# class UserLoginViewClass(LoginView):
#     template_name = 'login.html'
    
#     def get_success_url(self):
#         return reverse_lazy('homepage')
    
#     def form_valid(self, form):
#         messages.success(self.request, 'You are successfully logged in')
#         # form
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         messages.warning(self.request, 'Your provided information is incorrect')
#         # form
#         return super().form_invalid(form)
    
#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context['type'] = 'Login'
#         return context

# # This Class based user Logout
# # @method_decorator(login_required, name= 'dispatch')
# # class UserLogoutViewClass(LogoutView):
# #     template_name = 'logout.html'
# #     def get_success_url(self):
# #        return reverse_lazy('homepage')
    
# #     def dispatch(self, request, *args, **kwargs):
# #         response = super().dispatch(request, *args, **kwargs)

# #         messages.success(self.request, "You have been successfully logged out.")
# #         return response

# @login_required(login_url='your_login_url')
# def user_logout_view(request):
#     logout(request)
#     messages.success(request, "You have been successfully logged out.")
#     return redirect(reverse_lazy('homepage'))

# @method_decorator(login_required, name= 'dispatch')
# class ProfileView(View):
#     template_name = 'profile.html'
#     def get(self, request, *agrs, **kwargs):
#         data = Purchase_history.objects.filter(user=request.user)
#         userinfo = UserAccount.objects.filter(user = request.user)
#         print(userinfo)
#         return render(request, 'profile.html',{'data':data, 'userinfo': userinfo})

# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Profile Updated Successfully')
#             return redirect('profile')
    
#     else:
#         profile_form = forms.ChangeUserForm(instance = request.user)
#     return render(request, 'update_profile.html', {'form' : profile_form})


# @method_decorator(login_required, name= 'dispatch')
# class ChangePassWordClass(PasswordChangeView):
#     template_name = 'password_change.html'
#     success_url = reverse_lazy('profile')
#     success_message = "Your Password Successfully Changed"
#     def form_valid(self,form):
#         response = super().form_valid(form)
#         messages.success(self.request, self.success_message)
#         return response



# class Publishers_View(ListView):
#     template_name = 'publisherAll.html'
#     model = models.publisherInfo
#     # context_object_name = 'data'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Filter publishers with soldBookCount greater than 50
#         top_publishers = models.publisherInfo.objects.filter(adminPermission=True, soldBookCount__gt=50)
#         data =  models.publisherInfo.objects.filter(adminPermission=True)

#         # Add the filtered publishers to the context
#         context['top_publishers'] = top_publishers
#         context['data'] = data 

#         return context


# def Search_Publisher_Fillter(request):
#     search_query = request.GET.get('search', '')
    
#     if search_query:
#         data = models.publisherInfo.objects.filter(
#             Q(title__icontains=search_query) | 
#             Q(description__icontains=search_query) | 
#             Q(category__name__icontains=search_query)
#         )
#     else:
#         data = models.publisherInfo.objects.all()

#     return render(request, 'publisherAll.html', {'data': data})
# class PublisherResigterView(LoginRequiredMixin, FormView):
#     model = models.publisherInfo
#     form_class = forms.PublisherRegister
#     template_name = 'publisherRegister.html'
#     success_url = reverse_lazy('homepage')
#     context_object_name = 'form'
#     success_message = "Your Publisher Application Form Successfully Submited"
#     def form_valid(self, form):
#         # Get the UserAccount instance associated with the current user
#         user_account = self.request.user.account
#         # Assign the UserAccount instance to the user field of the publisherInfo model
#         form.instance.user = user_account
#         form.save()
#         messages.success(self.request, self.success_message)
#         return super().form_valid(form)
    

from django.shortcuts import render, redirect
from . import forms
from . import models
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from books.models import Purchase_history
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from user.models import UserAccount
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpViewClass(SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    form_class = forms.RegistationForm
    success_message = "Your account was created successfully "

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
   
        # Additional code for email verification
        user = form.save()
        user.is_active = False
        user.save()

        # Send email verification
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('verification_mail.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        user.email_user(subject, message)
        send_mail(subject, message, 'ssumaiya@live.com', [user.email])
        messages.success(self.request, 'Account Created Successfully. Please check your email to activate your account.')
        return response
    
class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Email verification successful. You can now log in.')
        else:
            messages.warning(request, 'Email verification failed.')
        return redirect('login')
    
class UserLoginViewClass(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('homepage')
    
    def form_valid(self, form):
        messages.success(self.request, 'You are successfully logged in')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Your provided information is incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

@login_required(login_url='your_login_url')
def user_logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(reverse_lazy('homepage'))

@method_decorator(login_required, name= 'dispatch')
class ProfileView(View):
    template_name = 'profile.html'
    def get(self, request, *args, **kwargs):
        data = Purchase_history.objects.filter(user=request.user)
        userinfo = UserAccount.objects.filter(user=request.user)
        print(userinfo)
        return render(request, 'profile.html',{'data': data, 'userinfo': userinfo})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': profile_form})

@method_decorator(login_required, name= 'dispatch')
class ChangePassWordClass(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('profile')
    success_message = "Your Password Successfully Changed"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class Publishers_View(ListView):
    template_name = 'publisherAll.html'
    model = models.publisherInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_publishers = models.publisherInfo.objects.filter(adminPermission=True, soldBookCount__gt=50)
        data =  models.publisherInfo.objects.filter(adminPermission=True)
        context['top_publishers'] = top_publishers
        context['data'] = data 
        return context

def Search_Publisher_Fillter(request):
    search_query = request.GET.get('search', '')
    if search_query:
        data = models.PublisherInfo.objects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) | 
            Q(category__name__icontains=search_query)
        )
    else:
        data = models.PublisherInfo.objects.all()

    return render(request, 'publisherAll.html', {'data': data})

class PublisherResigterView(LoginRequiredMixin, FormView):
    model = models.publisherInfo
    form_class = forms.publisherRegister
    template_name = 'publisherRegister.html'
    success_url = reverse_lazy('homepage')
    context_object_name = 'form'
    success_message = "Your Publisher Application Form Successfully Submited"
    
    def form_valid(self, form):
        # Get the UserAccount instance associated with the current user
        user_account = self.request.user.account
        # Assign the UserAccount instance to the user field of the publisherInfo model
        form.instance.user = user_account
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
