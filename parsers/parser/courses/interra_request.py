from ..functions import *


URL_MAIN = 'https://www.interra.bz'
URL_COURSE = 'https://www.interra.bz/courses'


def interra_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Interra').first()

    soup = get_soup(get_html(URL_COURSE))
    if soup:
        items = []

        for div in soup.findAll('div', class_='t396__elem'):
            url = div.findAll('a')
            if url and len(url) == 1:
                url = url[0].get('href')
                if url.__contains__('edu') and items.__contains__(url) is False:
                    items.append(url)

        for item in items:
            soup_item = get_soup(get_html(item))
            if soup_item:
                start_point = soup_item.findAll('div', class_='tn-atom')

                # name course
                name = check_tag(start_point[1])

                # description course
                description = check_tag(start_point[2])

                # save course
                if name and description:
                    save_course(
                        session,
                        name=name,
                        description=description,
                        partner_id=partner.id
                    )
