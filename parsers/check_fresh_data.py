from datetime import date

from scrapy_parsers.parser_database import load_session, Course


session = load_session()
archive_course = session.query(Course).filter(Course.updated_at != date.today()).update({Course.is_active: False})
get_from_archive_course = session.query(Course).filter_by(updated_at=date.today(), is_active=False).update({Course.is_active:True})
session.commit()
