from ..functions import *

URL_API_CATEGORY = 'https://netology.ru/backend/api/json_storages/products_navigator'
URL_API_COURSE = 'https://netology.ru/backend/api/page_contents/programs%2F'
URL_API_PROGRAMS = 'https://netology.ru/backend/api/directions/category/programs'


def netology_parse():
    
    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Нетология').first()

    # get all categories
    for category in get_data_api(URL_API_CATEGORY)['data']:

        # get all data about course, may be None
        url_api_programs = URL_API_PROGRAMS.replace('/category', category['direction']['link'])
        data = get_data_api(url_api_programs)
        if data:
            for item in data:
                part_url = item['url'].split('/')[-1]

                data_item = get_data_api(URL_API_COURSE + part_url)
                if data_item:
                    # save course
                    save_course(
                        session,
                        name=check_data(item['name'], ''),
                        # title=check_data(data_item['meta']['title'], ''),
                        # referral_link=check_data(item['url'], ''),
                        duration_of_training=check_data(item['duration'], ''),
                        description=check_data(data_item['meta']['description'], ''),
                        last_price=check_data(item['current_price']),
                        partner_id=partner.id,
                    )
