from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.BorrowedBooksListView.as_view(), name='borrowed'),
    path('books/<pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/<pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('book/<uuid:pk>/renew/', views.BookInstanceUpdateView.as_view(), name='renew'),
]