from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CourseModel(models.Model):
    name = models.CharField(_("course name"), max_length=128)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("CourseModel")
        verbose_name_plural = _("CourseModels")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pk} {self.name}"

    def get_absolute_url(self):
        return reverse("CourseModel_detail", kwargs={"pk": self.pk})


class UnitModel(models.Model):
    name = models.CharField(_("unit name"), max_length=50)
    lesson = models.ForeignKey(
        "lesson.CourseModel", verbose_name=_("Course"), on_delete=models.CASCADE
    )
    # TODO image for unit

    audio = models.FileField(_("audio"), upload_to="unit_audios/", blank=True)
    description = models.TextField(_("description"), blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("UnitModel")
        verbose_name_plural = _("UnitModels")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pk} {self.name}"

    def get_absolute_url(self):
        return reverse("UnitModel_detail", kwargs={"pk": self.pk})


class WordModel(models.Model):
    unit = models.ForeignKey(
        "lesson.UnitModel", verbose_name=_(""), on_delete=models.CASCADE
    )
    word = models.CharField(_("word"), max_length=128)
    part_of_speech = models.CharField(_("part of speech"), max_length=50)
    definition = models.TextField(_("definition"))
    examples = models.TextField(_("examples"))
    image = models.ImageField(_("image"), upload_to="word_images/", blank=True)

    # this fields are not applicable to all words
    adjective = models.CharField(_("adjective"), max_length=50, blank=True)
    noun = models.CharField(_("noun"), max_length=50, blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("WordModel")
        verbose_name_plural = _("WordModels")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pk} {self.word}"

    def get_absolute_url(self):
        return reverse("WordModel_detail", kwargs={"pk": self.pk})
