from django.shortcuts import render
from django.views import View
from .models import Blog
from review.models import BlogReview
# Create your views here.

class BlogView(View):
    def get(self,request):
        blogs = Blog.objects.all()
        context = {
            "blogs":blogs
        }
        return render(request, "blog/blog.html", context)
    
class BlogDetailView(View):
    def get(self,request,id):
        blog = Blog.objects.get(id=id)
        reviews = BlogReview.objects.filter(blog__id = id)
        context = {
            "blog":blog,
            "reviews":reviews,
        }
        return render(request, "blog/blog-detail.html", context)
