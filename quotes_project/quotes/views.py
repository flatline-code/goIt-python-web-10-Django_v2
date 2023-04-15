from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from quotes.forms import TagForm, AuthorForm, QuoteForm
from .models import Author, Quote, Tag

# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})

def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/author.html', {'form': form})
        
    return render(request, 'quotes/author.html', {'form': AuthorForm()})

def quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_authors = Author.objects.filter(fullname__in=request.POST.getlist('authors'))
            for author in choice_authors.iterator():
                new_quote.authors.add(author)
            
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/quote.html', {"authors": authors, "tags": tags, 'form': form})

    return render(request, 'quotes/quote.html', {"authors": authors, "tags": tags, 'form': QuoteForm()})

def author_detail(request, pk):
    post = get_object_or_404(Author, pk=pk)
    context = {
        'post': post,
        'fullname': post.fullname,
        'description': post.description,
        'born_date': post.born_date,
        'born_location': post.born_location,

    }

    return render(request, 'quotes/about-author.html', context)