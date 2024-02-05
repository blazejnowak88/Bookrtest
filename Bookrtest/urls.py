"""
URL configuration for Bookrtest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import HomeView
from reviews import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', HomeView.as_view(), name='home'),
    path('books/', views.book_list, name='book_list'),
    path('add-book/', views.AddBookView.as_view(), name='add_book'),

    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:book_pk>/reviews/new/', views.review_edit, name='review_create'),
    path('book-search/', views.book_search, name='book_search'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    # path('books/<int:book_pk>/reviews/<int:review_pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),

]
