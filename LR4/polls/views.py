from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Choice, Question

from .forms import NewPollForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
               :5
               ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


@login_required(login_url='accounts:login')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))




class NewPollView(TemplateView):
    login_url = 'accounts:login'
    template_name = 'polls/new_poll.html'

    def get(self, request):
        form = NewPollForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewPollForm(request.POST)
        if form.is_valid():
            # Обработка данных
            question_text = form.cleaned_data['question_text']
            choices_text = form.cleaned_data['choices']

            # Создаем вопрос и варианты
            question = Question.objects.create(
                question_text=question_text,
                pub_date=timezone.now()
            )

            choices_list = [choice.strip() for choice in choices_text.split('\n') if choice.strip()]
            for choice_text in choices_list:
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    votes=0
                )

            return redirect('polls:detail', pk=question.id)

        return render(request, self.template_name, {'form': form})