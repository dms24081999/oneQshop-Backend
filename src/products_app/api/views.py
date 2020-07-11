from rest_framework.views import APIView
from .serializers import *
from ..models import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

Users = get_user_model()


class ProductsFullInfoAPIView(ModelViewSet):
    lookup_field = "pk"
    serializer_class = ProductsSerializer
    permission_classes = [AllowAny]
    queryset = Products.objects.all()

    # List GET
    def get_queryset(self, *args, **kwargs):
        context = super(ProductsFullInfoAPIView, self).get_queryset(*args, **kwargs)
        qs = self.queryset
        query = self.request.GET.get("s")
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(short_name__icontains=query)
                | Q(barcode__icontains=query)
            ).distinct()
        return qs

    # GET
    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # PUT
    def update(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    # PATCH
    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    # DELETE
    def destroy(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesFullInfoAPIView(ModelViewSet):
    lookup_field = "pk"
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]
    queryset = Categories.objects.all()

    # List GET
    def get_queryset(self, *args, **kwargs):
        context = super(CategoriesFullInfoAPIView, self).get_queryset(*args, **kwargs)
        qs = self.queryset
        query = self.request.GET.get("s")
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(short_name__icontains=query)
                | Q(description__icontains=query)
            ).distinct()
        return qs

    # GET
    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # PUT
    def update(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    # PATCH
    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    # DELETE
    def destroy(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Auth not provided."}, status=400)
        else:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
