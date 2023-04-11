import datetime

from rest_framework.renderers import BaseRenderer
from django.utils.xmlutils import SimplerXMLGenerator
from io import StringIO


class FeedXMLRenderer(BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)

        xml.startDocument()
        xml.startElement('yml_catalog', {'date': str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))})
        xml.startElement('shop', {})

        xml.startElement('name', {})
        xml.characters(data.study_partner.name)
        xml.endElement('name')

        xml.startElement('company', {})
        xml.characters(data.study_partner.name)
        xml.endElement('company')

        xml.startElement('url', {})
        xml.characters('https://sokratapp.ru/')
        xml.endElement('url')

        xml.startElement('email', {})
        xml.characters('office@sokratapp.ru')
        xml.endElement('email')

        xml.startElement('picture', {})
        xml.characters('https://sokratapp.ru//static/media/header-logo-brain.0e858cde.svg')
        xml.endElement('picture')

        xml.startElement('description', {})
        xml.characters('office@sokratapp.ru')
        xml.endElement('description')

        xml.startElement('currencies', {})
        xml.startElement('currency', {'id': 'RUR', 'rate': '1'})
        xml.endElement('currency')
        xml.endElement('currencies')

        xml.startElement('offers', {})
        xml.startElement('offer', {'id': str(data.pk)})

        xml.startElement('name', {})
        xml.characters(data.name)
        xml.endElement('name')

        xml.startElement('url', {})
        xml.characters(f'https://sokratapp.ru/courses/{data.slag}')
        xml.endElement('url')

        xml.startElement('categoryId', {})
        xml.characters(data.course_category_webmaster.id)
        xml.endElement('categoryId')

        xml.startElement('price', {})
        xml.characters(str(data.last_price))
        xml.endElement('price')

        xml.startElement('currencyId', {})
        xml.characters('RUR')
        xml.endElement('currencyId')

        xml.startElement('param', {'name': 'Продолжительность', 'unit': data.type_of_training.name})
        xml.characters(str(data.duration_of_training))
        xml.endElement('param')

        xml.startElement('param', {'name': 'План', 'unit': 'Модуль 1'})
        xml.characters('Обзор')
        xml.endElement('param')

        xml.startElement('param', {'name': 'План', 'unit': 'Модуль 2'})
        xml.characters('Основной этап обучение')
        xml.endElement('param')

        xml.startElement('param', {'name': 'План', 'unit': 'Модуль 3'})
        xml.characters('')
        xml.endElement('param')

        xml.startElement('description ', {})
        xml.characters(data.description)
        xml.endElement('description')

        xml.endElement('offer')
        xml.endElement('offers')

        xml.endElement('shop')
        xml.endElement('yml_catalog')
        xml.endDocument()

        return stream.getvalue()