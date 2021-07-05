from django import forms
from .models import UserProfileInfo, Product, Order


class UserCreateForm(forms.Form):
    contactno = forms.CharField(max_length=30, required=True, help_text='Optional')
    city = forms.CharField(max_length=30, required=True, help_text='Optional')
    dob =  forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))  # If no date is selected then Django saves blank field value.
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    username = forms.CharField(max_length=30, required=True, help_text='Optional')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    gender = forms.CharField(max_length=30, required=False, help_text='Optional')
    grade = forms.CharField(max_length=30,required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, required=True,help_text='Enter a valid email address')
    image = forms.ImageField()

class LoginForm(forms.Form):
    username = forms.CharField(label="UserName:", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)

    # Profile Form
class UserProfileForm(forms.ModelForm):

    dob = forms.DateField(widget=forms.TextInput(attrs=
    {
        'class': 'datepicker'
    }))
    class Meta:
        model =  UserProfileInfo
        fields = [
            'dob',
            'city',
            'contactno',
            'username',
            'portfolio_site',
            'image',
            'gender',
            'grade',
            ]

#Product form

class ProductForm(forms.ModelForm):

    class Meta:
 
        model = Product

        fields = ['id', 'product_name', 'product_price', 'product_image', 'size','width','details']

 
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['id', 'product', 'product_price','size','width','quantity']

    def save(self, commit=True):
        self.instance.user = self.request.user
        return super().save(commit=commit)
