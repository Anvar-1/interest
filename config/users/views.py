import requests
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer, PasswordResetSerializer, \
    PasswordChangeSerializer
from .models import User
from django.conf import settings


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        # IP manzilini olish
        ip = self.request.META.get('REMOTE_ADDR')

        # Proksi-serverlar uchun tekshirish
        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            ip = self.request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]

        # Foydalanuvchini yaratish va IP manzilini saqlash
        user = serializer.save()
        user.ip_address = ip  # IP manzilini saqlash
        user.save()

    # def get_country_from_ip(self, ip_address):
    #     access_key = settings.IPSTACK_ACCESS_KEY  # API kalitini olamiz
    #     url = f'http://api.ipstack.com/{ip_address}?access_key={access_key}'
    #
    #     try:
    #         response = requests.get(url)
    #         if response.status_code == 200:
    #             data = response.json()
    #             print(data)  # Olingan ma'lumotlarni ko'rsatish
    #             return data.get('country_name')  # Davlat nomini qaytarish
    #         else:
    #             print(f"Xatolik: {response.status_code} - {response.text}")
    #             return None
    #     except Exception as e:
    #         print(f"Xatolik yuz berdi: {str(e)}")  # Xatolik haqida ma'lumot
    #         return None


class ProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "Bu himoyalangan API. Siz tizimga muvaffaqiyatli kirdingiz!"})


class UserLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            user = authenticate(phone=phone, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid Credentials'}, status=400)
        return Response(serializer.errors, status=400)

class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer

class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Muvaffaqiyatli chiqildi!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Xatolik yuz berdi!"}, status=status.HTTP_400_BAD_REQUEST)