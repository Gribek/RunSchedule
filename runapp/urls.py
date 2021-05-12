from django.urls import path

from runapp.views import LandingPage, HomepageView

app_name = 'runapp'
urlpatterns = [
    path('', LandingPage.as_view(), name='landing_page'),
    path('home', HomepageView.as_view(), name='homepage'),
]
