from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from runapp.views import LandingPageView, HomepageView

app_name = 'runapp'
urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('home', HomepageView.as_view(), name='homepage'),
    path('login', LoginView.as_view(template_name='runapp/login.html'),
         name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
