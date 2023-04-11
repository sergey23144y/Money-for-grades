from ..functions import *


URL_MAIN = 'https://contented.ru'


def contented_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Contented').first()

    soup = get_soup(get_html(URL_MAIN))
    if soup:

        # get all tag <a>, may be None
        items = soup.findAll('a', style="color:#ffffff;font-size:16px;font-weight:400;font-family:'CofoSans';")
        for item in items:

            temp_url = item.get('href')
            if temp_url and temp_url.__contains__('/edu/'):

                # name course
                name = check_tag(item, '')

                # url course
                url = get_correct_url(URL_MAIN, temp_url)
                soup_item = get_soup(get_html(url))
                if soup_item:

                    # duration course
                    duration = ''
                    for div in soup_item.findAll('div', class_='tn-atom'):
                        if div.text.__contains__('длительность:'):
                            duration = div.text.replace('длительность:', '').strip()
                            break

                    # save course
                    save_course(
                        session,
                        name=name,
                        # referral_link=url,
                        duration_of_training=duration,
                        partner_id=partner.id
                    )
                else:
                    # save course
                    save_course(
                        session,
                        name=name,
                        # referral_link=url,
                        partner_id=partner.id
                    )
