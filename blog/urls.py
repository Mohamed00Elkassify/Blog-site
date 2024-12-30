from django.urls import path
from . import views


# application namespace which allows you to organize URLs by application & use the name when referring to them
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail')
]