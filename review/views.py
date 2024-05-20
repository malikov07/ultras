from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from .models import Review,BlogReview
from shop.models import Product
from blog.models import Blog
# Create your views here.

class AddReviewView(View):
    def post(self,request):
        id = request.POST["user_id"]
        product_id = request.POST["product_id"]
        text = request.POST["review_text"]
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=id)
        review = Review.objects.create(author=user,product=product,text=text)
        review.save()
        return redirect("shop-detail",product_id)
    

class AddBlogReviewView(View):
    def post(self,request):
        id = request.POST["user_id"]
        blog_id = request.POST["blog_id"]
        text = request.POST["review_text"]
        blog = Blog.objects.get(id=blog_id)
        user = User.objects.get(id=id)
        review = BlogReview.objects.create(author=user,blog=blog,text=text)
        review.save()
        return redirect("blog-detail",blog_id)