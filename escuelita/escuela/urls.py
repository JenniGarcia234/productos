from .views import SignUpView,Update_ProfileView,LoginView,LogoutView, ProductCreateView, ProductListView, ProductDetailView,ProductUpdateView, ProductDeleteView
from django.urls import path, include  # new
from . import views




urlpatterns = [

    path('accounts/login/', LoginView.as_view(), name='login'),#overriding login url of default auth app.
    path('signup', SignUpView.as_view(), name='sign-up'),
    path('profile/<int:pk>/',Update_ProfileView.as_view(), name='profile'),
    path ('accounts/logout/',LogoutView.as_view() , name='logout'),#overriding logout url of default auth app.
    path('accounts/', include('django.contrib.auth.urls')),#Adding the url of default auth app to use it

    #Products
    path('products/create', ProductCreateView.as_view(), name='product-create'),
    path('products', ProductListView.as_view(), name='products-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),

    #Shops
    path('mis-compras/', views.add_sale, name='create_compra'),
    path('mis-compras/', views.select_product),
    path('compras/price/(?P<pk>\d+)/', views.fetch_price, name='fetch_price'),
]
