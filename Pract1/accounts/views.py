from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request,
                         'Регистрация успешна! Теперь вы можете войти.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Исправьте ошибки в форме.')
        return super().form_invalid(form)


def login_view(request):
    #if request.user.is_authenticated:
        #return redirect('polls:index')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')

                # Перенаправляем на страницу, с которой пришли или на список опросов
                next_url = request.GET.get('next', 'polls:index')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('polls:index')