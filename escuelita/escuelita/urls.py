from django.contrib import admin
from django.urls import include,path
from .views import HomePageView
from django.views.generic.base import TemplateView # new
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    # display Custom Admin Login  page
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(),name='home'), # display home page 
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),  # display about page
    path('services/', TemplateView.as_view(template_name='services.html'), name='services'),  # display services page
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),  # display contact page
    path('escuela/', include('escuela.urls'), name='escuela')  # display Sign up page
 
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)