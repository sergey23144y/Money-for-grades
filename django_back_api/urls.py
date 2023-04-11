"""django_back_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from authemail import urls as authemail_urls
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from ads.views import AdvertisementViewSet
from courses.views import CourseViewSet, CoursePriceViewSet, CourseSkillLevelWeightListAPIView, \
    PayTypeViewSet, TypeOfLearningViewSet, PaymentViewSet, BookViewSet, SoftwareViewSet, \
    StudyProgramViewSet, PersonalityTypeViewSet, TypeOfTrainingViewSet, CourseOriginViewSet, StatusViewSet, \
    CourseListAPIView, CourseBaseCategoryListAPIView, CourseCategoryListAPIView, \
    CourseByBaseCourseCategoryListAPIView, CourseCommitViewSet, CourseCommitRetrieve, CourseCommitUpdate, CourseCommitCreate
from expiring_token.obtain_token import ObtainAuthExpiringToken as token_obtain
from promotions.views import PromotionModelViewSet
from promotions.views import PromotionCityListAPIView
from reactions.views import ReactionsUsersAPIView, ReactionsEmployersAPIView
from skills.views import SkillViewSet
from specialties.views import SpecialtyViewSet, SpecialtyCategoriesViewSet
from study_partners.views import StudyPartnerViewSet
from teachers.views import TeacherViewSet
from users.views import UserSkillsListAPIView, UserRateHistoryListAPIView, PasswordResetVerify, SignupVerify, \
    UserTypeViewSet, SalesFunnelViewSet, SalesChannelViewSet, UserMe, UserViewSet, VKOAuth
from vacancies.views import VacancyCategoryViewSet, VacancyViewSet, VacancyRequirementListAPIView, TypeOfWorkViewSet, \
    WorkScheduleViewSet
from vacancy_partners.views import VacancyPartnerViewSet

from comments.views import CommentCourseAdminViewSet, CommentTeacherAdminViewSet, CommentStudyPartnerAdminViewSet, \
    CommentCourseEntityListApiView, CommentTeacherEntityListApiView, CommentStudyPartnerEntityListApiView, \
    CommentCourseUserViewSet, CommentTeacherUserViewSet, CommentStudyPartnerUserViewSet

from webmaster.views import FeedAPIView, YandexWebmasterApiView
from orders.views import OrderAPIView


router = DefaultRouter()

router.register('promotions_all', PromotionModelViewSet)
router.register('study_partners', StudyPartnerViewSet)
router.register('vacancy_partners', VacancyPartnerViewSet)
router.register('specialties', SpecialtyViewSet)
router.register('specialty_categories', SpecialtyCategoriesViewSet)
router.register('vacancy_categories', VacancyCategoryViewSet)
router.register('teachers', TeacherViewSet)
router.register('ads', AdvertisementViewSet)

#курсы:
router.register('courses', CourseViewSet)
router.register('course_prices', CoursePriceViewSet)
router.register('pay_types', PayTypeViewSet)
router.register('types_of_learning', TypeOfLearningViewSet)
router.register('payments', PaymentViewSet)
router.register('books', BookViewSet)
router.register('software', SoftwareViewSet)
router.register('study_programs', StudyProgramViewSet)
router.register('personality_types', PersonalityTypeViewSet)
router.register('types_of_training', TypeOfTrainingViewSet)
router.register('course_origins', CourseOriginViewSet)
router.register('statuses', StatusViewSet)

#вакансии:
router.register('vacancies', VacancyViewSet)
router.register('vacancy_categories', VacancyCategoryViewSet)
router.register('types_of_work', TypeOfWorkViewSet)
router.register('work_shedules', WorkScheduleViewSet)

# комментарии:
router.register('comments_admin_course', CommentCourseAdminViewSet)
router.register('comments_admin_teacher', CommentTeacherAdminViewSet)
router.register('comments_admin_studypartner', CommentStudyPartnerAdminViewSet)
router.register('comments_user_course', CommentCourseUserViewSet)
router.register('comments_user_teacher', CommentTeacherUserViewSet)
router.register('comments_user_studypartner', CommentStudyPartnerUserViewSet)

router.register('users_admin', UserViewSet)
router.register('user_types', UserTypeViewSet)
router.register('sales_funnel', SalesFunnelViewSet)
router.register('sales_channel', SalesChannelViewSet)

router.register('skills', SkillViewSet)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-token-auth/', obtain_auth_token),
    path('api/api-expiring-token/', token_obtain.as_view()),
    path('api/', include(router.urls)),

    path('api/promotions_cities/<int:pk>', PromotionCityListAPIView.as_view()),

    path('api/vacancy_requirements/<str:pk>', VacancyRequirementListAPIView.as_view()),

    path('api/course_by_base_category/<str:pk>', CourseByBaseCourseCategoryListAPIView.as_view()),
    path('api/course_categories/<str:pk>', CourseCategoryListAPIView.as_view()),
    path('api/course_base_categories/<str:pk>', CourseBaseCategoryListAPIView.as_view()),
    path('api/course_skill_level_weight/<str:pk>', CourseSkillLevelWeightListAPIView.as_view()),
    path('api/course_public/<str:pk>', CourseListAPIView.as_view()),

    path('api/vk-oauth2/login/', VKOAuth.as_view()),
    path('api/user_me', UserMe.as_view()),
    path('api/user_skills/<str:pk>', UserSkillsListAPIView.as_view()),
    path('api/user_rate_history/<str:pk>', UserRateHistoryListAPIView.as_view()),
    path('api/users/', include(authemail_urls)),
    path('api/password/reset/verify_/', PasswordResetVerify.as_view(), name='authemail-password-reset-verify_'),
    path('api/users/signup/verify_/', SignupVerify.as_view(), name='authemail-signup-verify'),

    path('api/comments/course/<str:pk>/', CommentCourseEntityListApiView.as_view(), name='comments-course'),
    path('api/comments/teacher/<str:pk>/', CommentTeacherEntityListApiView.as_view(), name='comments-teacher'),
    path('api/comments/study_partner/<str:pk>/', CommentStudyPartnerEntityListApiView.as_view(), name='comments-study-partner'),

    path('api/course_commits', CourseCommitViewSet.as_view()),
    path('api/course_commits/<int:pk>', CourseCommitRetrieve.as_view()),
    path('api/course_commits', CourseCommitCreate.as_view()),
    path('api/course_commits', CourseCommitUpdate.as_view()),

    # path('api/webmaster/<str:pk>/', YandexWebmasterApiView.as_view(), name='webmaster-yandex'),
    # path('api/webmaster/feed/<str:pk>/', FeedAPIView.as_view(), name='webmaster-yandex-feed'),

    path('api/orders/add/', OrderAPIView.as_view(), name='order-add'),
    path('api/reactions_user/add/', ReactionsUsersAPIView.as_view(), name='reaction-user-add'),
    path('api/reactions_employer/add/', ReactionsEmployersAPIView.as_view(), name='reaction-employer-add')
]


