from rest_framework import generics, status
from rest_framework.response import Response
from orders.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.

###########################
# Testing Hello World API #
###########################
class OrderView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello Order")
    def get(self, request):
        return Response(data={'msg':"Hello Order"}, status=status.HTTP_200_OK)



#################################
# Create Order & Get ALl Orders #
#################################
class OrderCreationListView(generics.GenericAPIView):
    serializer_class=OrderCreationSerializer
    queryset=Order.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List All Orders Made")
    def get(self, request):
        orders=Order.objects.all()
        if orders:
            serializer=self.serializer_class(orders, many=True)
            return Response({"msg":"all orders data","data":serializer.data, "status":True}, status=status.HTTP_200_OK)
        else:
            return Response({"data":serializer.errors, "status":False}, status=status.HTTP_404)
    
    @swagger_auto_schema(operation_summary="Create A New Order")
    def post(self, request):
        data = request.data
        serializer=self.serializer_class(data=data)
        user = request.user
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



############################################
# Update/Delete Order & Get ALSingle Order #
############################################
class OrderDetailListView(generics.GenericAPIView):
    serializer_class=OrderDetailSerializer
    permission_classes=[IsAdminUser]

    @swagger_auto_schema(operation_summary="Retrive an Order by ID")
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer=self.serializer_class(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Update an Order by ID")
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        data = request.data
        user = request.user
        permission_classes=[IsAuthenticated]
        serializer=self.serializer_class(data=data, instance=order, partial=True)
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(operation_summary="Delete an Order by ID")
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response({"data":"Order Successfully Deleted.."}, status=status.HTTP_204_NO_CONTENT)



############################
# Order Status Update View #
############################
class UpdateOrderStatusView(generics.GenericAPIView):
    serializer_class=UpdateOrderStatusSerializer
    permission_classes=[IsAdminUser]

    @swagger_auto_schema(operation_summary="Update Order's Status")
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        data=request.data
        serializer=self.serializer_class(data=data, instance=order, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



####################
# User Orders View #
####################
class UserOrderView(generics.GenericAPIView):
    serializer_class=OrderDetailSerializer

    @swagger_auto_schema(operation_summary="Get All Orders for a User")
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        orders = Order.objects.all().filter(customer=user)
        serializer=self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



##########################
# User Order Detail View #
##########################
class UserOrderDetailView(generics.GenericAPIView):
    serializer_class=OrderDetailSerializer
    permission_classes=[IsAdminUser]

    @swagger_auto_schema(operation_summary="Get a User's Specific order")
    def get(self, request, user_id, order_id):
        user = User.objects.get(pk=user_id)
        orders = Order.objects.all().filter(customer=user).get(pk=order_id)
        serializer=self.serializer_class(instance=orders)
        return Response(data=serializer.data, status=status.HTTP_200_OK)