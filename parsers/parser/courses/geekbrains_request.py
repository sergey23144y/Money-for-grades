from ..functions import *


URL_ALL_COURSE = 'https://gb.ru/courses/all'


def geekbrains_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='GeekBrains').first()

    soup = get_soup(get_html(URL_ALL_COURSE))
    if soup:

        # all courses, may be None
        for item in soup.findAll('a', class_='product_card_link w-inline-block'):
            url = item.get('href')

            # get course, may be None
            soup_item = get_soup(get_html(url))

            if soup_item:
                for course in soup_item.findAll('div', class_='gkb-package-card'):

                    name = course.find('div', class_='gkb-package-card__header-title')
                    if name:
                        name = name.text.encode('l1').decode()

                    last_price = course.find('div', class_="gkb-package-card__header-new ui-text-body--1 ui-text--bold")
                    if last_price:
                        last_price = get_price(last_price.text.encode('l1').decode())

                    save_course(
                        session,
                        name=check_data(name, ''),
                        last_price=check_data(last_price),
                        partner_id=partner.id
                    )

