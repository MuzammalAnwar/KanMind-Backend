from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterSerializer (serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        fullname = self.validated_data['fullname']
        if pw != repeated_pw:
            raise serializers.ValidationError("Passwords do not match")
        names = fullname.strip().split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ""
        username = fullname.replace(" ", "_")
        account = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.validated_data['email']
        )
        account.set_password(pw)
        account.save()

        return account


class LoginSerializer(AuthTokenSerializer):
    username = None
    email = serializers.EmailField(write_only=True)
    extra_kwargs = {
        'username': {'required': False},
    }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email does not exist")
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=user.username,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Invalid password')
        attrs['user'] = user
        return attrs


class EmailCheckQuerySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
