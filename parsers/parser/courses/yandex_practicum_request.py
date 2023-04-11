from ..functions import *


URL_API_COURSES = 'https://practicum.yandex.ru/api/v2/professions/?tags=true'


def yandex_practicum_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Яндекс Практикум').first()

    data = get_data_api(URL_API_COURSES)
    if data:
        for i in data:
            save_course(
                session,
                name=check_data(i['name'], ''),
                duration_of_training=check_data(i['duration'], ''),
                description=check_data(i['description'], ''),
                last_price=check_data(i['price'], None),
                partner_id=partner.id,
            )
