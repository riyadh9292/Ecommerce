from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView

# Create your views here.
class SearchProductListLiew(ListView):
    #queryset=Product.objects.all()
    template_name="search/view.html"

    def get_context_data(self,*args,**kwargs):
        context=super(SearchProductListLiew,self).get_context_data(*args,**kwargs)
        context['query']=self.request.GET.get('q')
        return context


    def get_queryset(self,*args,**kwargs):
        request=self.request
        print(request.GET)
        query=request.GET.get('q')
        print(query)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.features()
