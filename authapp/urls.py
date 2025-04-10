from django.urls import path
from .views import RegisterView,Profile,LogOutView,LogInView
urlpatterns=[
    path('regis/', RegisterView.as_view()),
    path('profile/',Profile.as_view()),
    path('logout/',LogOutView.as_view()),
    path('login/',LogInView.as_view())
]
