from rest_framework.response import Response
from userservice.service import APIUserClient


client = APIUserClient()

def authorization(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'Bearer ' not in auth_header:
        return Response({'error':'Email Not Found Please Login Again'})
    token = auth_header.split('Bearer ')[1].strip()
    return client.check_auth(token)
    