from ..functions import *


URL_MAIN = 'https://innopolis.university'
URL_COURSES = 'https://innopolis.university/dpo-courses/'


def innopolis_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Innopolis').first()

    soup = get_soup(get_html(URL_COURSES))
    if soup:
        items = soup.findAll('a', class_='course-cards__person', target='_blank')
        for item in items:

            # url course
            url = item.get('href')

            # duration course
            duration = ''
            soup_item = get_soup(get_html(url))
            if soup_item and soup_item.text.__contains__('Длительность:'):
                for div in soup_item.findAll('div', class_='tn-atom'):
                    if div.find('div') is None and div.text.__contains__('месяца'):
                        duration = check_tag(div, '')
                        break

            # course price
            try:
                price_item = item.find('div', class_='course__price-and-place')
                price = get_price(check_tag(price_item.findAll('p')[1]))
            except (AttributeError, IndexError):
                price = None

            # save course
            save_course(
                session,
                name=check_tag(item.find('h3'), ''),
                # referral_link=url,
                duration_of_training=duration,
                description=check_tag(item.find('p'), ''),
                last_price=price,
                partner_id=partner.id,
            )

