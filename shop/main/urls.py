from rest_framework.routers import DefaultRouter
from django.urls import path

from main.views import *

urlpatterns = [
    path('cart/', CartCreateView.as_view()),
    path('cart/<int:pk>/', CartView.as_view()),
    path('cart/add/', CartProductCreateView.as_view()),
    path('cartchange/<int:pk>/', CartProductUpdateView.as_view()),
    path('cart/clean/<int:pk>/', CartCleanView.as_view()),
    ]

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns.extend(router.urls)
