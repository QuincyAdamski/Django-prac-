from django.urls import path, include
#from django.conf.urls import url
from . import views
from theApp import views #from the second vid
from .views import enroll_course
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    #path('', main)#if we get a blank url then call the main function and do whatever is inside there
    path('', views.index2, name='index2'),#it should just call whichever comes first if the '' at the beging is identical
    path('signup/', views.signup, name='signup'), #this will path to the sign up page (account creation)
    #path('login', views.login, name='login'),#paths to the login page
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('courses/', views.courses, name='courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('events/', views.events, name='events'),
    path('register_event/<int:event_id>/', views.register_event, name='register_event'),
    path('settings/', views.settings_page, name='settings'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),#in the settings page
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),#in the settings page
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),#in the settings page
    path('calendar/', views.CalendarView.as_view(), name='calendar'), #for the calandar from the blog
    #the password reset pages
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]