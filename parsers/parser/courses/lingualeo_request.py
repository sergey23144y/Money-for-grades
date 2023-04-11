from ..functions import *


def lingualeo_parse():

    session = load_session()
    partner = session.query(StudyPartner).filter_by(name='Lingualeo').first()
