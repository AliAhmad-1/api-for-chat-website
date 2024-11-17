from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        exstra_kwargs={
        'password':{'write_only':True}
        }

class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=100,required=True)
    class Meta:
        model=User
        fields=['username','password']

class ProfileSerializer(serializers.ModelSerializer):
    avatar=serializers.SerializerMethodField(method_name='get_avatar')
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','avatar']
    def get_avatar(self,obj):
        return obj.cover

class LogoutSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()
    def validate(self,data):
        
        self.token=data.get('refresh_token')
        return data
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')