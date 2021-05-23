from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from runapp.views import LandingPageView, HomepageView, RegisterUserView, \
    TrainingPlanCreateView, TrainingPlanDetailsView, TrainingPlanListView, \
    TrainingPlanEditView, SelectCurrentTrainingPlanView

app_name = 'runapp'
urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('home', HomepageView.as_view(), name='homepage'),
    path('login', LoginView.as_view(template_name='runapp/login.html'),
         name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterUserView.as_view(), name='register_user'),
    path('training_plan/new', TrainingPlanCreateView.as_view(),
         name='training_plan_create'),
    path('training_plan/edit/<int:pk>', TrainingPlanEditView.as_view(),
         name='training_plan_edit'),
    path('training_plan/<int:pk>', TrainingPlanDetailsView.as_view(),
         name='training_plan_details'),
    path('training_plans', TrainingPlanListView.as_view(),
         name='training_plan_list'),
    path('select_plan', SelectCurrentTrainingPlanView.as_view(),
         name='select_current_training_plan'),
]
