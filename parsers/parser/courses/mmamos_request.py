from ..functions import *


URL_MAIN = 'https://mmamos.ru/'
URL_DPO = 'https://mmamos.ru/dpo/'


def mmamos_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Mmamos').first()

    soup = get_soup(get_html(URL_DPO))
    if soup:
        categories = soup.findAll('div', class_='js-filter')
        for category in categories:
            items = category.findAll('a')
            for item in items:
                url = get_correct_url(URL_MAIN, item.get('href'))

                # description and price course
                description = ''
                price = None
                soup_item = get_soup(get_html(url))
                if soup_item:
                    description = soup_item.find('meta', property='og:description').get('content')
                    for b in soup_item.findAll('b'):
                        if b.text.__contains__('рублей'):
                            price = get_price(check_tag(b))
                            break

                # save course
                save_course(
                    session,
                    name=check_tag(item.find('h3'), ''),
                    # referral_link=url,
                    duration_of_training=check_tag(item.find('div', class_='uk-grid-small').find('div'), ''),
                    description=description,
                    last_price=price,
                    partner_id=partner.id,
                )
