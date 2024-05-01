from django.http.request import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from .serializers import *


# Create your views here.
class ItemsListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    @extend_schema(tags=['Items'], description="Item 목록 조회를 위한 API")
    def get(self, request):
        paginator = self.pagination_class()

        category = request.GET.get('category')
        keyword = request.GET.get('keyword')
        sort = request.GET.get('sort')
        if not category:
            category = 'title'

        if not keyword:
            keyword = ''

        if not sort:
            sort = 'recent'

        items = None
        if category == 'title':
            items = Item.objects.filter(title__icontains=keyword)
        elif category == 'username':
            items = Item.objects.filter(user__username__icontains=keyword)
        elif category == 'content':
            items = Item.objects.filter(content__icontains=keyword)

        if sort == 'recent':
            items = items.order_by('-created_at')
        if sort == 'oldest':
            items = items.order_by('created_at')
        # elif sort == 'click':
        #     items = items.all().order_by('-click_count')
        # elif sort == 'like':
        #     items = items.annotate(like_count=Count('like_users')).order_by('-like_count')
        items = paginator.paginate_queryset(items, request)

        serializer = ItemSerializer(items, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(tags=['Items'], description="Item 생성을 위한 API", request=ItemSerializer)
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=['Items'], description="Item 수정을 위한 API", request=ItemSerializer)
    def put(self, request, id):
        item = get_object_or_404(Item, id=id)
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            item.title = serializer.validated_data['title']
            item.content = serializer.validated_data['content']
            item.category = serializer.validated_data['category']
            item.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=['Items'], description="Item 삭제를 위한 API", request=ItemSerializer)
    def delete(self, request, id):
        item = get_object_or_404(Item, id=id)
        item.delete()
        return Response(f'item deleted(id={item.id}, title={item.title}', status=status.HTTP_200_OK)


class CategoryAPIView(APIView):
    @extend_schema(tags=['Categories'], description="Category 생성을 위한 API", request=CategorySerializer)
    def post(self, request: HttpRequest):
        if not request.user.is_superuser:
            return Response({'message': 'only admin user can add categories'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeAPIView(APIView):
    @extend_schema(tags=['Likes'], description="좋아요 생성을 위한 API")
    def post(self, request: HttpRequest, id):
        User = get_user_model()
        username = request.data['user']
        item = get_object_or_404(Item, id=id)

        users = item.like_users.filter(username=username)
        if users.exists():
            return Response({'message': f'{username} is already in like system'})

        user = User.objects.get(username=username)
        item.like_users.add(user)

        return Response({'message': f'{username} add to like user'})
