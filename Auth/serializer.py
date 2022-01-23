from django.contrib.auth import authenticate
from rest_framework import serializers
from Auth.models import CustomUser
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'name', )
        extra_kwargs = {
            'name': {'required': True},
        }


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = ('wrong password or username')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
class RefreshTokenSerializer(serializers.Serializer):
    refreshToken = serializers.CharField(write_only=True, required=True)
    class Meta:
        fields = ('refreshToken')
    def validate(self, attrs):
        if not attrs['refreshToken'] :
            raise serializers.ValidationError({"refreshToken": "this field is required"})
        return attrs


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(write_only=True, required=True)
    class Meta:
        fields = ('otp')
    def validate(self, attrs):
        if not attrs['otp'] :
            raise serializers.ValidationError({"otp": "this field is required"})
        return attrs

