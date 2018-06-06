from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views import generic
from .forms import (
    LoginForm, CreateUserForm, UpdateUserForm, ArticleForm
)
from .models import Article, Category


from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy


User = get_user_model()


class Login(LoginView):
    """
    ログインページ
    """
    form_class = LoginForm
    template_name = 'nikki/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """
    ログアウトページ
    """
    template_name = 'nikki/article_list.html'


class CreateUser(generic.CreateView):
    """
    ユーザー仮登録
    """
    template_name = 'nikki/user_create.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        """
        仮登録と本登録用メールの発行
        """
        # 仮登録と本登録の切り替えは、is_active属性を使う。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
            'token': urlsafe_base64_encode(force_bytes(user.email)).decode('utf-8'),
            'user': user,
        }

        # テンプレートを使ってメールを組み立てる
        subject_template = get_template('nikki/mail_templates/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('nikki/mail_templates/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)  # ユーザーのメール送信メソッド
        return redirect('nikki:create_user_done')


class CreateUserDone(generic.TemplateView):
    """
    ユーザー仮登録完了
    """
    template_name = 'nikki/user_create_done.html'


class CreateUserComplete(generic.TemplateView):
    """
    メール内URLアクセス後のユーザー本登録
    """
    template_name = 'nikki/user_create_complete.html'

    def get(self, request, **kwargs):
        """
        uid、tokenが正しければ本登録
        """
        token = kwargs.get('token')
        uidb64 = kwargs.get('uidb64')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            email = force_text(urlsafe_base64_decode(token))
            user = User.objects.get(pk=uid, email=email)
            if user.is_active:    # すでにis_activeがTrueなら、処理は必要ないので404
                raise Http404
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        else:
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return super().get(request, **kwargs)

        raise Http404


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class DetailUser(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'nikki/user_detail.html'


class UpdateUser(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'nikki/user_form.html'

    def get_success_url(self):
        return resolve_url('nikki:detail_user', pk=self.kwargs['pk'])


class Top(generic.TemplateView):
    template_name = 'nikki/top.html'

# class CreateArticle(generic.CreateView):
#     """日記投稿ページ"""
#     model = Article
#     template_name = 'nikki/article_form.html'
#     form_class = ArticleForm
#
    # def form_valid(self, form):
    #     user_id = self.kwargs['user_id']
    #     article = form.save(commit=False)
    #     category = category.objects.get(name=name)
    #     artcle.category = category
    #
    #     article.user = get_object_or_404(User, pk=user_pk)
    #     article.category = get_object_or_404(Category, pk=category_pk)
    #     article.save()
    #     return redirect('nikki:top')


class ArticleList(generic.ListView):
    model = Article
    template_name = 'nikki/article_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_study'] = Article.objects.filter(category=1).order_by('-created_time')[:4]
        context['category_school'] = Article.objects.filter(category=2).order_by('-created_time')[:4]
        context['category_work'] = Article.objects.filter(category=3).order_by('-created_time')[:4]
        context['category_life'] = Article.objects.filter(category=4).order_by('-created_time')[:4]
        context['category_love'] = Article.objects.filter(category=5).order_by('-created_time')[:4]
        context['category_triviality'] = Article.objects.filter(category=6).order_by('-created_time')[:5]
        return context


def create_article(request, user_id):
    """
    日記投稿ページ
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ArticleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('nikki:index')
            # return HttpResponseRedirect('nikki:top')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ArticleForm()

    return render(request, 'nikki/article_form.html', {'form': form})


class DetailArticle(generic.DetailView):
    model = Article


class UpdateArticle(generic.UpdateView):
    model = Article
    form_class = ArticleForm

    def get_success_url(self):
        article_pk = self.kwargs['pk']
        url = reverse_lazy("nikki:detail", kwargs={"pk": article_pk})
        return url


class DeleteArticle(generic.DeleteView):
    model = Article
    success_url = reverse_lazy("nikki:index")


class CategoryView(generic.ListView):
    model = Article
    template_name = 'nikki/category.html'

    def get_context_data(self, **kwargs):
        category_pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['category_article'] = Article.objects.filter(category=category_pk).order_by('-created_time')
        return context
