import requests

from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User
from orders.models import Order
from study_partners.models import StudyPartner


class OrderAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            partner = StudyPartner.objects.filter(name=request.data.get('partner')).first()
            telegram = request.data.get('telegram')

            if email:

                user = User.objects.filter(email=request.data.get('email')).first()
                name = request.data.get('name')
                phone = request.data.get('phone')

                if user is None and name and phone:
                    user = User.objects.create_user(
                        first_name=name,
                        email=email,
                        phone=phone)

                if user:
                    order = Order.objects.create(
                        user_id=user,
                        study_partner=partner if partner else None)

                    try:
                        requests.post(
                            'http://localhost:8001/applications',
                            json={
                                'order_uid': str(order.uid),
                                'first_name': str(name),
                                'partner': order.study_partner.name if order.study_partner else '',
                                'user_email': str(email),
                                'user_phone': str(phone),
                                'user_telegram': str(telegram if telegram else ''),
                                'time': str(order.time),
                                'date': str(order.date)
                            })
                    except Exception as ex:
                        print(ex)

                    return Response(status=HTTP_201_CREATED)
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_200_OK)
