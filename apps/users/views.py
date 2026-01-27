"""
Views para autenticación y gestión de usuarios.

Usamos APIView para auth porque no necesitamos CRUD completo.
"""

from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register
    
    Registrar nuevo usuario.
    No requiere autenticación (obviously).
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Auto-login después del registro
        login(request, user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST /api/auth/login
    
    Login con username/password.
    Crea una session con cookie y devuelve CSRF token.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        # Obtener/generar el CSRF token
        csrf_token = get_token(request)
        
        return Response({
            'message': 'Login exitoso',
            'user': UserSerializer(user).data,
            'csrf_token': csrf_token
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/auth/logout
    
    Cerrar sesión y destruir cookie.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    GET /api/auth/me
    
    Obtener usuario actual.
    Útil para verificar si hay sesión activa.
    También devuelve el CSRF token.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        csrf_token = get_token(request)
        
        return Response({
            'user': UserSerializer(request.user).data,
            'csrf_token': csrf_token
        })


class UpdateProfileView(generics.UpdateAPIView):
    """
    PATCH /api/auth/profile
    
    Actualizar perfil del usuario actual.
    No permite cambiar username ni password (hay endpoints separados).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        # Prevenir cambio de username (dato sensible)
        if 'username' in request.data:
            return Response({
                'error': 'No se puede cambiar el username. Contactá a soporte.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return super().update(request, *args, **kwargs)


class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password
    
    Cambiar contraseña del usuario actual.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        }, status=status.HTTP_200_OK)


class TestAuthView(APIView):
    """
    GET /api/auth/test/
    
    Endpoint de prueba para debug de autenticación.
    Muestra estado de sesión, cookies y usuario actual.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'authenticated': request.user.is_authenticated,
            'user': str(request.user),
            'session_key': request.session.session_key,
            'cookies': list(request.COOKIES.keys()),
        })