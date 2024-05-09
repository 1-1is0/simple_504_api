from my_user.models import UserStudyWordModel, UserStudySessionModel
from lesson.models import CourseModel, UnitModel, WordModel


class UserStudyManager:
    @staticmethod
    def plan(user):
        user_studied_words = UserStudyWordModel
