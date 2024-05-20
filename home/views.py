from django.shortcuts import render
from django.views import View
from shop.models import Product
from shop.models import ClothingType,Sale
# Create your views here.

class HomeView(View):
    def get(self,request):
        products_by_type = {}
        for clothing_type in ClothingType.choices:
            type_key = clothing_type[0]
            pros = Product.objects.filter(types=type_key)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",pros,len(pros))
            if len(pros) != 0:
                products_by_type[type_key] = pros
        print(products_by_type)
        products = Product.objects.all()
        sales = Sale.objects.all()
        best_products = Product.objects.order_by("-viewed")[:4]
        context = {
            "best_products": best_products,
            "products_by_type": products_by_type,
            "sales": sales,
            "types": ClothingType.choices,
        }
        return render(request, "home/home.html",context)

class AboutView(View):
    def get(self,request):
        return render(request, "home/about.html")
    

class ContactView(View):
    def get(self,request):
        return render(request, "home/contact.html")