from django.urls import path,include
from .views import SearchProductListLiew


urlpatterns=[
    path("",SearchProductListLiew.as_view(),name="query"),

]
