from django.urls import path,include
from .views import ProductListLiew,ProductDetailSlugView


urlpatterns=[
    path("",ProductListLiew.as_view(),name="list"),
    path("<slug:slug>/",ProductDetailSlugView.as_view(),name="detail")
]
