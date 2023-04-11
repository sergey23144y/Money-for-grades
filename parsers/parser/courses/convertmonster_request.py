from ..functions import *


URL_MAIN = 'https://convertmonster.ru'
URL_EDU = 'https://convertmonster.ru/edu'


def convertmonster_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Convert Monster').first()

    soup = get_soup(get_html(URL_EDU))
    if soup:
        # get all courses
        items = []
        categories = soup.findAll('div', id=['events', 'online', 'premium', 'express'])

        for category in categories:
            courses = category.findAll('div', class_='courses_item grey_bg padding_sm_all clearfix')
            for course in courses:
                items.append(course)

        for item in items:

            # name course
            name = check_tag(item.find('h3', class_='info_head'), '')

            # description course
            description = check_tag(item.find('p', class_='info_description'), '')

            # url course
            part_url = item.find('a', class_='button_link inline md')
            if part_url:
                url = get_correct_url(URL_MAIN, part_url.get('href'))
                item_soup = get_soup(get_html(url))
                if item_soup:
                    price_block = item_soup.find('div', id='tariff')
                    if price_block:
                        for div in price_block.findAll('div', class_='tariff__item'):

                            # new name course
                            new_name = f"{name} ({check_tag(div.find('p', class_='default_p center'), '')})"

                            # price course
                            price = get_price(check_tag(div.find('span', class_='txt_sm medium'), ''))

                            # duration course
                            duration = ''
                            ul = div.find('ul')
                            if ul:
                                duration = check_tag(ul.find('span', class_='medium'), '')

                            # save course
                            save_course(
                                session,
                                name=new_name,
                                # referral_link=url,
                                duration_of_training=duration,
                                description=description,
                                last_price=price,
                                partner_id=partner.id
                            )
                    else:
                        save_course(
                            session,
                            name=name,
                            # referral_link=url,
                            description=description,
                            partner_id=partner.id
                        )
