from ..functions import *


URL_API_COURSES = 'https://learn.school-xyz.com/api/public/v1/courses/'


def school_xyz_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='XYZ').first()

    # data about all courses, may be None
    data = get_data_api(URL_API_COURSES)
    if data:
        for item in data:

            # name course
            name = check_data(item['title'], '')

            # link on course
            url = check_data(item['infoUrl'], '')

            # duration course
            duration = ''
            soup_item = get_soup(get_html(url))
            if soup_item:
                lis = soup_item.findAll('li')
                for li in lis:
                    if li.text.__contains__('продолжительность:'):
                        duration = li.text.replace('продолжительность:', '').strip()
                        break

            # prise course
            price = check_data(item['regions']['ru']['price'], None)

            # save course
            save_course(
                session,
                name=name,
                # referral_link=url,
                duration_of_training=duration,
                last_price=price,
                partner_id=partner.id
            )
