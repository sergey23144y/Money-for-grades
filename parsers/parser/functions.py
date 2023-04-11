import requests
import json
import uuid
import re

from scrapy_parsers.parser_database import load_session, Course, CoursePrice, StudyPartner, Status, CourseOrigin

from bs4 import BeautifulSoup
from datetime import datetime
from transliterate import translit

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/102.0.5005.61 Safari/537.36',
           'accept': '*/*'}


def get_soup(response) -> BeautifulSoup or None:
    if response:
        return BeautifulSoup(response.text, 'lxml')
    else:
        return None


def get_html(url: str) -> requests.get or None:
    try:
        if url:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                return response
        return None
    except AttributeError:
        return None


def get_data_api(url: str) -> dict or None:
    try:
        response = requests.get(url)
        content = response.content
        return json.loads(content)
    except (AttributeError, json.JSONDecodeError) as ex:
        return None


def get_correct_url(host: str, url: str) -> str:
    if url and url.__contains__(host):
        return url
    elif url and url.__contains__('http'):
        return url
    else:
        return host + url


def get_price(price: str) -> int or None:
    try:
        result = re.sub('\D', '', price)
        return int(result)
    except:
        return None


def check_tag(tag, default=None, concatenation_string=''):
    if tag:
        return re.sub('|\n', '', tag.text.strip()) + concatenation_string
    else:
        return default


def check_data(data, default=None):
    if data:
        return data
    else:
        return default


def get_slag(name, session):
    result = translit(name, 'ru', reversed=True).strip().replace(' ', '-')
    temp_slag = re.sub(r'[.,"\'?:!;]', '', result)
    index_slag = 1
    while session.query(Course).filter_by(slag=result).one_or_none():
        result = f'{temp_slag}-{index_slag}'
        index_slag += 1
    return result


def get_vendor(session, index=1):
    while True:
        result = str(index).rjust(7, '0')
        if session.query(Course).filter_by(vendor=result).one_or_none() is None:
            break
        index += 1
    return result


def save_course(session: load_session, name: str, summary: str = '', title: str = '', definition: str = '',
                referral_link: str = '', duration_of_training: str = '', description: str = '', last_price: int = None,
                partner_id: int = None, rating: int = 0, is_active: bool = True):
    if name == '':
        return

    # get course from db, may be None
    course = session.query(Course).filter_by(
        name=str(name),
        study_partner_id=partner_id
    ).one_or_none()

    uid = str(uuid.uuid4()).replace('-', '')
    course_status = session.query(Status).filter_by(name='не опубликован').one_or_none()
    course_origin = session.query(CourseOrigin).filter_by(name='парсер').one_or_none()

    if course is None:
        course = Course(
            uid=uid,
            name=name,
            vendor=get_vendor(session),
            summary=summary,
            title=title,
            definition=definition,
            referral_link=referral_link,
            duration_of_training=duration_of_training,
            description=description,
            last_price=last_price,
            study_partner_id=partner_id,
            rating=rating,
            is_active=is_active,
            status_id=course_status.id,
            course_origin_id=course_origin.id,
            slag=get_slag(name, session),
            support_url='https://sokratinvest.ru/supportsokrat',
            updated_at=datetime.now()
        )
        session.add(course)
        course_price = CoursePrice(
            course_id=uid,
            price=last_price,
            date=datetime.now()
        )
    else:
        course.updated_at = datetime.now()
        course.last_price = last_price

        if course.status_id is None:
            course.status_id = course_status.id

        if course.course_origin_id is None:
            course.course_origin_id = course_origin.id

        if course.slag is None:
            course.slag = get_slag(name, session)

        if course.vendor is None:
            course.vendor = get_vendor(session)

        course_price = CoursePrice(
            course_id=course.uid,
            price=last_price,
            date=datetime.now()
        )
        
    session.add_all([course, course_price])
    session.commit()

