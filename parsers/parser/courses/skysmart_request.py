from ..functions import *

URL_MAIN = 'https://skysmart.ru'
URL_COURSES = 'https://skysmart.ru/courses'


def skysmart_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Skysmart').first()

    soup = get_soup(get_html(URL_COURSES))
    if soup:
        classes = soup.findAll('div', class_='courses-filter-settings-content')
        if classes:
            for class_ in classes[0].findAll('a')[1:]:
                url_class = get_correct_url(URL_MAIN, class_.get('href'))
                soup_class_ = get_soup(get_html(url_class))
                if soup_class_:
                    targets = soup_class_.findAll('div', class_='courses-filter-settings-content')
                    if targets:
                        for target in targets[1].findAll('a', class_='courses-filter-settings-item ng-star-inserted')[1:]:
                            part_url = target.get('href')
                            if part_url != '/courses':
                                url_target = get_correct_url(URL_MAIN, part_url)
                                soup_target = get_soup(get_html(url_target))
                                if soup_target:
                                    for item in soup_target.findAll('div', class_='courses-list-item ng-star-inserted'):
                                        save_course(
                                            session,
                                            name=check_tag(item.find('div', class_='courses-card-name'), ''),
                                            # referral_link=get_correct_url(
                                            #     URL_MAIN, item.find('a', class_='courses-card-link').get('href')),
                                            duration_of_training=check_tag(item.find('span', class_='courses-card-quantity'),''),
                                            description=check_tag(item.find('div', class_='courses-card-content'), ''),
                                            partner_id=partner.id,
                                        )
