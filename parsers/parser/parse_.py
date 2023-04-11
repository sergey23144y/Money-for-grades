from parser.courses.yandex_practicum_request import yandex_practicum_parse
# from .courses.sf_request import sf_parse
from parser.courses.netology_request import netology_parse
from parser.courses.skillbox_request import skillbox_parse
from parser.courses.wayup_request import wayup_parse
from parser.courses.convertmonster_request import convertmonster_parse
from parser.courses.skillfactory_request import skillfactory_parse
from parser.courses.teachline_request import teachline_parse
from parser.courses.interra_request import interra_parse
from parser.courses.irs_request import irs_parse
from parser.courses.contented_request import contented_parse
from parser.courses.school_xyz_request import school_xyz_parse
from parser.courses.geekbrains_request import geekbrains_parse
from parser.courses.englex_request import englex_parse
from parser.courses.otus_request import otus_parse
from parser.courses.skyeng_request import skyeng_parse
from parser.courses.escc_request import escc_parse
from parser.courses.lingualeo_request import lingualeo_parse
from parser.courses.skysmart_request import skysmart_parse
from parser.courses.innopolis_request import innopolis_parse
from parser.courses.mmamos_request import mmamos_parse


def parse_all_courses():
    functions_parsers = [
        yandex_practicum_parse,
        # sf_parse,
        netology_parse,
        skillbox_parse,
        wayup_parse,
        convertmonster_parse,
        skillfactory_parse,
        teachline_parse,
        interra_parse,
        irs_parse,
        contented_parse,
        school_xyz_parse,
        geekbrains_parse,
        englex_parse,
        otus_parse,
        skyeng_parse,
        escc_parse,
        lingualeo_parse,
        skysmart_parse,
        innopolis_parse,
        mmamos_parse,
    ]

    for func in functions_parsers:
        try:
            print(func.__name__)
            func()
        except Exception as ex:
            print(ex)
