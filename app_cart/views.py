from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_cart.cart import Cart
from app_cart.serializers import AddToCartSerializer


class AddToCartView(APIView):
    """
        add product to cart
    """

    serializer_class = AddToCartSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)

        if srz_data.is_valid(raise_exception=True):
            data = srz_data.validated_data
            cart = Cart(request)
            cart.add(data['product_id'], quantity=data['quantity'])
            return Response({'message': 'product added.'}, status=status.HTTP_200_OK)


class RetrieveCartView(APIView):
    """
        get and retrieve cart of user and set coupon
    """

    def get(self, request, coupon=None):

        if coupon is not None:
            cart_detail = Cart(request).get_list(coupon)
        else:
            cart_detail = Cart(request).get_list()

        data = {}
        for key, value in cart_detail.items():
            if key.isnumeric():
                data[key] = {
                    'quantity': value['quantity'],
                    'total_price': value['total_price'],
                }

        data['pay_price'] = cart_detail['pay_price']
        data['discount'] = cart_detail['discount']
        data['final_price'] = cart_detail['final_price']

        return Response(data, status=status.HTTP_200_OK)


class DeleteCartItemView(APIView):
    """
        delete 1 product from user cart
    """

    def delete(self, request, product_id):
        Cart(request).remove(product_id)
        return Response({'message': 'product deleted.'}, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    """
        delete all products from user cart
    """

    def delete(self, request):
        Cart(request).clear()
        return Response({'message': 'cart deleted.'}, status=status.HTTP_200_OK)