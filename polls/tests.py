import datetime
from django.urls import reverse
from django.test import TestCase, Client
from django.utils import timezone

from .models import Question


def create_question(question_text, days, seconds=0, end_in=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.localtime() + datetime.timedelta(days=days, seconds=seconds)
    return Question.objects.create(question_text=question_text, pub_date=time,
                                   end_date=time + datetime.timedelta(days=end_in))


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        future_question = create_question(question_text="Future question.", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.localtime() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for questions whose pub_date
        is in the future.
        """
        future_question = create_question(question_text="Future question.", days=1)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_recent_question(self):
        """
        is_published() return True for questions whose pub_date
        is equal or older than now.
        """
        recent_question1 = Question(question_text="Recent question.", pub_date=timezone.localtime())
        self.assertIs(recent_question1.is_published(), True)
        time = timezone.localtime() - datetime.timedelta(hours=0, minutes=0, seconds=1)
        recent_question2 = Question(question_text="Recent question.", pub_date=time)
        self.assertIs(recent_question2.is_published(), True)

    def test_can_vote_with_future_question(self):
        """
        can_vote() return False for question whose pub_date
        is in the future.
        """
        future_question = create_question(question_text="Future question.", days=1)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_after_end_date(self):
        """
        can_vote() return False for question whose end_date
        is in the past.
        """
        # end date pasted by 1 sec
        ended_question = create_question(question_text="Ended question.", days=-1, seconds=-1, end_in=1)
        self.assertIs(ended_question.can_vote(), False)

    def test_can_vote_when_now_equal_to_end_date(self):
        """
        can_vote() return True for question whose end_date
        is the current present.
        """
        now_question = create_question(question_text="Now question.", days=-1, end_in=1)
        self.assertIs(now_question.can_vote(), True)

    def test_can_vote_before_end_date(self):
        """
        can_vote() return True for published question whose
        end_date is the future.
        """
        question = create_question(question_text="Now question.", days=0, end_in=5)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_question_without_end_date(self):
        """
        can_vote() return True for published question without end_date.
        """
        time = timezone.localtime()
        no_end_date_question = Question(pub_date=time)
        self.assertIs(no_end_date_question.can_vote(), True)
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.can_vote(), True)

    def test_can_vote_published_date(self):
        """
        can vote() return True for published now question.
        """
        question = Question(pub_date=timezone.localtime())
        self.assertIs(question.can_vote(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 redirect to index view.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5, end_in=10)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTests(TestCase):
    def test_vote_count_display_correctly(self):
        """
        The ResultView should display the vote count of question correctly.
        """
        question = create_question(question_text='Some interesting question.', days=-2)
        question.choice_set.create(choice_text="5/5", votes=0)
        choice = question.choice_set.get(pk=1)
        choice.votes += 2
        question.save()
        choice.save()
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, choice.votes)

    def test_future_question(self):
        """
        The result view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
