from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, BookInstance, Author, Genre, Language
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.contrib import messages


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


def book_instance_delete(request, id):
    book = get_object_or_404(BookInstance, id=id)
    book.delete()
    return redirect(request.GET.get('next'))


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.bookinstance_set.all():
        messages.warning(request, 'You Should First Delete all Copies!')
        return redirect(request.GET.get('next'))
    else:
        book.delete()
        return redirect(reverse('catalog:book-list'))

class BookListView(ListView):
    model = Book
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(DetailView):
    model = Book


class BookCreateView(CreateView):
    model = Book
    fields = '__all__'


class BookUpdateView(UpdateView):
    model = Book
    fields = '__all__'


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return redirect(reverse('catalog:author-list'))


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'


class AuthorUpdateView(UpdateView):
    model = Author
    fields = '__all__'


class GenreCreateView(CreateView):
    model = Genre
    fields = '__all__'


class LanguageCreateView(CreateView):
    model = Language
    fields = '__all__'


class BookInstanceCreateView(CreateView):
    model = BookInstance
    fields = ['imprint', 'status']

    def form_valid(self, form):
            print(self.request)
            self.instance = form.save(commit=False)
            self.instance.book = Book.objects.get(pk=self.kwargs['pk'])
            self.instance.save()
            return super().form_valid(form)

        
