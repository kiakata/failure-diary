from django.urls import path
from . import views

app_name = 'nikki'

urlpatterns = [
    path('index', views.ArticleList.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('search/', views.SearchList.as_view(), name='search'),
    # User
    path('create_user/', views.CreateUser.as_view(), name='create_user'),
    path('create_user/done', views.CreateUserDone.as_view(), name='create_user_done'),
    path('create_user/complete/<uidb64>/<token>/', views.CreateUserComplete.as_view(), name='create_user_complete'),
    path('user_detail/<int:pk>/', views.DetailUser.as_view(), name='detail_user'),
    path('user_update/<int:pk>/', views.UpdateUser.as_view(), name='update_user'),
    path('user_delete/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    # Article
    path('create_article/<int:user_id>', views.create_article, name='create_article'),
    path('detail_article/<int:pk>', views.DetailArticle.as_view(), name='detail_article'),
    path('update_article/<int:pk>', views.UpdateArticle.as_view(), name='update_article'),
    path('delete_article/<int:pk>', views.DeleteArticle.as_view(), name='delete_article'),
    # Comment
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('comment/<int:article_id>', views.create_comment, name='comment'),
    path('detail_comment/<int:pk>', views.DetailComment.as_view(), name='detail_comment'),
    path('update_comment/<int:pk>', views.UpdateComment.as_view(), name='update_comment'),
    path('delete_comment/<int:pk>', views.DeleteComment.as_view(), name='delete_comment'),

]
