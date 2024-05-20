from django.urls import path
from .views import AddReviewView,AddBlogReviewView
urlpatterns = [
    path("add-review/", AddReviewView.as_view(), name="add-review"),
    path("add-blog-review/", AddBlogReviewView.as_view(), name="add-blog-review"),
]