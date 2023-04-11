from ..functions import *


URL_MAIN = 'https://www.escc.ru'
URL_PRICE = 'https://www.escc.ru/price-list'


def escc_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='ЕШКО').first()

    soup = get_soup(get_html(URL_PRICE))
    if soup:
        items = soup.findAll('tr', class_='price-list__item-row')
        for item in items:
            # price course
            old_price = check_tag(item.find('td', class_='price-list__pk-special united-table').find('s'), '')
            if old_price:
                str_price = check_tag(item.find('td', class_='price-list__pk-special united-table'), '')
                price = get_price(str_price.replace(old_price, ''))
            else:
                price = None
            # save course
            save_course(
                session,
                name=check_tag(item.find('a'), ''),
                # referral_link=get_correct_url(URL_MAIN, item.find('a').get('href')),
                duration_of_training=check_tag(item.find('td', class_='price-list__months-col'), '', concatenation_string=' мес.'),
                last_price=price,
                partner_id=partner.id
            )
