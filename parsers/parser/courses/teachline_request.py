from ..functions import *


URL_MAIN = 'https://teachline.ru'
URL_COURSES = 'https://teachline.ru/courses'
URL_PAGINATION = 'https://teachline.ru/courses/?PAGEN_1='


def teachline_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Teachline').first()

    soup = get_soup(get_html(URL_COURSES))
    if soup:
        # get quantity page on site
        try:
            page_count = len(soup.find('div', class_='page-navigation').findAll('a'))
        except AttributeError:
            page_count = 1

        for i in range(page_count):

            # get all course on one page
            soup_page = get_soup(get_html(URL_PAGINATION + str(i + 1)))
            if soup_page:
                items = soup_page.findAll('a', class_='courseholder__item')
                for item in items:

                    # url course
                    url = get_correct_url(URL_MAIN, item.get('href'))

                    # name course
                    name = check_tag(item.find('p', class_='courseholder__title'), '')

                    # duration course
                    duration = ''
                    for use in item.findAll('use'):
                        if use.get('xlink:href').__contains__('#course-clock'):
                            duration = check_tag(use.find_next('span'), '')
                            break

                    # get information course, may be None
                    soup_item = get_soup(get_html(url))
                    if soup_item:
                        page_main_header = soup_item.find('div', class_='page__mainheader')

                        # description course
                        description = check_tag(page_main_header.find('span', class_='small'), '')

                        # price course if you find block
                        block_price = soup_item.findAll('div', class_='tarifs__slider__slide')
                        if block_price:
                            for tariff in block_price:

                                # u# name course
                                part_name_tag = tariff.find('p', class_='tarifs__slider__slide__title')
                                new_name = f'{name} ({check_tag(part_name_tag, "")})'

                                # price course
                                price_tag = tariff.find('span', class_='tarifs__slider__slide__price__cost')
                                price = get_price(check_tag(price_tag))

                                # save course
                                save_course(
                                    session,
                                    name=new_name,
                                    # referral_link=url,
                                    duration_of_training=duration,
                                    description=description,
                                    last_price=price,
                                    partner_id=partner.id
                                )
                            else:
                                # save course
                                save_course(
                                    session,
                                    name=name,
                                    # referral_link=url,
                                    duration_of_training=duration,
                                    description=description,
                                    partner_id=partner.id
                                )

                        else:
                            # save course
                            save_course(
                                session,
                                name=name,
                                # referral_link=url,
                                duration_of_training=duration,
                                partner_id=partner.id
                            )
