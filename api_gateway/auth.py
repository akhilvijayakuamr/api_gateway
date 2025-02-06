from userservice.service import APIUserClient
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


client = APIUserClient()


# Check Authorization

def authorization(request):
    for i in range(10):
        print("is working")
    auth_header = request.headers.get('Authorization')
    print(auth_header)
    if not auth_header or 'Bearer ' not in auth_header:
        return Response({'error':'Email Not Found Please Login Again'})
    token = auth_header.split('Bearer ')[1].strip()
    return client.check_auth(token)
    
    
    
    
# Checking funcation

@api_view(['GET'])
def health_check(request):
    return Response({"status": "Success"}, status=status.HTTP_200_OK)