import binascii
import datetime
import os
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from .serializer import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from Auth.serializer import RegisterSerializer, RefreshTokenSerializer,OTPSerializer
from .models import RefreshToke,CustomUser,Otp


@api_view(['POST'])
def signUp(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={
            "success": True,
            "message": "New user added successfully "
        }, status=status.HTTP_201_CREATED)
    return Response(data={
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):  # login function
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="email",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        refreshToken = binascii.hexlify(os.urandom(20)).decode()
        RefreshToke(user_id=user.id, refreshToken=refreshToken).save()
        return Response({'accessToken': token.key, 'refreshToken': refreshToken, 'userId': user.id, "name": user.name})


class RefreshToken(APIView):  # refresh token
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = RefreshToke.objects.get(refreshToken__exact=serializer.validated_data["refreshToken"])
            if token and (token.created_at.replace(tzinfo=None) + datetime.timedelta(
                    minutes=settings.REFRESH_TOKEN_EXPIRED_AFTER_MINUTES)).replace(
                tzinfo=None) < datetime.datetime.now():
                Token.objects.get(user_id=token.user.pk).delete()
                newToken = Token.objects.create(user=token.user)
                print(newToken.key)
                return Response(data={
                    "success": True,
                    "accessToken": newToken.key
                }, status=status.HTTP_201_CREATED)
            return Response(data={
                "success": False,
                "errors": "Can't find this token"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ActiveAccount(APIView):
    def post(self,request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp=Otp.objects.get(otp__exact=serializer.validated_data["otp"])
            if otp and (otp.created_at.replace(tzinfo=None) + datetime.timedelta(
                    minutes=settings.OTP_EXPIRED_AFTER_MINUTES)).replace(
                tzinfo=None) < datetime.datetime.now():
                account= CustomUser.objects.get(pk=otp.user_id)
                account.is_active=True
                account.save()
                otp.delete()
                return Response(data={
                    "success": True,
                    "message": "Your account is activated successfully"
                }, status=status.HTTP_201_CREATED)
            return Response(data={
                "success": False,
                "errors": "your otp expired"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
