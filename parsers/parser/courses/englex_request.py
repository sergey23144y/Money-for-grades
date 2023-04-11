from ..functions import *


URL_COURSES = 'https://englex.ru/courses/'


def englex_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Инглекс').first()

    soup = get_soup(get_html(URL_COURSES))
    if soup:
        items = soup.findAll('a', class_='card course-card')
        for item in items:
            url = item.get('href')

            # get course, may be None
            soup_item = get_soup(get_html(url))
            if soup_item:

                # save course
                save_course(
                    session,
                    name=check_tag(soup_item.find('h1', class_='title'), ''),
                    # referral_link=url,
                    duration_of_training=check_tag(soup_item.find('div', class_='characteristic-description'), ''),
                    description=check_tag(soup_item.find('p', class_='section-title-comment'), ''),
                    last_price=get_price(check_tag(soup_item.find('span', class_='attention'))),
                    partner_id=partner.id
                )
