from ..functions import *


URL_PROGRAMS = 'https://skyeng.ru/programs/'


def skyeng_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Skyeng').first()

    soup = get_soup(get_html(URL_PROGRAMS))
    if soup:
        items = soup.findAll('catalog-courses-showcase-card')
        for item in items:
            url = item.find('a').get('href')
            soup_item = get_soup(get_html(url))
            if soup_item:
                # save course
                save_course(
                    session,
                    name=check_tag(soup_item.find('h1'), ''),
                    # referral_link=url,
                    description=check_tag(soup_item.find('div', class_='-size-xl catalog-intro-text'), ''),
                    partner_id=partner.id
                )
