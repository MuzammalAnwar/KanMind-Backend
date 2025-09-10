from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import permissions, status
from .serializers import RegisterSerializer, LoginSerializer, EmailCheckQuerySerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        allowed_fields = {"fullname", "email", "password", "repeated_password"}
        received_fields = set(request.data.keys())
        extra_fields = received_fields - allowed_fields
        if extra_fields:
            return Response(
                {"error": f"Invalid fields in request: {', '.join(extra_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'fullname': f"{saved_account.first_name} {saved_account.last_name}".strip(),
                'email': saved_account.email,
                'user_id': saved_account.id,
                'token': token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'fullname': f"{user.first_name} {user.last_name}".strip(),
            'email': user.email,
            'user_id': user.id,
            'token': token.key
        }
        return Response(data)


User = get_user_model()


class EmailCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = EmailCheckQuerySerializer(data=request.query_params)
        q.is_valid(raise_exception=True)
        email = q.validated_data["email"].strip()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise NotFound("Email nicht gefunden.")

        return Response({
            "id": user.id,
            "email": user.email,
            "fullname": f"{user.first_name} {user.last_name}".strip()
        }, status=status.HTTP_200_OK)
