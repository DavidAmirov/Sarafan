from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .models import *
from .permissions import IsOwner, IsOwnerCartProduct
from  .serializers import *


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartCreateView(generics.CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartCreateSerializer


class CartView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    http_method_names = ['get']
    serializer_class = CartSerializer
    permission_classes = (IsOwner, )


class CartProductCreateView(generics.CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductCreateSerializer
    permission_classes = (IsOwnerCartProduct, )


class CartProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = (IsOwnerCartProduct,)


class CartCleanView(generics.RetrieveUpdateAPIView):
    queryset =Cart.objects.all()
    http_method_names = ['get', 'post', 'put']
    serializer_class =CartCleanSerializer
    permission_classes = (IsOwner,)
