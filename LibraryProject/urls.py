"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from LibraryApp.views import *
from django.conf.urls.static import static
from LibraryProject import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',admin_student,name='admin_student'),
    path('all_books/',all_books,name='all_books'),
    path('admin_login',admin_login,name='admin_login'),
    path('admin_login/admin_new_register',admin_new_register,name='admin_new_register'),
    path('student_login',student_login,name='student_login'),
    path('student_login/student_dashboard',student_dashboard,name='student_dashboard'),
    path('admin_valid',admin_valid,name='admin_valid'),
    path('add_book',add_book,name="add_book"),
    path('delete_book',delete_book,name="delete_book"),
    path('assign_book',assign_book,name="assign_book"),
    path('clone_book',clone_book,name='clone_book'),
    path('return_book',return_book,name='return_book'),
    path('lost_book_delete',lost_book_delete,name='lost_book_delete'),
    path('add_student',add_student,name='add_student'),
    path('add_ebook',add_ebook,name='add_ebook'),
    path('settings',admin.site.urls),
    path('admin_logout',admin_logout,name='admin_logout'),



    path('student_valid',student_valid,name='student_valid'),
    path('books_borrowed/<str:student_id>/',books_borrowed, name='books_borrowed'),
    path('books_returned/<str:student_id>/',books_returned, name='books_returned'),
    path('books_overdue/<str:student_id>/',books_overdue, name='books_overdue'),
    path('e_books',e_books, name='e_books'),
    path('download/<book_id>/',download_book, name='download_book'),
    path('student_home',student_home,name='student_home'),
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)