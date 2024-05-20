from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Review,BlogReview
# Register your models here.


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ["id", "author", "text","product", "created_date"]
    list_display_links = ["id", "author", "text","product", "created_date"]
    search_fields = ["id", "author", "text", "product", "created_date"]
    ordering = ["id"]


@admin.register(BlogReview)
class BlogReviewAdmin(ImportExportModelAdmin):
    list_display = ["id", "author", "text","blog", "created_date"]
    list_display_links = ["id", "author", "text","blog", "created_date"]
    search_fields = ["id", "author", "text", "blog", "created_date"]
    ordering = ["id"]
