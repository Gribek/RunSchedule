from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from . import views

app_name = 'runapp'
urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('home', views.HomepageView.as_view(), name='homepage'),
    path('login', LoginView.as_view(template_name='runapp/login.html'),
         name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', views.RegisterUserView.as_view(), name='register_user'),
    path('training_plan/new', views.TrainingPlanCreateView.as_view(),
         name='training_plan_create'),
    path('training_plan/edit/<int:pk>', views.TrainingPlanEditView.as_view(),
         name='training_plan_edit'),
    path('training_plan/<int:pk>', views.TrainingPlanDetailsView.as_view(),
         name='training_plan_details'),
    path('training_plans', views.TrainingPlanListView.as_view(),
         name='training_plan_list'),
    path('select_plan', views.SelectCurrentTrainingPlanView.as_view(),
         name='select_current_training_plan'),
    path('training/new/<int:plan_pk>', views.TrainingCreateView.as_view(),
         name='training_create'),
    path('training/edit/<int:pk>', views.TrainingEditView.as_view(),
         name='training_edit'),
    path('training/delete/<int:pk>', views.TrainingDeleteView.as_view(),
         name='training_delete'),
]
