from django.urls import path
from . import views

app_name = 'nikki'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('index', views.ArticleList.as_view(), name='index'),
    # path('create_article/<int:user_id>', views.CreateArticle.as_view(), name='create_article'),
    path('create_article/<int:user_id>', views.create_article, name='create_article'),
    path('detail_article/<int:pk>', views.DetailArticle.as_view(), name='detail_article'),
    path('update_article/<int:pk>', views.UpdateArticle.as_view(), name='update_article'),
    path('delete_article/<int:pk>', views.DeleteArticle.as_view(), name='delete_article')
]