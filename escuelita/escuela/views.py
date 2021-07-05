from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.messages import constants as messages
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
import os
from .models import User,UserProfileInfo, Product, Order
from .forms import  UserCreateForm,UserProfileForm,LoginForm, OrderForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, request
from django.urls import reverse
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.views.generic import View
import pyautogui as pu

# Create your views here.
class SignUpView(View):
   model = User,UserProfileInfo
   #login_url = reverse_lazy('login')
   form_class = UserCreateForm
   template_name = "signup.html"

   def get(self, request, *args, **kwargs):
       form = self.form_class()
       return render(request, self.template_name, {'form': form})


   def post(self, request, *args, **kwargs):
       form = UserCreateForm(request.POST, request.FILES or None)


       if form.is_valid():
           # Cleaned(normalized) data
           city = form.cleaned_data.get('city')
           contact_no = form.cleaned_data.get('contactno')
           date_of_birth = form.cleaned_data.get('dob')
           password = form.cleaned_data.get('password')
           username = form.cleaned_data.get('username')
           email = form.cleaned_data.get('email')
           firstname = form.cleaned_data.get('first_name')
           lastname = form.cleaned_data.get('last_name')
           gender = form.cleaned_data.get('gender')
           grade = form.cleaned_data.get('grade')
           lastname = form.cleaned_data.get('last_name')
           lastname = form.cleaned_data.get('last_name')
           confirm_password = form.cleaned_data.get('confirm_password')
           image = form.cleaned_data.get('image')


           # check if the password match
           if password == confirm_password:
               if not User.objects.filter(email=email).exists():


                   if  User.objects.filter(username=username).exists():
                       pu.alert("Username already exists.Registration Failed.Try again.")
                       return redirect('sign-up')
                   else:
                       new_user = User.objects.create_user(username=username, password=password, email=email,
                                                           first_name=firstname, last_name=lastname)
                       new_user.save()
                       user= User.objects.get(username=username)
                       p_form = UserProfileForm()

                       p_form = p_form.save(commit=False)
                       p_form.user = user
                       p_form.dob = date_of_birth
                       p_form.username=username
                       p_form.city = city
                       p_form.contactno = contact_no
                       p_form.image = image
                       p_form.gender = gender
                       p_form.grade= grade
                       p_form.save()
                       pu.alert( text="New User Created Successfully",title="Success")
                       # Create UserProfile model

                       # logged in the user
                       login(request, new_user)
                       pu.alert( text="New User Loggedin susuccessfully",title="Success")                      
                       return redirect('home')
               else:
                   pu.alert('Registration Failed - Try different email address')
                   return redirect('sign-up')

           else:
               pu.alert("password and confirmpassword does not match.Try again")
               return redirect('sign-up')

       else:

           return render(request, self.template_name, {'form': form})



class LoginView(View):
    form_class = LoginForm
    redirect_authenticated_user = True
    model = UserProfileInfo

    def get(self, request, *args, **kwargs):  # GET Method
        form = self.form_class()
        return (render(request, 'registration/login.html', {'form': form}))  # Renders Login page

    def post(self, request, *args, **kwargs):  # POST Method
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']           
            
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                if user.is_active and user.is_superuser:
                    if not User.objects.filter(username=username).exists():
                        new_userprofile= UserProfileInfo.objects.create(user=user,username=username, city= '',contactno='',dob='2010-05-25')
                        new_userprofile.save()# Creating userprofile record for superuser(admin)with default date
                    return redirect("/")  # Redirect to home page
       

                else:
                    if user.is_active:
                        return redirect("/") # Redirect to home page
                    else:
                        return redirect('login')  # Redirect to Login page

            else:
                pu.alert("Wrong Username or Password")
                return redirect('login')

        else:
            return render(request, 'registration/login.html', {'form': form})







class LogoutView(View):
    def get(self, request):
     logout(request)
     return HttpResponseRedirect('/')


