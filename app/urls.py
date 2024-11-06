from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),  # URL pattern for the home page
    path('signup/', views.signUp, name='signup'),  # URL pattern for the sign-up page
    path('signin/', views.signIn, name='signin'),  # URL pattern for the sign-in page
    path('update_profile/', views.updateProfile, name='update_profile'),
    path('place_bid/', views.place_bid, name='place_bid'),
]
