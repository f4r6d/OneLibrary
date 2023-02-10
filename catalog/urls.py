from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedBooksListView.as_view(), name='borrowed'),
    path('authors/add/', views.AuthorCreateView.as_view(), name='author-create'),
    path('books/add/', views.BookCreateView.as_view(), name='book-create'),
    path('genres/add/', views.GenreCreateView.as_view(), name='genre-create'),
    path('languages/add/', views.LanguageCreateView.as_view(), name='language-create'),
    path('authors/<pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('books/<pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/<pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<pk>/delete/', views.author_delete, name='author-delete'),
    path('books/<pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<pk>/delete/', views.book_delete, name='book-delete'),
    path('books/<pk>/book_instance/add/', views.BookInstanceCreateView.as_view(), name='book_instance-create'),
    path('book_instance/<uuid:pk>/renew/', views.BookInstanceRenewUpdateView.as_view(), name='book_instance-renew'),
    path('book_instance/<uuid:pk>/update/', views.BookInstanceUpdateView.as_view(), name='book_instance-update'),
    path('book_instance/<uuid:id>/delete/', views.book_instance_delete, name='book_instance-delete'),
    path('book_instance/<uuid:pk>/borrow/', views.borrow, name='book_instance-borrow'),
    path('book_instance/<uuid:pk>/take_back/', views.take_back, name='book_instance-take-back'),
]