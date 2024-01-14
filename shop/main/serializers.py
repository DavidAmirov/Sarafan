from rest_framework import serializers

from .models import Cart, CartProduct, Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image')

    def get_fields(self):
        fields = super().get_fields()
        fields['children'] = CategorySerializer(many=True, read_only=True)
        return fields


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    original_image = serializers.ReadOnlyField(source="original_image.url")
    small_image = serializers.ReadOnlyField(source='small_image.url')
    big_image = serializers.ReadOnlyField(source='big_image.url')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug',
            'price', 'category',
            'original_image',
            'small_image', 'big_image',
        ]


class ProductInCartSerializer(serializers.ModelSerializer):
    price = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartProductCostSerializer(serializers.ModelSerializer):
    product = ProductInCartSerializer(read_only=True)
    cost = serializers.SerializerMethodField(read_only=True)

    def get_cost(self, obj):
        return obj.product.price * obj.quantity

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity', 'cost']


class CartSerializer(serializers.ModelSerializer):
    cartproduct = CartProductCostSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        total = 0
        for cp in obj.cartproduct.all():
            total += cp.product.price * cp.quantity
        return {"total": total}

    class Meta:
        model = Cart
        fields = ['user', 'cartproduct', 'total']


class CartPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['pk']


class ProductPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk']


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductPkSerializer(read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']


class CartProductCreateSerializer(serializers.ModelSerializer):
    cart = CartPkSerializer(read_only=True)
    product = ProductPkSerializer
    quantity = serializers.IntegerField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartProduct
        fields = ['cart', 'product', 'quantity', 'user']

    def create(self, validated_data):
        user = validated_data['user']
        cart = Cart.objects.get(user=user)
        product = validated_data['product']
        quantity = validated_data['quantity']
        new_cartproduct = CartProduct.objects.create(cart=cart, product=product, quantity=quantity)
        return new_cartproduct


class CartCleanSerializer(serializers.ModelSerializer):

    def update(self, obj, validated_data):
        for cartproduct in obj.cartproduct.all():
            cartproduct.delete()
        return obj

    class Meta:
        model = Cart
        fields = ['user', 'cartproduct']


class CartCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartProduct
        fields = ['user']

    def create(self, validated_data):
        user = validated_data['user']
        new_cart = Cart.objects.create(user=user)
        return new_cart
        