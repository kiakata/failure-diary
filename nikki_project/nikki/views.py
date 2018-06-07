from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views import generic
from .forms import (
    LoginForm, CreateUserForm, UpdateUserForm, ArticleForm, CommentForm
)
from .models import Article, Category, Comment


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


class ArticleList(generic.ListView):
    model = Article
    template_name = 'nikki/article_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_study'] = Article.objects.filter(category=1).order_by('-created_at')[:6]
        context['category_school'] = Article.objects.filter(category=2).order_by('-created_at')[:6]
        context['category_work'] = Article.objects.filter(category=3).order_by('-created_at')[:6]
        context['category_life'] = Article.objects.filter(category=4).order_by('-created_at')[:6]
        context['category_love'] = Article.objects.filter(category=5).order_by('-created_at')[:6]
        context['category_triviality'] = Article.objects.filter(category=6).order_by('-created_at')[:6]
        return context


def create_article(request, user_id):
    """
    日記投稿ページ
    """
    model = Article
    template_name = 'nikki/article_form.html'
    user = get_object_or_404(User, pk=user_id)
    posted_article_title = request.POST.get('title')
    posted_article_text = request.POST.get('text')
    posted_user_id = request.POST.get('user_id')
    posted_category_id = request.POST.get('category_id')

    form = ArticleForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        p = Article(title=posted_article_title, text=posted_article_text, user_id=user_id, category_id=posted_category_id)
        p.save()
        return redirect('nikki:index')

    context = {
    'form':form
    }
    return render(request, 'nikki/article_form.html', context)


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
        context['category_name'] = Category.objects.get(pk=category_pk)
        return context

def create_comment(request, article_id):
    """
    コメント投稿ページ
    """
    model = Comment
    template_name = 'nikki/comment_form.html'
    article = get_object_or_404(Article, pk=article_id)
    posted_user_id = request.user.id
    posted_comment_text = request.POST.get('text')

    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        p = Comment(article_id=article_id, user_id=posted_user_id, text=posted_comment_text)
        p.save()
        return redirect('nikki:detail_article', pk=article_id )

    context = {
    'form':form
    }
    return render(request, 'nikki/article_form.html', context)
