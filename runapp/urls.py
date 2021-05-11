from django.urls import path

from runapp.views import LandingPage, HomePageView

app_name = 'runapp'
urlpatterns = [
    path('', LandingPage.as_view(), name='landing_page'),
    path('home', HomePageView.as_view(), name='homepage'),
]
