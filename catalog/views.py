from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, BookInstance, Author, Genre, Language
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django import forms


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

@permission_required(['is_staff'], raise_exception=True)
def book_instance_delete(request, id):
    book = get_object_or_404(BookInstance, id=id)
    book.delete()
    return redirect(request.GET.get('next'))

@permission_required(['is_staff'], raise_exception=True)
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


class BookDetailView(DetailView):
    model = Book


class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'is_staff'


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'is_staff'


def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    author.delete()
    return redirect(reverse('catalog:author-list'))


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'is_staff'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_of_birth'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['date_of_death'].widget = forms.TextInput(attrs={'type': 'date'})
        return form


class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'is_staff'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['date_of_birth'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['date_of_death'].widget = forms.TextInput(attrs={'type': 'date'})
        return form


class GenreCreateView(PermissionRequiredMixin, CreateView):
    model = Genre
    fields = '__all__'
    permission_required = 'is_staff'


class LanguageCreateView(PermissionRequiredMixin, CreateView):
    model = Language
    fields = '__all__'
    permission_required = 'is_staff'


class BookInstanceCreateView(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = ['imprint', 'status']
    permission_required = 'is_staff'

    def form_valid(self, form):
            print(self.request)
            self.instance = form.save(commit=False)
            self.instance.book = Book.objects.get(pk=self.kwargs['pk'])
            self.instance.save()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Book.objects.get(pk=self.kwargs['pk'])
        return context

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/my_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

    
class BorrowedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed.html'
    permission_required = 'can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').all()
        
class BookInstanceRenewUpdateView(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    fields = 'due_back',
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:borrowed')
    initial = {'due_back': datetime.date.today() + datetime.timedelta(weeks=3)}


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_back'].widget = forms.TextInput(attrs={'type': 'date'})
        return form


class BookInstanceUpdateView(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    fields = ['imprint', 'due_back', 'borrower', 'status']
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('catalog:borrowed')


    def get_form(self, form_class=None):
        form = super(BookInstanceUpdateView, self).get_form(form_class)
        form.fields['due_back'].widget = forms.TextInput(attrs={'type': 'date'})
        return form
    
    def get_success_url(self):
        return self.request.GET.get('next')

@login_required()
def borrow(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if book_instance.status == 'a':
        book_instance.borrower = request.user
        book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        book_instance.status = 'o'
        book_instance.save()
        return redirect(reverse('catalog:my-borrowed'))
    else:
        messages.warning(request, f'You can\'t borrow a "{book_instance.get_status_display().upper()}" copy!')
        return redirect(request.GET.get('next'))


@permission_required(['is_staff'], raise_exception=True)
def take_back(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if book_instance.status == 'o':
        book_instance.borrower = None
        book_instance.due_back = None
        book_instance.status = 'a'
        book_instance.save()
        return redirect(reverse('catalog:borrowed'))
    else:
        messages.warning(request, f'You can\'t take back a "{book_instance.get_status_display().upper()}" copy!')
        return redirect(request.GET.get('next'))
