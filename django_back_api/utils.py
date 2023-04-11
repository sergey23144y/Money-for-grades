import binascii
import os
from datetime import datetime
import datetime as dtime
from datetime import timedelta
import pytz
from PIL import Image
from os import remove as remove_file

from rest_framework.authtoken.models import Token

USER_FIELDS = ['email']


def convert_image(image, height, width):
    img_path = image.path
    img = Image.open(img_path)
    if img.height > height or img.width > width:
        output_size = (width, height)
        img.thumbnail(output_size, Image.ANTIALIAS)
        img.save(image.path, format='png')


def rename_image(name):
    img_name = name.split('.')[:-1]
    img_name.append('png')
    new_path = '.'.join(img_name)
    return new_path


def check_token_expired(token):
    utc_now = datetime.now(dtime.timezone.utc)
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    return token.created < utc_now - timedelta(days=2)


def update_token(user):
    token = Token.objects.filter(user=user).first()
    if token:
        is_expired = check_token_expired(token)
        if is_expired:
            token.delete()
            token = Token.objects.create(user=user)
            token.save()
        return token
    token = Token.objects.create(user=user)
    token.save()
    token_key = token.key
    return token_key


def generate_email():
    email = f'{binascii.hexlify(os.urandom(15)).decode()}@{binascii.hexlify(os.urandom(5)).decode()}.com'
    return email
