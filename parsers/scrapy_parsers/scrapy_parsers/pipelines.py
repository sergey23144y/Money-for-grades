# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import traceback
import uuid
from datetime import datetime
from unicodedata import normalize

from parser_database import load_session, StudyPartner, Course, CoursePrice, TypeOfLearning


# from parser_database import load_session, Course, CoursePrice, StudyPartner, TypeOfLearning


class ScrapyParserPipeline:
    def __init__(self):
        self.session = load_session()

    def process_item(self, item, spider):
        print('process')
        if "htmlacademy_name" in item.keys() or 'htmlacademy_price' in item.keys():
            htmlacademy_partner = self.session.query(StudyPartner).filter_by(name='HTML Academy').first()
            course = self.session.query(Course).filter_by(
                name=str(item['htmlacademy_name'][0]),
                study_partner_id=htmlacademy_partner.id
            ).one_or_none()
            if course is None:
                uid = str(uuid.uuid4()).replace('-', '')
                course = Course(
                    uid=uid,
                    name=str(item['htmlacademy_name'][0]) if str(item['htmlacademy_name'][0]) else '',
                    summary='',
                    title='',
                    definition='',
                    referral_link='',
                    duration_of_training='',
                    description='',
                    last_price=int(item['htmlacademy_price'].replace('\xa0', '')) if item['htmlacademy_price'] else None,
                    rating=0,
                    study_partner_id=htmlacademy_partner.id,
                    is_active=True,
                    updated_at=datetime.now()
                )
                self.session.add(course)
                course_price = CoursePrice(
                    course_id=uid,
                    price=int(item['htmlacademy_price'].replace('\xa0', '')) if item['htmlacademy_price'] else None,
                    date=datetime.now()
                )
                self.session.add(course_price)
                self.session.commit()
                print('html added')
            else:
                course.updated_at = datetime.now()
                course.last_price = int(item['htmlacademy_price'].replace('\xa0', '')) if item['htmlacademy_price'] else None
                course_price = CoursePrice(
                    course_id=course.uid,
                    price=int(item['htmlacademy_price'].replace('\xa0', '')) if item['htmlacademy_price'] else None,
                    date=datetime.now()
                )
                self.session.add(course_price)
                self.session.commit()
                print('html updated')
        else:
            try:
                # course_program = '\n'.join(item['course_program'])
                # teachers = '\n'.join(item['teachers'])
                type_of_learning_dict = {
                    'Онлайн курс': 'онлайн',
                    'Видеокурс': 'офлайн',
                    'Очный': 'очная',
                    'Корпоративный': 'корпоративная'
                }
                name = str(item['name'])
                training_time = ' \n'.join(list(map(lambda x: ' '.join(x.split()), item['training_time'][1:])))
                description = '\n'.join(set(map(lambda x: ' '.join(x.split()), item['description'])))
                price = ' '.join(re.findall('\d+', item['price'])) if item['price'] else None
                # currency = ' '.join(re.findall('[a-zA-Zа-яА-ЯёЁ]+', item['price'])) if item['price'] is not None else ''
                rshu_partner = self.session.query(StudyPartner).filter_by(name='Русская школа управления').first()
                type_of_learning_re = ' '.join(re.findall('[а-яА-ЯёЁ]+', item['type_of_learning'][0]))
                type_of_learning = self.session.query(TypeOfLearning).filter_by(
                    name=type_of_learning_dict[type_of_learning_re]
                ).one_or_none()
                course = self.session.query(Course).filter_by(
                    name=name,
                    study_partner_id=rshu_partner.id,
                    type_of_learning_id=type_of_learning.id
                ).one_or_none()

                if course is None:
                    uid = str(uuid.uuid4()).replace('-', '')
                    course = Course(
                        uid=uid,
                        name=name,
                        summary='',
                        title='',
                        definition='',
                        referral_link='',
                        type_of_learning_id=type_of_learning.id,
                        rating=0,
                        is_active=True,
                        study_partner_id=rshu_partner.id,
                        updated_at=datetime.now(),
                        duration_of_training=str(training_time),
                        description=str(description),
                        # self.sheet_2[f'E{self.counter_rshu}'] = str(course_program)
                        # self.sheet_2[f'F{self.counter_rshu}'] = str(teachers)
                        last_price=(int(price.replace(' ', '')) if price is not None else None))
                        # self.sheet_2[f'H{self.counter_rshu}'] = str(currency)
                        # self.sheet_2[f'I{self.counter_rshu}'] = str(item['category'])
                    self.session.add(course)

                    course_price = CoursePrice(
                        course_id=uid,
                        price=(int(price.replace(' ', '')) if price is not None else None),
                        date=datetime.now()
                    )
                    self.session.add(course_price)
                    self.session.commit()
                    print('rshu added')
                else:
                    course.updated_at = datetime.now()
                    course.last_price = (int(price.replace(' ', '')) if price is not None else None)
                    course_price = CoursePrice(
                        course_id=course.uid,
                        price=(int(price.replace(' ', '')) if price is not None else None),
                        date=datetime.now()
                    )
                    self.session.add(course_price)
                    self.session.commit()
                    print('rshu updated')
            except Exception as e:
                    print('error', traceback.format_exc())
