import random
from my_user.models import UserStudyWordModel, UserStudySessionModel
from lesson.models import CourseModel, UnitModel, WordModel


class UserStudyManager:
    @staticmethod
    def plan(user, unit):

        # TODO use the user studied words instead
        all_units = UnitModel.objects.filter(course=unit.course, order__lte=unit.order)
        words_in_unit = WordModel.objects.filter(unit__in=all_units)

        user_studied_words = UserStudyWordModel.objects.filter(
            user=user, word__in=words_in_unit
        )

        correct_word = UserStudyManager.get_card(user, unit)
        if correct_word is None:
            correct_word = UserStudyManager.get_intro(user, unit)
            print("plan intro")
        else:
            print("plan card")

        # studied_words = [word.word for word in user_studied_words]
        studied_words.append(correct_word)
        word_count_limit = 3
        if len(studied_words) >= word_count_limit:
            words = studied_words[:word_count_limit]
        else:
            words = list(WordModel.objects.filter(unit=unit)[:word_count_limit])

        words.append(correct_word)
        random.shuffle(words)

        # TODO do next step
        return words, correct_word

    @staticmethod
    def get_intro(user, unit):
        all_units = UnitModel.objects.filter(course=unit.course, order__lte=unit.order)
        words_in_unit = WordModel.objects.filter(unit__in=all_units)
        # only 3 intros are allowed
        user_studied_words = UserStudyWordModel.objects.filter(
            user=user, word__in=words_in_unit
        )
        studied_words = [word.word for word in user_studied_words]
        user_session = UserStudySessionModel.objects.get_or_create(user=user)

        intro_words = user_studied_words.filter(study_type=UserStudyWordModel.INTRO)
        if intro_words.count() > UserStudyWordModel.MAX_INTRO:
            return None
        else:
            correct_word = (
                WordModel.objects.filter(unit=unit)
                .exclude(pk__in=[w.pk for w in studied_words])
                .order_by("-created_at")
                .first()
            )
            if correct_word:
                return correct_word
            else:
                return None

    def get_card(user, unit):
        all_units = UnitModel.objects.filter(course=unit.course, order__lte=unit.order)
        words_in_unit = WordModel.objects.filter(unit__in=all_units)
        # only 3 intros are allowed
        user_studied_words = UserStudyWordModel.objects.filter(
            user=user, word__in=words_in_unit
        )
        studied_words = [word.word for word in user_studied_words]
        cards = user_studied_words.filter(study_type=UserStudyWordModel.CARD)
        if cards.count() > UserStudyWordModel.MAX_CARD:
            return cards.first().word
        else:
            correct_word = (
                user_studied_words.filter(study_type=UserStudyWordModel.INTRO)
                .order_by("?")
                .first()
            )
            if correct_word:
                return correct_word.word
            else:
                return None

    @staticmethod
    def get_listening(user, unit):
        return UserStudyManager.get(user, unit, study_type=UserStudyWordModel.LISTENING)

    @staticmethod
    def get_writing(user, unit):
        return UserStudyManager.get(user, unit, study_type=UserStudyWordModel.WRITING)

    @staticmethod
    def get(user, unit, study_type):
        all_units = UnitModel.objects.filter(course=unit.course, order__lte=unit.order)
        words_in_unit = WordModel.objects.filter(unit__in=all_units)
        # only 3 intros are allowed
        user_studied_words = UserStudyWordModel.objects.filter(
            user=user, word__in=words_in_unit
        ).order_by("?")
        studied_words = [word.word for word in user_studied_words]

        intro_cards = user_studied_words.filter(study_type=study_type)
        # TODO change for other cards
        if intro_cards.count() > 3:
            return None
        else:

            # TODO return an intro card
            return None
