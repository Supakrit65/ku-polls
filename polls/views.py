"""This module contains IndexView class, DetailView class, ResultsView class, and vote function."""

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    """This class provides a view of index page."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.localtime()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """This class provides a view for detail page."""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())

    def get(self, request, *args, **kwargs):
        """Redirect to pages according to the status of question."""
        user = request.user
        self.question = None
        try:
            self.question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request, 'No such question.')
            return HttpResponseRedirect(reverse('polls:index'))
        # If someone navigates to a poll detail page when voting is not allowed,
        # redirect them to the polls index page
        else:
            if not self.question.is_published():
                messages.error(request, 'That given question is not published yet.')
                return HttpResponseRedirect(reverse('polls:index'))
            if not self.question.can_vote():
                messages.error(request, 'This question is closed.')
                return HttpResponseRedirect(reverse('polls:results', args=(self.question.id,)))
            selected_choice_info = ''
            if not user.is_anonymous:
                try:
                    vote_object = Vote.objects.get(user=user, choice__in=self.question.choice_set.all())
                    selected_choice_info = vote_object.choice.choice_text
                except Vote.DoesNotExist:
                    selected_choice_info = ''
                return render(request, 'polls/detail.html',
                              {'question': self.question, 'check_info': selected_choice_info})
            return render(request, 'polls/detail.html',
                          {'question': self.question, 'check_info': selected_choice_info})


class ResultsView(generic.DetailView):
    """This class provides a view for result page."""
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any results of questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())


@login_required
def vote(request, question_id):
    """
    create or update Vote object when vote occurs.
    """
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redirect to the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            vote_object = Vote.objects.get(user=user, choice__in=question.choice_set.all())
        except Vote.DoesNotExist:
            # create a new vote object for that question for user
            new_vote = Vote.objects.create(user=user, choice=selected_choice)
            new_vote.save()
            messages.success(request, "Congratulation! Vote taken.", fail_silently=True)
        else:
            vote_object.choice = selected_choice
            vote_object.save()
            messages.success(request, "Congratulation! Vote Updated.", fail_silently=True)
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
