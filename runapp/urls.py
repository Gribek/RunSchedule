from django.urls import path

from runapp.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page')
]
