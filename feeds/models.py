from typing import Iterable, Optional
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import QuerySet
from django.contrib.postgres.fields import ArrayField


class UnderSixty(models.QuerySet):
    def under(self) -> QuerySet:
        return self.filter(percent__lte=60)

    def up(self) -> QuerySet:
        return self.filter(percent__gt=60)


class PercentManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return UnderSixty(self.model, using=self._db)

    def under(self) -> QuerySet:
        return self.get_queryset().under()

    def up(self) -> QuerySet:
        return self.get_queryset().up()


class Feed(models.Model):
    title = models.CharField(max_length=50, error_messages={"required": " 제목을 입력해주세요."})
    payload = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rel_feed = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="RelationFeed",
        blank=True,
        related_name="+",
    )
    sim_word = models.OneToOneField(
        "FeedRelWord",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sim_feed",
    )


class FeedRelWord(models.Model):
    word_list = ArrayField(models.TextField(), blank=True)


class RelationFeed(models.Model):
    from_feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name="rel_from_feed",
    )
    sim_feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name="rel_sim_feed",
    )

    similar = models.FloatField([MinValueValidator(0.0), MaxValueValidator(100.0)])


class PayloadWord(models.Model):
    word = models.TextField()
    count = models.BigIntegerField(default=0)
    percent = models.FloatField(
        null=True, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    objects = models.Manager()
    percent_objects = PercentManager()

    class Meta:
        default_manager_name = "objects"
