"""This module contains IndexView class, DetailView class, ResultsView class, and vote function."""

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


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
        try:
            self.object = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request, 'No such question.')
            return HttpResponseRedirect(reverse('polls:index'))
        # If someone navigates to a poll detail page when voting is not allowed,
        # redirect them to the polls index page
        else:
            if not self.object.is_published():
                messages.error(request, 'That given question is not published yet.')
                return HttpResponseRedirect(reverse('polls:index'))
            if not self.object.can_vote():
                messages.error(request, 'This question is closed.')
                return HttpResponseRedirect(reverse('polls:results', args=(self.object.id,)))
            return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """This class provides a view for result page."""
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any results of questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())


def vote(request, question_id):
    """
    Increment a vote count for selected choice.
    """
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
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
