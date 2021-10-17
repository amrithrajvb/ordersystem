from django.shortcuts import render
from owner.models import MyUser,Product,Order,OrderItems
from owner.serializers import UserCreationSerializer, SigninSerializer, AddProductSerializer, AddOrdersSerializer, \
    OrderItemSerializer
from rest_framework import mixins,generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class UserCreationView(generics.GenericAPIView,mixins.CreateModelMixin):
    model=MyUser
    serializer_class = UserCreationSerializer

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class SigninView(APIView):
    serializer_class=SigninSerializer

    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data["email"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=email,password=password)
            print(user)
            if user:
                login(request,user)
                token, create = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"INVALID USER"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)


class AddProductsView(generics.GenericAPIView,mixins.CreateModelMixin,
                  mixins.ListModelMixin):

    model=Product
    serializer_class = AddProductSerializer
    queryset = model.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class OrderView(generics.GenericAPIView,mixins.CreateModelMixin,mixins.ListModelMixin):
    model=Order
    serializer_class = AddOrdersSerializer
    queryset = Order.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.model.objects.filter(user=self.request.user)

    def get(self,request,*args,**kwargs):
        order_serializer = AddOrdersSerializer(Order.objects.all(),many=True)
        print("orders",order_serializer.data)
        for order in order_serializer.data:
            orderitem_queryset=OrderItems.objects.filter(order_id=order['id'])
            order_item_serializer = OrderItemSerializer(orderitem_queryset,many=True)
            order['orderitems'] = order_item_serializer.data
        return Response({
            'response_code': 200,
            'status': 'Ok',
            'orders': order_serializer.data
        })


    # def perform_create(self, serializer):
    #     user = self.request.user
    #     # serializer.user=self.request.user
    #     serializer.save(user=user)

    # def post(self,request,*args,**kwargs):
    #     cart=self.model.objects.get(user=self.request.user)
    #     if cart:
    #         total=cart.price
    #         user=MyUser.objects.get(user=self.request.user)
    #         order,created=self.model.get_or_create(price=total,user=user)
    #         order_items=OrderItems.objects.get(order=cart)
    #         for items in order_items:
    #             itemid=items.product
    #             quantity=items.quantity
    #             item_instance=Product.objects.get(product=items)
    #             orders_items,created=OrderItems.objects.get_or_create(order=order,product=item_instance,
    #                                                                   quantity=quantity)
    #             order.save()
    #             orders_items.save()
    #             if created:
    #                 items.delete()
    #         return Response(status=status.HTTP_200_OK)
    #     return self.create(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.role=="consumer":
            # order = {}
            data = request.data
            # data['id'] = self.request.user.id
            # order['user'] = data['user']
            # order['payment_method'] = data['payment_method']
            # order['price'] = data['price']
            # # order['discount'] = data['discount']
            # # order['final_amount'] = data['final_amount']
            # order['order_status'] = 'failed'
            # # order['ordered_on'] = datetime.now().date()
            # print(order)
            print(data)
            order_serializer = AddOrdersSerializer(data=data)
            print("hai",order_serializer)
            if order_serializer.is_valid():
                order_serializer_data = order_serializer.save(user=self.request.user)
                print("error",order_serializer_data)
                order_id = order_serializer_data.id
                for product in data['products']:
                    product['order'] = order_id

                    order_item_serializer = OrderItemSerializer(data=product)
                    if order_item_serializer.is_valid():
                        order_item_serializer.save()
                return Response({
                    'response_code': 200,
                    'status': 'Ok',
                    'message': 'Order Completed'
                })
            return Response({
                'response_code': 400,
                'status': 'Bad request',
                'message': 'Order Failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message":"sorry you don't have the permission "},status=status.HTTP_400_BAD_REQUEST)

