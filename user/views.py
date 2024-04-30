from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status


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
            

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
