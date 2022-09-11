"""This module contains Question clas and Choice class."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """This class represents a model of question
    with some functional methods."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', null=True, blank=True)

    def __str__(self) -> str:
        """Return a text of a question."""
        return str(self.question_text)

    @admin.display(
        boolean=True,
        ordering=['pub_date', 'end_date'],
        description='Published recently?',
    )
    def was_published_recently(self) -> bool:
        """Check if the question is published within one day."""
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self) -> bool:
        """Check if the question is published."""
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self) -> bool:
        """Check if the question can be voted."""
        now = timezone.localtime()
        if not self.end_date:
            return self.is_published()
        return self.is_published() and now <= self.end_date


class Choice(models.Model):
    """This class is a subclass models.Model."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Return a test of a choice."""
        return str(self.choice_text)
