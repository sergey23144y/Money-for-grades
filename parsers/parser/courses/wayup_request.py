from ..functions import *


URL_MAIN = 'https://wayup.in'
URL_LIBRARY = 'https://wayup.in/library'


def wayup_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='WayUp').first()

    soup = get_soup(get_html(URL_LIBRARY))
    if soup:
        block_category = soup.find('div', class_='courses__block')
        if block_category:
            items = block_category.findAll('a', class_='courses__item')
            if items:
                for item in items:
                    url = get_correct_url(URL_MAIN, item.get('href'))

                    item_soup = get_soup(get_html(url))
                    if item_soup:

                        # duration course
                        try:
                            duration = item_soup.find('div', class_='info-block').findAll('h3')[1].text
                        except (AttributeError, KeyError):
                            duration = ''

                        # description course
                        try:
                            description = item_soup.find(
                                'div',
                                class_='description-block').find('p').text.replace('\n', '').strip()
                        except (AttributeError, KeyError):
                            description = ''

                        # price course
                        price = item_soup.find('span', class_='converted-price')
                        if price:
                            price = int(price.text.replace('\n', '').strip()[1:-1])
                        else:
                            price = None

                        save_course(
                            session,
                            name=check_tag(item.find('h4'), ''),
                            # referral_link=url,
                            duration_of_training=duration,
                            description=description,
                            last_price=price,
                            partner_id=partner.id,
                        )
