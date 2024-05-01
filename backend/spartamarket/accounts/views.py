from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import *
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import *


def get_object_by_username(username):
    return get_object_or_404(User, username=username)


@extend_schema(tags=['Account'], description="로그인을 위한 API")
class LoginAPIView(TokenObtainPairView):
    pass


@extend_schema(tags=['Account'], description="JWT 토큰 초기화를 위한 API")
class TokenRefreshAPIView(TokenRefreshView):
    pass


class LogoutAPIView(APIView):

    # 일반적으로 서버측에서 권장되지 않음
    @extend_schema(tags=['Account'], description="로그아웃을 위한 API", request=UserSerializer)
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "not logined"}, status=status.HTTP_400_BAD_REQUEST)

        auth_logout(request)
        return Response({"message": f"{request.user.username} logout"}, status=status.HTTP_200_OK)


class SignupAPIView(APIView):
    @extend_schema(tags=['Account'], description="회원가입을 위한 API", request=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            username = serializer.data['username']
            password = serializer.data['password']
            email = serializer.data['email'] if 'email' in serializer.data else ''
            nickname = serializer.data['nickname'] if 'nickname' in serializer.data else ''
            birthday = serializer.data['birthday'] if 'birthday' in serializer.data else None

            user = User.objects.create_user(username=username, password=password, email=email, nickname=nickname,
                                            birthday=birthday)
            # auth_login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'message': 'username already exists'}, status=e.status_code)


class ProfileAPIView(APIView):
    @extend_schema(tags=['Account'], description="프로필 수정을 위한 API", request=UserSerializer)
    def put(self, request, username):
        user = get_object_by_username(username)

        if not user:
            return Response({'message': f'{username} user not exists'})

        json_data = request.data

        email = json_data.get('email')
        nickname = json_data.get('nickname')
        birthday = json_data.get('birthday')

        if email != '':
            users = User.objects.filter(email=email)
            if users.exists():
                return Response({'message': f'email(={email}) already exists'})

        user.email = email
        user.nickname = nickname
        user.birthday = birthday

        user.save()
        user = get_object_by_username(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @extend_schema(tags=['Account'], description="프로필 조회를 위한 API", request=UserSerializer)
    def get(self, request, username):
        user = get_object_by_username(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@extend_schema(tags=['Account'], description="유저 리스트 조회 API", request=UserSerializer)
class UserListAPIView(APIView):
    def get(self, request):
        start = request.GET.get('start', default=0)
        end = request.GET.get('end', default=20)

        start = int(start)
        end = int(end)

        if start > end:
            start = 1
            end = 20

        users = User.objects.filter(id__range=(start, end))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class PasswordAPIView(APIView):
    @extend_schema(tags=['Account'], description="비밀번호 수정", request=UserSerializer)
    def put(self, request, username):
        user = get_object_by_username(username)

        if not user:
            return Response({'message': f'{username} user not exists'})

        new_password = request.data['new_password']
        if new_password is None:
            return Response({'message': 'password is None'})

        if new_password == '':
            return Response({'message': 'password is empty'})

        user.password = new_password
        user.save()

        return Response({'message': 'password changed successfully'})


class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Account'], description="계정 삭제", request=UserSerializer)
    def delete(self, request, username):
        user = get_object_by_username(username)
        if not user:
            return Response({'message': f'{username} user not exists'})

        password = request.data['password']
        if not user.check_password(password):
            return Response({'message': f'password is not match'})

        user.delete()
        return Response({'message': f'"{username}" is deleted.'})
