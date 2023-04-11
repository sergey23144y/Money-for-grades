from ..functions import *


URL_MAIN = 'https://irs.academy'


def irs_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='irs.academy').first()

    soup = get_soup(get_html(URL_MAIN))
    if soup:
        try:
            categories = soup.find('div', class_='container coursesShop__sortBox menu-svg').findAll('a')
        except AttributeError:
            categories = None

        if categories:
            for category in categories:

                # link on category
                url_category = get_correct_url(URL_MAIN, category.get('href'))

                # get all course in category, may be None
                soup_category = get_soup(get_html(url_category))
                if soup_category:

                    # all category
                    courses = soup_category.findAll('div', class_='mainDirections__item')

                    for item in courses:

                        # price course
                        coast_box = item.find('div', class_='coastBox')
                        price = get_price(check_tag(coast_box.find('p'))) if coast_box else None

                        save_course(
                            session,
                            name=check_tag(item.find('h3'), ''),
                            # referral_link=get_correct_url(URL_MAIN, item.find('a').get('href')),
                            duration_of_training=check_tag(item.find('div', class_='duration'), ''),
                            description=check_tag(item.find('p', class_='descr'), ''),
                            last_price=price,
                            partner_id=partner.id
                        )
