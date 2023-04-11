from ..functions import *

import re

URL_COURSES = 'https://skillfactory.ru/courses'


def skillfactory_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='SkillFactory').first()
    soup = get_soup(get_html(URL_COURSES))
    if soup:
        all_links = soup.findAll('a', class_='tn-atom', target='_blank')
        if all_links:
            # get all courses
            items = []
            for link in all_links:
                url = link.get('href')
                if url.__contains__('https://skillfactory.ru/'):
                    items.append(url)

            for item in items:

                start_point = soup.find('a', class_='', href=item)
                # name course
                name = re.sub('[«-»]', '', check_tag(start_point, ''))

                # description course
                # description = check_tag(start_point.findNext('div'), '')

                if start_point:
                    next_point = start_point.findNext('strong', style='color: rgb(53, 179, 74);')

                    # duration course
                    duration = check_tag(next_point, '')

                    # price course
                    if next_point:
                        price = get_price(check_tag(next_point.findNext('div')))
                    else:
                        price = None

                    # save course
                    save_course(
                        session,
                        name=name,
                        # referral_link=item,
                        duration_of_training=duration,
                        # description=description,
                        last_price=price,
                        partner_id=partner.id
                    )
