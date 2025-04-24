from django.urls import path
from .views import RegisterView,Profile,LogOutView,LogInView,Authone,Main,AuthTwo
urlpatterns=[
    path('main/', Main.as_view()),
    path('regis/', RegisterView.as_view()),
    path('profile/',Profile.as_view()),
    path('logout/',LogOutView.as_view()),
    path('login/',LogInView.as_view()),
    path('auth-one/',Authone.as_view()),
    path('auth-two/',AuthTwo.as_view())
]
