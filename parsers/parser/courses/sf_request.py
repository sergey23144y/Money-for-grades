from ..functions import *


URL_MAIN = 'https://sf.education'


def sf_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='SF Education').first()
    soup = get_soup(get_html(URL_MAIN))

    if soup:
        faculties = []

        for i in soup.findAll('a', style='color: inherit'):
            if i.text.__contains__('ФАКУЛЬТЕТ') and faculties.__contains__(i.get('href').lower()) is False:
                faculties.append(i.get('href').lower())

        for faculty in faculties:
            url = get_correct_url(URL_MAIN, faculty)
            soup_faculty = get_soup(get_html(url))

            if soup_faculty:
                te = [i.text for i in soup_faculty.findAll('a')]
                f = te[9:]
                for item in soup_faculty.findAll('a'):
                    pass

