from rest_framework import serializers
from .models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)       # Declaring password as a CharField with write_only=True ensures that the 
                                                            # serializer will expect this field in the input data and validate it accordingly.

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')
       # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''), #  The user's first name is set, or an empty string if not provided.
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(user)
                data['access'] = str(refresh.access_token)
                data['refresh'] = str(refresh)
            else:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')
        return data

# forgot password

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value
    
# Reset password


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        # Here you would check if the token exists in the database and is valid
        if not CustomUser.objects.filter(password_reset_token=value).exists():
            raise serializers.ValidationError("Invalid or expired token.")
        return value


