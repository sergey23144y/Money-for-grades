from ..functions import *


URL_API_PROFESSION = 'https://skillbox.ru/api/v6/ru/sales/skillbox/directions/all/nomenclature/profession/?'
URL_API_COURSE = 'https://skillbox.ru/api/v6/ru/sales/skillbox/directions/all/nomenclature/course/?'
URL_API_PRICE = 'https://api.retailrocket.ru/api/1.0/partner/6048a0d097a52514f050731f/items/?itemsIds=&stock=&format=json'


def skillbox_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Skillbox').first()

    for url in [URL_API_PROFESSION, URL_API_COURSE]:
        count_page = get_data_api(url)
        if count_page:
            count_page = count_page['meta']['last_page']
            for i in range(count_page):
                items = get_data_api(f'{url}page={i + 1}')['data']
                for item in items:

                    # landing_id = item['id']
                    # data_course = get_data_api(URL_API_PRICE.replace('itemsIds=', f'itemsIds={landing_id}'))[0]

                    save_course(
                        session,
                        name=check_data(item['title'], ''),
                        # title=check_data(data_course['Name'], ''),
                        # referral_link=check_data(item['href'], ''),
                        duration_of_training=check_data(f"{item['duration']['count']} {item['duration']['label']}", ''),
                        # last_price=check_data(data_course['Price']),
                        partner_id=partner.id
                    )
