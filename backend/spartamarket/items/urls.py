from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
    path("", views.ItemsListAPIView.as_view(), name="item_list"),
    path("<int:id>/", views.ItemsListAPIView.as_view(), name="item_list"),
    path("category/", views.CategoryAPIView.as_view(), name="category"),
    path("like/<int:id>/", views.LikeAPIView.as_view(), name="like"),
]