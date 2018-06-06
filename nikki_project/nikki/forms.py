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
        fields = ('category_id', 'title', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # CATEGORYS = (('life', '日常'), ('work', '仕事'), ('school', '学校'), ('study', '勉強'), ('love', '恋愛'), ('dream', '夢'), ('triviality', '小ネタ'), ('etc', 'その他'))
    CATEGORYS = ((e.id, e.name) for e in Category.objects.all())

    category_id = forms.ChoiceField(label='カテゴリ', choices=CATEGORYS)
    title = forms.CharField(label='タイトル', max_length=100)
    text = forms.CharField(label='本文', widget=forms.Textarea, max_length=1000)


########### コメント投稿 ###########
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'text')
