from datetime import datetime
from parser.parse_ import parse_all_courses
from scrapy_parsers.parser_database import load_session, Course


if __name__ == '__main__':

    start_parse = datetime.now()

    parse_all_courses()

    session = load_session()
    session.query(Course).filter(Course.updated_at < start_parse).update({Course.is_active: False})
    session.query(Course).filter(Course.updated_at >= start_parse).update({Course.is_active: True})
    session.commit()

    print(f'Time work {datetime.now() - start_parse}')





