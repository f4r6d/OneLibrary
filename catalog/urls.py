from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('books/add/', views.BookCreateView.as_view(), name='book-create'),
    path('authors/add/', views.AuthorCreateView.as_view(), name='author-create'),
    path('genres/add/', views.GenreCreateView.as_view(), name='genre-create'),
    path('languages/add/', views.LanguageCreateView.as_view(), name='language-create'),
    path('books/<pk>/book_instance/add/', views.BookInstanceCreateView.as_view(), name='book_instance-create'),
    path('book_instance/<uuid:id>/delete/', views.book_instance_delete, name='book_instance-delete'),
    path('books/<pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<pk>/delete/', views.book_delete, name='book-delete'),
    path('authors/<pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<pk>/delete/', views.author_delete, name='author-delete'),
]