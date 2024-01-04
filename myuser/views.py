from rest_framework import permissions, status
from rest_framework.response import Response
from myuser.models import MyUser
from myuser.serializer import MyUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import make_password


@permission_classes([permissions.AllowAny])
class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = MyUser(username=username, password=make_password(password))
        user.save()
        user_data = MyUserSerializer(user).data
        return Response(user_data, status=status.HTTP_201_CREATED)


@permission_classes([permissions.AllowAny])
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = MyUser.objects.filter(username=username).first()
            if user and user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
