from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        role = None
        check=int(user.user_type)
        if check == 1:
            role = 'inspector'
        elif check == 2:
            role = 'buyer'
        elif check == 3:
            role = 'seller'

        response_data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'role': role
        }

        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie('access_token', str(refresh.access_token), httponly=True)
        response.set_cookie('refresh_token', str(refresh), httponly=True)
        return response

class TokenVerificationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve the token from the request cookies
        access_token = request.COOKIES.get('access_token')
        role = request.GET.get('role')

        if access_token:
            if role:
                valid_roles = ['inspector', 'buyer', 'seller']
                if role.lower() in valid_roles:
                    return Response({'message': f'Token verified successfully for role: {role}'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid role provided'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Token verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Access token not found in cookies'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')  # or extract from cookies
    if refresh_token:
        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)
            return Response({'access_token': access_token})
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)
    else:
        return Response({'error': 'Refresh token is missing'}, status=400)

class LogoutAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        try:
            response = Response()
            refresh_token = request.COOKIES.get('refresh_token')
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            if refresh_token:
                RefreshToken(refresh_token).blacklist()
            response.data = {
                'message': 'success'
            }
            return response
        except Exception as e:
            # Handle any errors occurred during logout
            return Response({'error': 'An error occurred while logging out'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)