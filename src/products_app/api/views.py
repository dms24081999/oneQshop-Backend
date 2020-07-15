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
from django.conf import settings
from django.core import serializers as django_serializers
import json

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


class ProductImagesFullInfoAPIView(ModelViewSet):
    lookup_field = "pk"
    serializer_class = ProductImagesSerializer
    permission_classes = [AllowAny]
    queryset = ProductImages.objects.all()

    # List GET
    def get_queryset(self, *args, **kwargs):
        context = super(ProductImagesFullInfoAPIView, self).get_queryset(
            *args, **kwargs
        )
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


class ImagesTrainingAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        products = dict()
        for product in Products.objects.all():
            for images in ProductImages.objects.filter(id__in=product.images.all()):
                if images.main_image == True:
                    products[product.id] = images.image.url
                    break
        print(products)
        return Response(products)


class ProductVisualSimilarityRecommendationAPI(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        self.filename = settings.PRODUCT_VISUAL_RECOMMEND_FILENAMES
        self.model = settings.PRODUCT_VISUAL_RECOMMEND_MODEL
        self.nb_closest_images = settings.PRODUCT_VISUAL_RECOMMEND_TOTAL

    def retrieve_most_similar_products(self, given_img):
        print("-----------------------------------------------------------------------")
        print("most similar products:")
        closest_imgs = self.model[given_img].sort_values(ascending=False)[1:].index
        closest_imgs_scores = self.model[given_img].sort_values(ascending=False)[1:]
        # print(closest_imgs)
        # print(closest_imgs_scores)
        print("-----------------------------------------------------------------------")

        recommend = list()
        for i in range(0, self.nb_closest_images):
            recommend.append(closest_imgs[i])
            print(
                str(closest_imgs[i]),
                "| similarity score :",
                closest_imgs_scores[(closest_imgs[i])],
            )
        return recommend

    def get(self, request, pk, *args, **kwargs):
        # print(self.filename)
        products_recommend = []
        if str(pk) in self.filename:
            recommend = self.retrieve_most_similar_products(str(pk))
            queryset = Products.objects.filter(id__in=recommend)
            serializer = ProductsSerializer(queryset, many=True)
            products_recommend = serializer.data
        return Response(products_recommend)
        ## Alternative Method
        #     products_recommend = django_serializers.serialize('json', data)
        # return Response(json.loads(products_recommend), content_type="application/json")
