from django.urls import path

from runapp.views import LandingPageView, HomepageView

app_name = 'runapp'
urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('home', HomepageView.as_view(), name='homepage'),
]
