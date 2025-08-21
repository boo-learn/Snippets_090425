from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages, auth
from django.views.generic import CreateView, DetailView, View, ListView, UpdateView
from django.shortcuts import render, redirect

from MainApp.models import Snippet, LANG_CHOICES
from MainApp.forms import SnippetForm, CommentForm, UserRegistrationForm
from MainApp.utils import send_activation_email


class AddSnippetView(LoginRequiredMixin, CreateView):
    """Создание нового сниппета"""
    model = Snippet
    form_class = SnippetForm
    template_name = 'pages/add_snippet.html'
    success_url = reverse_lazy('snippets-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Создание сниппета'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Success!!!")
        return super().form_valid(form)


class SnippetDetailView(DetailView):
    model = Snippet
    template_name = 'pages/snippet_detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snippet = self.get_object()
        context['pagename'] = f'Сниппет: {snippet.name}'
        context['comments'] = snippet.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def get_queryset(self):
        return Snippet.objects.prefetch_related("comments")


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('home')


class SnippetsListView(ListView):
    """Отображение списка сниппетов с фильтрацией, поиском и сортировкой"""
    model = Snippet
    template_name = 'pages/view_snippets.html'
    context_object_name = 'snippets'
    paginate_by = 5

    def get_queryset(self):
        my_snippets = self.kwargs.get('my_snippets', False)

        if my_snippets:
            if not self.request.user.is_authenticated:
                raise PermissionDenied
            queryset = Snippet.objects.filter(user=self.request.user)
        else:
            if self.request.user.is_authenticated:  # auth: all public + self private
                queryset = Snippet.objects.filter(
                    Q(public=True) | Q(public=False, user=self.request.user)
                ).select_related("user")
            else:  # not auth: all public
                queryset = Snippet.objects.filter(public=True).select_related("user")

        # Поиск
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )

        # Фильтрация по языку
        lang = self.request.GET.get("lang")
        if lang:
            queryset = queryset.filter(lang=lang)

        # Фильтрация по пользователю
        user_id = self.request.GET.get("user_id")
        if user_id:
            queryset = queryset.filter(user__id=user_id)

        # Сортировка
        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_snippets = self.kwargs.get('my_snippets', False)

        if my_snippets:
            context['pagename'] = 'Мои сниппеты'
        else:
            context['pagename'] = 'Просмотр сниппетов'

        # Получаем пользователей со сниппетами
        users = User.objects.filter(snippet__isnull=False).distinct()

        context.update({
            'sort': self.request.GET.get("sort"),
            'LANG_CHOICES': LANG_CHOICES,
            'users': users,
            'lang': self.request.GET.get("lang"),
            'user_id': self.request.GET.get("user_id")
        })

        return context


class SnippetEditView(UpdateView):
    model = Snippet
    form_class = SnippetForm
    template_name = 'pages/add_snippet.html'
    success_url = reverse_lazy('snippets-list')
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] =  "Редактировать Сниппет"
        context['edit'] =  True
        context['id'] = self.kwargs.get('id')
        return context


class UserRegistrationView(CreateView):
    """Регистрация нового пользователя"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'pages/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        send_activation_email(user, self.request)
        messages.success(self.request, f"Пользователь {user.username} успешно зарегистрирован!")
        return super().form_valid(form)