@method_decorator(login_required, name='dispatch')
class Update_ProfileView(UpdateView):
    model = User, UserProfileInfo
    # login_url = reverse_lazy('login')
    form_class = UserProfileForm
    template_name = "userprofile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
      if request.method == 'POST':
          form = UserProfileForm(request.POST, request.FILES or None)
          if form.is_valid():
              # Cleaned(normalized) data
              uId = form.cleaned_data.get('id')
              city = form.cleaned_data.get('city')
              username = form.cleaned_data.get('username')
              contact_no = form.cleaned_data.get('contactno')
              date_of_birth = form.cleaned_data.get('dob')
              gender = form.cleaned_data.get('gender')
              grade = form.cleaned_data.get('grade')
              image = form.cleaned_data.get('image')

              userprofile = UserProfileInfo.objects.get(username=username)

              userprofile.city = city
              userprofile.contactno = contact_no
              userprofile.dob = date_of_birth
              userprofile.gender = gender
              userprofile.grade = grade
              userprofile.image = image
              userprofile.save()
              pu.alert(text="New User Profile Updated Successfully", title="Success")
              return HttpResponseRedirect('/')


          else:
              pu.alert(text="Form is not valid.Date might be not in 'YYYY-MM-DD' Format", title="Error")

              return HttpResponseRedirect('/')

      else:
          return HttpResponseRedirect('/')


#Products views 
class ProductCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Product
    template_name = "create_product.html"
    fields=['product_name', 'product_price', 'product_image', 'size','width','details']
    login_url = 'login'  #if not authenticated redirect to login page

    # only superuser is allowed to see this view.
    def test_func(self):
        return self.request.user.is_superuser

    # url to redirect after successfully creation
    def get_success_url(self):
         #Displaying message of successful creation of new product
         pu.alert(text='New Product Created Successfully',title='Create',button='OK')
         return reverse_lazy('products-list')


# Only logged in superuser can see this view
class ProductListView(LoginRequiredMixin,UserPassesTestMixin,ListView):

    model = Product
    template_name = 'show_product.html'
    context_object_name = 'products'
    paginate_by = 5
    login_url = 'login' #if not authenticated redirect to login page

    # only superuser is allowed to see this view.
    def test_func(self):
        return self.request.user.is_superuser


    def get_queryset(self):  # new

        if self.request.method == "GET":
            query = self.request.GET.get('search')  # your input name is 'search'
            print('Search word:' + str(query))
        if query:
            return Product.objects.filter(product_name__icontains=query)

        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        products = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(products, self.paginate_by)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context['products'] = products
        return context



# Only logged in superuser can see this view
class ProductDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):

    model = Product
    template_name = 'detail_product.html'
    login_url = 'login' #if not authenticated redirect to login page

    # only superuser is allowed to see this view.
    def test_func(self):
        return self.request.user.is_superuser
   

# Only logged in superuser can see this view
class ProductUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Product
    template_name = 'update_product.html'
    # specify the fields
    fields = ['id', 'product_name', 'product_price', 'product_image', 'size','width','details']
    login_url = 'login' #if not authenticated redirect to login page

    # only superuser is allowed to see this view.
    def test_func(self):
        return self.request.user.is_superuser

    # updating details
    # url to redirect after successfully updation
    def get_success_url(self):
         # Displaying message of successful updation of product
         pu.alert(text='Product Info Updated Successfully', title='Update', button='OK')
         return reverse_lazy('products-list')



# Only logged in superuser can see this view
class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Product
    template_name = 'delete_product.html'
    login_url = 'login' #if not authenticated redirect to login page

    # only superuser is allowed to see this view.
    def test_func(self):
        return self.request.user.is_superuser

    # url to redirect after successfully deletion
    def get_success_url(self):
        # Displaying message of successful deletion of product
         pu.alert(text='Product Deleted Successfully', title='Delete', button='OK')
         return reverse_lazy('products-list')



#Orders views
def add_sale(request):
    if request.method=='POST':
        form = OrderForm(request.POST or None)
        form.fields['product_price'].widget.attrs['disabled']=True
        if form.is_valid():
            product = form.cleaned_data['product']
            product_price = form.cleaned_data['product_price']
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data['size']
            width = form.cleaned_data['width']
            Order.objects.create(product=product, quantity=quantity, product_price=product_price,size=size,width=width)
            messages.success(request, 'Product is successfully sold.')
            return HttpResponseRedirect('/')
    else:
        form = OrderForm()
    return render(request, 'create_compra.html', {'form':form})


def select_product(request):
    productobj = Product.objects.all()
    return render(request, 'create_compra.html', {'product_data': productobj})

def fetch_price(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print('product',product)
    if request.method=='GET':
        response = HttpResponse('')
        product_price = product.product_price
        print('product_price',product_price)
        response['price-pk'] = product.pk
        response['product_price'] = product_price
        return response


