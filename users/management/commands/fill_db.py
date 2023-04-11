import json
from random import randint, choice, choices

import environ
from django.core.management.base import BaseCommand

from ads.models import Advertisement
from courses.models import Book, CourseCategory, Software, StudyProgram, PersonalityType
from skills.models import Skill, SkillCategory
from specialties.models import Specialty
from teachers.models import Teacher
from users.models import User
from faker import Faker
from study_partners.models import StudyPartner
from vacancies.models import VacancyCategory, Vacancy, WorkSchedule, VacancyRequirement
from vacancy_partners.models import VacancyPartner
from promotions.models import Promotion
from promotions.models import PromotionCitiesCategories

fake = Faker()

env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('django_back_api/jsons/fake_numbers.json', 'r', encoding='utf-8') as db_data:
            data = json.loads(db_data.read())

        random_images = []
        # bytes_images = []
        # for i in range(data["image_number"]):
        #     bytes_images.append(grequests.get('https://picsum.photos/200/300'))
        # bytes_images = grequests.map(bytes_images)
        # bytes_images = list(map(lambda a: a.content, bytes_images))
        for i in range(data['image_number']):
            random_images.append(f'image_{i}.png')
            # with open(BASE_DIR / 'media' / f'image_{i}.png', 'wb') as j:
            #     j.write(bytes_images[i])
        # group = Group.objects.all()
        #
        # authemail = User.objects.all()
        # authemail.delete()
        # for i in range(data['users_number']):
        #     user = User.objects.create(
        #         username=fake.name(),
        #         first_name=fake.first_name(),
        #         last_name=fake.last_name(),
        #         email=fake.email(),
        #         avatar=choice(random_images)
        #     )
        #
        #     user.save()
        #     user.groups.add(choice(group))
        users = User.objects.all()
        users.delete()

        User.objects.create_superuser(
            email=env('SUPERUSER_EMAIL'),
            password=env('SUPERUSER_PASSWORD')
        )
        vac_par = VacancyPartner.objects.all()
        vac_par.delete()
        for i in range(data['vac_par_number']):
            vac_par = VacancyPartner.objects.create(
                name=fake.sentence(nb_words=3, variable_nb_words=True),
                title=fake.sentence(nb_words=3, variable_nb_words=True),
                description=fake.text(max_nb_chars=50),
                definition=fake.text(max_nb_chars=50),
                found_year=fake.random_int(min=1901, max=2021),
                vac_quantity=fake.random_int(min=1, max=10),
                image=choice(random_images)
            )
            vac_par.save()

        # for i in range(data['study_par_number']):
        #     study_par = StudyPartner.objects.create(
        #         name=fake.sentence(nb_words=3, variable_nb_words=True),
        #         title=fake.sentence(nb_words=3, variable_nb_words=True),
        #         definition=fake.text(max_nb_chars=50),
        #         description=fake.text(max_nb_chars=50),
        #         found_year=fake.random_int(min=1901, max=2021),
        #         course_quantity=fake.random_int(min=1, max=10),
        #         rating=fake.random_int(min=1, max=5),
        #         image=choice(random_images),
        #         certificate=choice(random_images)
        #     )
        #     study_par.save()

        study_par = StudyPartner.objects.all()
        vac_par = VacancyPartner.objects.all()
        promo = Promotion.objects.all()
        promo_categories = PromotionCitiesCategories.objects.all()
        promo.delete()
        for i in range(data['promo_number']):
            r_num = randint(0, 1)
            promo = Promotion.objects.create(
                name=fake.sentence(nb_words=5, variable_nb_words=True),
                title=fake.sentence(nb_words=5, variable_nb_words=True),
                description=fake.text(max_nb_chars=50),
                definition=fake.text(max_nb_chars=50),
                coupon=fake.text(max_nb_chars=10),
                link=fake.url(),
                vacancy_partner=(choice(vac_par) if r_num == 0 else None),
                study_partner=(choice(study_par) if r_num == 1 else None),
                image=choice(random_images)
            )
            promo.save()
            promo.cities.set(choices(promo_categories, k=15))

        specialties = Specialty.objects.all()
        specialties.delete()
        for i in range(data['specialties_number']):
            specialties = Specialty.objects.create(
                name=fake.sentence(nb_words=3, variable_nb_words=True),
            )
            specialties.save()

        teachers = Teacher.objects.all()
        teachers.delete()
        for i in range(data['teachers_number']):
            teachers = Teacher.objects.create(
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                title=fake.sentence(nb_words=5, variable_nb_words=True),
                definition=fake.text(max_nb_chars=50),
                description=fake.text(max_nb_chars=50),
                position=fake.text(max_nb_chars=30),
                experience=fake.text(max_nb_chars=30),
                rating=fake.random_int(min=1, max=5),
                company_one=fake.text(max_nb_chars=10),
                company_two=fake.text(max_nb_chars=10),
                company_three=fake.text(max_nb_chars=10),
                image=choice(random_images)

            )
            teachers.save()

        ads = Advertisement.objects.all()
        ads.delete()
        for i in range(data['ads_number']):
            ads = Advertisement.objects.create(name=fake.text(max_nb_chars=50), url=fake.url())
            ads.save()

        books = Book.objects.all()
        books.delete()
        for i in range(data['books_number']):
            books = Book.objects.create(name=fake.text(max_nb_chars=10))
            books.save()

        course_categories = CourseCategory.objects.all()
        course_categories.delete()
        for i in range(data['course_categories_number']):
            course_categories = CourseCategory.objects.create(
                name=fake.text(max_nb_chars=10),
                title=fake.text(max_nb_chars=10),
                definition=fake.text(max_nb_chars=30),
                description=fake.text(max_nb_chars=30),
                image=choice(random_images)
            )

        study_programs = StudyProgram.objects.all()
        study_programs.delete()
        for i in range(data['study_program_number']):
            study_programs = StudyProgram.objects.create(name=fake.text(max_nb_chars=10))
            study_programs.save()

        personality_types = PersonalityType.objects.all()
        personality_types.delete()
        for i in range(data['personality_type_number']):
            personality_types = PersonalityType.objects.create(name=fake.text(max_nb_chars=10))
            personality_types.save()

        software = Software.objects.all()
        software.delete()
        for i in range(data['software_number']):
            software = Software.objects.create(name=fake.text(max_nb_chars=10))
            software.save()
        #
        # courses = Course.objects.all()
        # courses.delete()
        # pay_types = PayType.objects.all()
        # teachers = Teacher.objects.all()
        # types_of_learning = TypeOfLearning.objects.all()
        # books = Book.objects.all()
        # payments = Payment.objects.all()
        # software = Software.objects.all()
        # personality_types = PersonalityType.objects.all()
        # study_programs = StudyProgram.objects.all()
        # for i in range(data['courses_number']):
        #     course = Course.objects.create(
        #         name=fake.text(max_nb_chars=10),
        #         summary=fake.text(max_nb_chars=20),
        #         title=fake.sentence(nb_words=5, variable_nb_words=True),
        #         definition=fake.text(max_nb_chars=50),
        #         description=fake.text(max_nb_chars=30),
        #         last_price=fake.random_int(min=1000, max=100000),
        #         pay_type=choice(pay_types),
        #         study_partner=choice(study_par),
        #         rating=fake.random_int(min=1, max=5),
        #         type_of_learning=choice(types_of_learning),
        #         personality_type=choice(personality_types),
        #         study_program=choice(study_programs),
        #         duration_of_training=fake.text(max_nb_chars=10),
        #         payment=choice(payments),
        #         referral_link=fake.url(),
        #         image=choice(random_images),
        #         certificate=choice(random_images),
        #         image_mini=choice(random_images),
        #         image_mobile=choice(random_images),
        #
        #     )
        #     course.save()
        #     course.teachers.set(choices(teachers))
        #     course.books.set(choices(books))
        #     course.software.set(choices(software))
        #
        # course_prices = CoursePrice.objects.all()
        # course_prices.delete()
        # course_price = CoursePrice.objects.create(
        #     price=fake.random_int(min=1000, max=100000),
        #     course=course)
        # course_price.save()

            # course_comments = CourseComment.objects.all()
        # course_comments.delete()
        # authemail = User.objects.all()
        # specialties = Specialty.objects.all()
        # courses = Course.objects.all()
        # for course in courses:
        #     course_comment = CourseComment.objects.create(
        #         user=choice(authemail),
        #         comment=fake.text(max_nb_chars=20),
        #         specialty=choice(specialties),
        #         course=course
        #     )
        #     course_comment.save()

        vacancy_categories = VacancyCategory.objects.all()
        vacancy_categories.delete()
        for i in range(data['vacancy_categories_number']):
            vacancy_category = VacancyCategory.objects.create(
                name=fake.text(max_nb_chars=10),
                title=fake.text(max_nb_chars=10),
                definition=fake.text(max_nb_chars=30),
                description=fake.text(max_nb_chars=30),
                image=choice(random_images)
            )
            vacancy_category.save()

        vacancies = Vacancy.objects.all()
        vacancies.delete()
        personality_types = PersonalityType.objects.all()
        vacancy_partners = VacancyPartner.objects.all()
        work_sched = WorkSchedule.objects.all()
        vacancy_categories = VacancyCategory.objects.all()
        for i in range(data['vacancy_number']):
            vacancy = Vacancy.objects.create(
                name=fake.text(max_nb_chars=10),
                summary=fake.text(max_nb_chars=20),
                description=fake.text(max_nb_chars=30),
                title=fake.text(max_nb_chars=10),
                definition=fake.text(max_nb_chars=30),
                payment=fake.text(max_nb_chars=10),
                internship=fake.text(max_nb_chars=20),
                vacancy_partner=choice(vacancy_partners),
                vacancy_category=choice(vacancy_categories),
                work_schedule=choice(work_sched),
                image=choice(random_images),
                image_mini=choice(random_images),
                image_mobile=choice(random_images),
                link=fake.url(),
                personality_type=choice(personality_types)
            )
            vacancy.save()
            # vacancy.courses.set(choices(courses))

        skills = Skill.objects.all()
        skills.delete()
        skill_cat = SkillCategory.objects.all()
        for i in range(data['skill_number']):
            skill = Skill.objects.create(
                name=fake.text(max_nb_chars=10),
                skill_category=choice(skill_cat),
                is_active=True,
                order=i
            )
            skill.save()

        vac_reqs = VacancyRequirement.objects.all()
        vac_reqs.delete()
        vacancies = Vacancy.objects.all()
        skills = Skill.objects.all()
        for j in vacancies:
            for i in skills:
                vac_req = VacancyRequirement.objects.create(
                    vacancy=j,
                    skill=i,
                    level=fake.random_int(min=0, max=10)
                )
                vac_req.save()
