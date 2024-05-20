from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, filters, pagination
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.transaction import atomic
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import Count

from blog.models import Blog
from review.models import Review
from shop.models import Category, Brands, Product, Order
from .serializers import (
    UserSerializer,
    BlogSerializer,
    ReviewSerializer,
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    OrderSerializer,
)

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]
    pagination_class = LimitOffsetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "text"]
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=["get"])
    def recent_posts(self, request, *args, **kwargs):
        blog = self.get_object()
        recent_posts = blog.posts.order_by("-created_date")[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def clone_blog(self, request, *args, **kwargs):
        original_blog = self.get_object()
        new_blog = Blog.objects.create(
            title=f"Clone of {original_blog.title}",
            text=original_blog.text,
            author=request.user, 
            topic=original_blog.topic,
        )
        new_blog.save()
        serializer = self.get_serializer(new_blog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=["get"])
    def recent_reviews(self, request):
        recent_reviews = Review.objects.all().order_by("-created_date")[:10]
        serializer = self.get_serializer(recent_reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def author_reviews(self, request, *args, **kwargs):
        review = self.get_object()
        author_reviews = Review.objects.filter(author=review.author)
        serializer = self.get_serializer(author_reviews, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=['get'])
    def products_by_category(self, request, *args, **kwargs):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular_categories(self, request):
        popular_categories = Category.objects.annotate(product_count=Count('product')).order_by('-product_count')[:5]
        serializer = self.get_serializer(popular_categories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rename_category(self, request, *args, **kwargs):
        category = self.get_object()
        new_name = request.data.get('new_name')
        category.name = new_name
        category.save()
        return Response({'status': 'name updated'})


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    pagination_class = LimitOffsetPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=["get"])
    def top_viewed(self, request):
        top_viewed_products = Product.objects.order_by("-viewed")[:5]
        serializer = ProductSerializer(top_viewed_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def view(self, request, *args, **kwargs):
        product = self.get_object()
        with atomic():
            product.viewed += 1
            product.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def related_products(self, request, *args, **kwargs):
        product = self.get_object()
        related_products = Product.objects.filter(
            category=product.category, types=product.types
        ).exclude(id=product.id)[:5]
        serializer = self.get_serializer(related_products, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["product__name", "user__username"]
    pagination_class = LimitOffsetPagination
