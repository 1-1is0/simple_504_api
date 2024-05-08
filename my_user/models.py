from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class UserStudyWordModel(models.Model):
    INTRO = "intro"
    CARD = "card"
    LISTENING = "listening"
    WRITING = "writing"

    MAX_INTRO = 1
    MAX_CARD = 5
    MAX_LISTENING = 2
    MAX_WRITING = 2

    STUDY_TYPE_CHOICES = [
        (INTRO, _("intro")),
        (CARD, _("card")),
        (LISTENING, _("listening")),
        (WRITING, _("writing")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE
    )
    word = models.ForeignKey(
        "lesson.WordModel", verbose_name=_("word"), on_delete=models.CASCADE
    )
    study_type = models.CharField(
        _("study type"), max_length=64, choices=STUDY_TYPE_CHOICES, default=INTRO
    )
    progress_step = models.IntegerField(_("study type progress"), default=0)

    right_count = models.PositiveIntegerField(_("right count"), default=0)
    wrong_count = models.PositiveIntegerField(_("wrong count"), default=0)
    note = models.TextField(_("note"), blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    @property
    def total_count(self):
        return self.right_count + self.wrong_count

    class Meta:
        verbose_name = _("UserStudyWordModel")
        verbose_name_plural = _("UserStudyWordModels")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pk} user: {self.user} word: {self.word}"

    def get_absolute_url(self):
        return reverse("UserStudyWordModel_detail", kwargs={"pk": self.pk})

    def next_step(self):
        if self.study_type == self.INTRO:
            self.study_type = self.CARD
            self.progress_step = 0
        elif self.study_type == self.CARD:
            self.progress_step += 1
            if self.progress_step >= self.MAX_CARD:
                self.study_type = self.LISTENING
                self.progress_step = 0
        elif self.study_type == self.LISTENING:
            self.progress_step += 1
            if self.progress_step >= self.MAX_LISTENING:
                self.study_type = self.WRITING
                self.progress_step = 0
        elif self.study_type == self.WRITING:
            self.progress_step += 1
            if self.progress_step >= self.MAX_WRITING:
                self.study_type = self.INTRO
                self.progress_step = 0
        self.save()

    def previous_step(self):
        # Card -> intro
        if self.study_type == self.CARD:
            self.progress_step -= 1
            if self.progress_step < 0:
                self.study_type = self.INTRO
                self.progress_step = 0
        # listening -> card
        elif self.study_type == self.LISTENING:
            self.progress_step -= 1
            if self.progress_step < 0:
                self.study_type = self.CARD
                self.progress_step = self.MAX_CARD
        # writing -> listening
        elif self.study_type == self.WRITING:
            self.progress_step -= 1
            if self.progress_step < 0:
                self.study_type = self.LISTENING
                self.progress_step = self.MAX_LISTENING
        self.save()


class UserStudySessionModel(models.Model):
    max_correct = models.PositiveIntegerField(_("max correct"), default=15)
    max_session = models.PositiveIntegerField(_("max session"), default=30)
    correct = models.PositiveIntegerField(_("correct"), default=0)
    incorrect = models.PositiveIntegerField(_("incorrect"), default=0)
    current = models.PositiveIntegerField(_("current"), default=0)
    learn_id = models.PositiveIntegerField(_("learn id"), default=1)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE
    )
    words = models.ManyToManyField(
        "lesson.WordModel", verbose_name=_("words studied in the session")
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("UserStudySessionModel")
        verbose_name_plural = _("UserStudySessionModels")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pk} user: {self.user} word: {self.word}"
