from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
    path("", views.ItemsListAPIView.as_view(), name="item_list"),
    path("<int:id>/", views.ItemsListAPIView.as_view(), name="item_list"),
    path("category/", views.CategoryAPIView.as_view(), name="category"),
    # path("<int:article_pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    # path("<int:pk>/comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    # path("comments/<int:comment_pk>/", views.CommentListAPIView.as_view(), name="comment_detail"),
    # path("check-sql/", views.check_sql, name="check_sql")
]