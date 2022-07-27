from django.urls import path

from . import views

urlpatterns = [
    path('', views.flux, name='flux'),
    path('create_review_solo/', views.create_review_solo, name='create_review_solo'),
    path('create_review/<int:pk>', views.create_review, name='create_review'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('posts/', views.posts, name='posts'),
    path('ticket/delete/<int:pk>', views.delete_ticket, name='delete_ticket'),
    path('ticket/update/<int:pk>', views.update_ticket, name='update_ticket'),
    path('review/delete/<int:pk>', views.delete_review, name='delete_review'),
    path('review/update/<int:pk>', views.update_review, name='update_review'),
]
