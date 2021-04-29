from rest_framework.views import APIView
from .serializers import *
from .models import *
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
import pandas as pd
from mainsite.pagination import *
from django.db.models import Sum

Users = get_user_model()


from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


class MyUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsFullInfoAPIView(ModelViewSet):
    lookup_field = "pk"
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all()
    pagination_class = ProductsLimitOffsetPagination

    def get_serializer_context(self):
        context = super(ProductsFullInfoAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    # List GET
    def get_queryset(self, *args, **kwargs):
        context = super(ProductsFullInfoAPIView, self).get_queryset(*args, **kwargs)
        qs = self.queryset
        searchQuery = self.request.GET.get("s")
        categoryQuery = self.request.GET.get("category")
        if categoryQuery is not None:
            qs = qs.filter(categories__id=int(categoryQuery))
        if searchQuery is not None:
            qs = qs.filter(
                Q(name__icontains=searchQuery)
                | Q(short_name__icontains=searchQuery)
                | Q(barcode__icontains=searchQuery)
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

    # List GET
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = {"count": len(serializer.data), "results": serializer.data}
        return Response(response)

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


class ProductImagesTrainingAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        products = dict()
        for product in Products.objects.all():
            for images in ProductImages.objects.filter(id__in=product.images.all()):
                if images.main_image == True:
                    products[product.id] = images.image.url
                    break
        return Response(products)


class GetCartCountAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = 0
        for cart in Carts.objects.filter(user_id=request.user.id):
            count = count + cart.count
        return Response({"count": count})


class ProductNamesTrainingAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        products = dict()
        for product in Products.objects.all():
            products[product.id] = product.name
        return Response(products)


class ProductBarCodesAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        products = dict()
        for product in Products.objects.all():
            products[product.barcode] = product.id
        response = {"count": len(products), "results": products}
        return Response(response)


class ProductVisualSimilarityRecommendationAPI(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        self.ids = settings.PRODUCT_VISUAL_RECOMMEND_IDS
        self.model = settings.PRODUCT_VISUAL_RECOMMEND_MODEL
        self.nb_closest = settings.PRODUCT_VISUAL_RECOMMEND_TOTAL

    def retrieve_most_similar_products(self, given_id):
        print("-----------------------------------------------------------------------")
        print("most similar products:")
        closest_imgs = self.model[given_id].sort_values(ascending=False)[1:].index
        closest_imgs_scores = self.model[given_id].sort_values(ascending=False)[1:]
        print("-----------------------------------------------------------------------")
        recommend = list()
        for i in range(0, self.nb_closest):
            recommend.append(int(closest_imgs[i]))
            print(
                str(closest_imgs[i]),
                "| similarity score :",
                closest_imgs_scores[(closest_imgs[i])],
            )
        return recommend

    def get(self, request, pk, *args, **kwargs):
        # print(self.ids)
        products_recommend = []
        if str(pk) in self.ids:
            recommend = self.retrieve_most_similar_products(str(pk))
            queryset = [Products.objects.get(id=id) for id in recommend]
            serializer = ProductsSerializer(
                queryset, context={"request": request}, many=True
            )
        response = {"count": len(serializer.data), "results": serializer.data}
        return Response(response)
        ## Alternative Method
        #     products_recommend = django_serializers.serialize('json', data)
        # return Response(json.loads(products_recommend), content_type="application/json")


class ProductNameSimilarityRecommendationAPI(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        self.ids = settings.PRODUCT_NAME_RECOMMEND_IDS
        self.model = settings.PRODUCT_NAME_RECOMMEND_MODEL
        self.nb_closest = settings.PRODUCT_NAME_RECOMMEND_TOTAL

    def retrieve_most_similar_products(self, given_id):
        print("-----------------------------------------------------------------------")
        print("most similar products:")
        closest_name = self.model[given_id].sort_values(ascending=False)[1:].index
        closest_name_scores = self.model[given_id].sort_values(ascending=False)[1:]
        print("-----------------------------------------------------------------------")
        recommend = list()
        for i in range(0, self.nb_closest):
            recommend.append(int(closest_name[i]))
            print(
                str(closest_name[i]),
                "| similarity score :",
                closest_name_scores[(closest_name[i])],
            )
        return recommend

    def get(self, request, pk, *args, **kwargs):
        # print(self.ids)
        products_recommend = []
        if str(pk) in self.ids:
            recommend = self.retrieve_most_similar_products(str(pk))
            queryset = [Products.objects.get(id=id) for id in recommend]
            serializer = ProductsSerializer(queryset, many=True)
            products_recommend = serializer.data
        return Response(products_recommend)


class UserBasedCollaborativeFilteringRecommendationAPI(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        self.pivot_df = settings.USER_BASED_COLLABORATIVE_FILTERING_PIVOT_DF
        self.preds_df = settings.USER_BASED_COLLABORATIVE_FILTERING_PREDS_DF
        self.num_recommendations = (
            settings.USER_BASED_COLLABORATIVE_FILTERING_RECOMMEND_TOTAL
        )

    def recommend_items(self, userID):
        try:
            sorted_user_ratings = self.pivot_df.loc[userID].sort_values(ascending=False)
            sorted_user_predictions = self.preds_df.loc[userID].sort_values(
                ascending=False
            )
        except:
            return []
        temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis=1)
        temp.index.name = "Recommended Items"
        temp.columns = ["user_ratings", "user_predictions"]
        temp = temp.loc[temp.user_ratings == 0]
        temp = temp.sort_values("user_predictions", ascending=False)
        print(
            "\nBelow are the recommended items for user(user_id = {}):\n".format(userID)
        )
        recommendations = temp.head(self.num_recommendations)
        print(recommendations)
        recommendations_list = recommendations.index.values.tolist()
        return recommendations_list

    def get(self, request, *args, **kwargs):
        # print(self.ids)
        products_recommend = []
        recommend = self.recommend_items(request.user.pk)
        queryset = [Products.objects.get(id=id) for id in recommend]
        serializer = ProductsSerializer(queryset, many=True)
        products_recommend = serializer.data
        return Response(products_recommend)


class ItemBasedCollaborativeFilteringRecommendationAPI(APIView):
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        self.pivot_df = settings.ITEM_BASED_COLLABORATIVE_FILTERING_PIVOT_DF
        self.num_recommendations = (
            settings.ITEM_BASED_COLLABORATIVE_FILTERING_RECOMMEND_TOTAL
        )

    def recommend_items(self, itemID):
        df_features = self.pivot_df.pivot(
            index="user_id", columns="product_id", values="ratings"
        ).fillna(0)
        try:
            df_id = df_features[itemID]
        except:
            return []
        similar = df_features.corrwith(df_id)
        similar = pd.DataFrame(similar, columns=["Correlation"])
        similar.dropna(inplace=True)
        similar.sort_values("Correlation", ascending=False)
        similar = similar[1 : self.num_recommendations + 1]
        print(similar)
        recommendations_list = similar.index.values.tolist()
        return recommendations_list

    def get(self, request, pk, *args, **kwargs):
        # print(self.ids)
        products_recommend = []
        recommend = self.recommend_items(pk)
        queryset = [Products.objects.get(id=id) for id in recommend]
        serializer = ProductsSerializer(queryset, many=True)
        products_recommend = serializer.data
        return Response(products_recommend)


class CartsFullInfoAPIView(ModelViewSet):
    lookup_field = "pk"
    serializer_class = CartsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Carts.objects.all()

    def get_serializer_context(self):
        context = super(CartsFullInfoAPIView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self, *args, **kwargs):
        context = super(CartsFullInfoAPIView, self).get_queryset(*args, **kwargs)
        qs = self.queryset
        query = self.request.GET.get("s")
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(short_name__icontains=query)
                | Q(description__icontains=query)
            ).distinct()
        return qs

    # List GET
    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(user_id=request.user.id)
        price = 0
        for cart in queryset:
            price = price + (Products.objects.get(id=cart.id).price * cart.count)
        serializer = self.get_serializer(queryset, many=True)
        response = {
            "count": len(serializer.data),
            "price": price,
            "results": serializer.data,
        }
        return Response(response)

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
            serializer = self.get_serializer(instance)
            product = Products.objects.get(id=instance.product_id.id)
            product.count = product.count + instance.count
            product.save()
            self.perform_destroy(instance)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class InvoicesFullInfoAPIView(ModelViewSet):
    lookup_field = "pk"
    serializer_class = InvoicesSerializer
    permission_classes = [AllowAny]
    queryset = Invoices.objects.all()

    # List GET
    def get_queryset(self, *args, **kwargs):
        context = super(InvoicesFullInfoAPIView, self).get_queryset(*args, **kwargs)
        return self.queryset

    # List GET
    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(user_id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        response = {"count": len(serializer.data), "results": serializer.data}
        return Response(response)

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
