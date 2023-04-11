from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from django_back_api.utils import update_token


class ObtainAuthExpiringToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = update_token(user)
        return Response({'token': token.key})
