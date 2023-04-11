from ..functions import *


URL_MAIN = 'https://otus.ru'


def otus_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='OTUS').first()

    soup = get_soup(get_html(URL_MAIN))
    if soup:
        categories = soup.find('div', id='categories_id')
        if categories:
            for category in categories.findAll('a', class_='nav__item course-categories__nav-item'):
                url_category = get_correct_url(URL_MAIN, category.get('href'))
                soup_category = get_soup(get_html(url_category))
                if soup_category:
                    lessons = soup_category.findAll('a')
                    if lessons:
                        for item in lessons:
                            part_url = item.get('href')
                            if item.get('href').split('/').__contains__('lessons'):
                                url = get_correct_url(URL_MAIN, part_url)
                                soup_item = get_soup(get_html(url))
                                if soup_item:
                                    price = None
                                    for i in soup_item.findAll('nobr'):
                                        if i.text.__contains__('₽'):
                                            price = get_price(i.text)
                                            break
                                    description = check_tag(soup_item.find('div', class_='course-about__content'), '')

                                    save_course(
                                        session,
                                        name=check_tag(soup_item.find('div', class_='course-header2__title'), ''),
                                        # referral_link=url,
                                        duration_of_training=check_tag(soup_item.find('p', class_='course-header2-bottom__item-text'), ''),
                                        description=description,
                                        last_price=price,
                                        partner_id=partner.id
                                    )
