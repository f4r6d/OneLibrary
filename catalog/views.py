from django.shortcuts import render
from .models import Book, BookInstance, Author


def index(request):
    num_visit = request.session.get('num_visit', 0)
    num_visit += 1
    request.session['num_visit'] = num_visit

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_visit': num_visit,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request, 'catalog/index.html', context)