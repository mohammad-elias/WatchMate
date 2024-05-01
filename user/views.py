from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken


# Create your views here.
class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Registration Successful!'
            data['user_id'] = user.id
            data['username'] = user.username
            data['first_name'] = user.first_name
            data['last_name'] = user.last_name
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
            
        return Response(data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})
            

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
