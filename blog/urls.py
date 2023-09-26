from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_blogs, name='blogs'),
    path('<slug:slug>', views.blog_detail, name='blog_detail'),
    path('delete/<slug:slug>/', views.delete_blog, name='delete_blog'),
    path('add/', views.add_blog, name='add_blog'),
    path('edit/<slug:slug>/', views.edit_blog, name='edit_blog'),
]
