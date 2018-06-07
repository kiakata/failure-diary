from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model
from .models import Article, Comment, Category, User

import logging
User = get_user_model()


def info(msg):
    logger = logging.getLogger('command')
    logger.info(msg)


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class CreateUserForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email', 'nickname', 'agegroup')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


    agegroup = forms.ChoiceField(label='年代', choices=User.AGEGROUPS)


class UpdateUserForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ('nickname', 'agegroup',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    agegroup = forms.ChoiceField(label='年代' ,choices=User.AGEGROUPS)
    # 性別 = forms.ChoiceField(choices=GENDERS)


########## 記事投稿#############
class ArticleForm(forms.ModelForm):
    """Article投稿フォーム"""

    class Meta:
        model = Article
        fields = ('category_id', 'title', 'text', 'failure_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    CATEGORYS = ((e.id, e.name) for e in Category.objects.all())

    category_id = forms.ChoiceField(label='カテゴリ', choices=CATEGORYS)
    title = forms.CharField(label='タイトル', max_length=100)
    text = forms.CharField(label='本文', widget=forms.Textarea, max_length=1000)
    failure_image = forms.ChoiceField(label='画像選択', choices=Article.IMAGES)


########### コメント投稿 ###########
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
