from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'form': form,
            'pagename': 'Добавление нового сниппета'
        }
        return render(request, 'pages/add_snippet.html', context)

    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            lang = form.cleaned_data["lang"]
            code = form.cleaned_data["code"]

            Snippet.objects.create(name=name, lang=lang, code=code)

            return redirect('snippets-list')
        else:
            ...



def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    context = {
        'pagename': f'Сниппет: {snippet.name}',
        'snippet': snippet
    }
    return render(request, 'pages/snippet_detail.html', context)