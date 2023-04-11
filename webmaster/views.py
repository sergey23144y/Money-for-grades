import requests
import environ
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.status import HTTP_201_CREATED

from courses.models import Course
from webmaster.renderers import FeedXMLRenderer


env = environ.Env()
environ.Env.read_env()


# Create your views here
class FeedAPIView(APIView):

    renderer_classes = [FeedXMLRenderer]

    def get(self, request, *args, **kwargs):
        queryset = Course.objects.filter(uid=self.kwargs['pk']).first()
        return Response(queryset)


class YandexWebmasterApiView(APIView):

    permission_classes = (IsAdminUser,)
    app_name = 'https://sokratapp.ru/'
    webmaster_yandex_url = 'https://api.webmaster.yandex.net/'
    headers_auth = {
        'Authorization': 'OAuth ' + env.str('YANDEX_WEBMASTER_TOKEN'),
        'Content-type': 'application/json',
    }

    def post(self, request, *args, **kwargs):

        course_id = kwargs.get('pk')
        # get user id
        response_user = requests.get(f'{self.webmaster_yandex_url}v4/user/', headers=self.headers_auth)

        # feed for webmaster
        feed = json.dumps({
            'feed': {
                'url': f'https://{request.META["HTTP_HOST"]}/api/webmaster/feed/{course_id}/',
                'type': 'EDUCATION',
                'regionIds': [
                    225
                ]
            }
        })

        if response_user.status_code == 200:
            # get user_id
            user_id = json.loads(response_user.text)['user_id']
            host_id = self.get_host(user_id)
            response_code = requests.get(f'{self.webmaster_yandex_url}v4/user/{user_id}/hosts/{host_id}/verification', headers=self.headers_auth)
            verification_info = json.loads(response_code.text)
            if verification_info['verification_state'] == 'VERIFIED':

                create_feed = requests.post(
                    url=f'{self.webmaster_yandex_url}v4/user/{user_id}/hosts/{host_id}/feeds/add/start',
                    headers=self.headers_auth,
                    data=feed,
                )

                info_feed = requests.get(
                    url=f'{self.webmaster_yandex_url}v4/user/{user_id}/hosts/{host_id}/feeds/add/info',
                    headers=self.headers_auth,
                    data=create_feed.text
                )

                if info_feed.status_code == 200:
                    return Response(status=HTTP_201_CREATED)
                else:
                    return Response(status=info_feed.status_code)

            elif verification_info['verification_state'] == 'NONE':
                Response(requests.post(f'{self.webmaster_yandex_url}v4/user/{user_id}/hosts/{host_id}/verification?verification_type=META_TAG', headers=self.headers_auth))
            else:
                Response(response_code)
        else:
            Response(response_user)

    def get_host(self, user_id):
        requests.post(f'{self.webmaster_yandex_url}v4/user/{user_id}/hosts', headers=self.headers_auth, data=json.dumps({'host_url': self.app_name}))
        response_hosts = requests.get(f'{self.webmaster_yandex_url}v4/user/{user_id}/hosts', headers=self.headers_auth)
        if response_hosts.status_code == 200:
            hosts = json.loads(response_hosts.text)['hosts']
            for host in hosts:
                if host['unicode_host_url'] == self.app_name:
                    return host['host_id']
        return ''