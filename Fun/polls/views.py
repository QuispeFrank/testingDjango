# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.views import generic


# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", { "latest_question_list": latest_question_list })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ Return the last five published questions """
        return Question.objects.order_by("-pub_date")[:5]

# def details(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/details.html", {"question": question})

class DetailsView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {
#         "question": question
#     })

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/details.html", {
            "question": question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))