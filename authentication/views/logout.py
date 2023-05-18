from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response()
