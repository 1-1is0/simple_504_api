from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class UserStudyWordModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE
    )
    word = models.ForeignKey(
        "lesson.WordModel", verbose_name=_("word"), on_delete=models.CASCADE
    )
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
