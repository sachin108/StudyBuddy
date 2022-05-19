from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)
