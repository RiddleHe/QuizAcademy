from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AddQuestion, AddQuiz


from .models import Question, Quiz, Score

# Create your views here.

@login_required
def index(request):
    # pull up the user's past scores
    temp = Score.objects.filter(user=request.user).order_by('-created_time')
    if len(temp) >= 3:
        scores = temp[0:3]
    else:
        scores = temp
    # pull up the user's past quiz
    quizzes = Quiz.objects.all()
    # send context
    context = {'scores': scores, 'quizzes': quizzes}
    return render(request, 'quizzes/index.html', context)

@login_required
def quiz(request, quiz_id):
    """Load the individual quiz page and the first question"""
    quiz = Quiz.objects.get(id=quiz_id)
    scores = Score.objects.filter(quiz=quiz, user=request.user).order_by('-created_time')

    if request.method == "POST":
    # get ready to see the first question

        # pull up the first question
        question = quiz.head
        # create the score and save it
        score = Score()
        score.quiz = quiz
        score.user = request.user
        score.save()

        return HttpResponseRedirect(reverse('quizzes:question', args=[question.id]))

    # display quiz info
    context={'quiz': quiz, 'scores': scores}
    return render (request, 'quizzes/quiz.html', context)

@login_required
def question(request, question_id):
    """Load the question"""
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        # pull up the score
        scores = Score.objects.filter(user=request.user).order_by('-created_time')
        score = scores[0]
        # change the score
        score.total += 1
        if question.answer == request.POST.get("options"):
                score.score += 10
                score.correct += 1
        else:
                score.wrong += 1
        score.percentage = score.score / (score.total*10) * 100
        score.save()
        # pull up the next question
        question = question.next_question
        # check if this is the last question, if it is, to next
        if question != None:  

            return HttpResponseRedirect(reverse('quizzes:question', args=[question.id]))
        # if it's not, submit and see score
        else: 
            return HttpResponseRedirect(reverse('quizzes:result'))

        
    context = {'question': question}
    return render(request, 'quizzes/question.html', context)

@login_required
def result(request):
    """Load the result page"""
    # pull up the score
    scores = Score.objects.filter(user=request.user).order_by('-created_time')
    score = scores[0]
    context = {'score': score}
    return render(request, 'quizzes/result.html', context)

@login_required
def add_question(request, quiz_id):
    """Add a new question and set up what the previous question is"""
    quizzes = Quiz.objects.all()
    target_quiz = Quiz.objects.get(id=quiz_id)
    node = target_quiz.head
    nodes = []
    while node != None:
        nodes.append(node)
        node = node.next_question

    if request.method != 'POST':
        form = AddQuestion()

    else:
        form = AddQuestion(request.POST)
        if form.is_valid():
            new_question=form.save(commit=False)
            # if the question is not the head
            if request.POST.get("question_name") != None and request.POST.get("quiz_name") == None:
                new_question.prev_question = Question.objects.get(name=request.POST.get("question_name"))
                prev = new_question.prev_question
                new_question.next_question = prev.next_question
                next = prev.next_question
                if next != None:
                    next.prev_question = new_question
                prev.next_question = new_question
                new_question.save()
            # if question is the head
            elif request.POST.get("question_name") != None and request.POST.get("quiz_name") == None:
                quiz = Quiz.objects.get(name=request.POST.get("quiz_name"))
                if quiz.head != None:
                    new_question.next_question = quiz.head
                    quiz.head.prev_question = new_question
                    new_question.save()
                    quiz.head.save()
                quiz.head = new_question
                new_question.save()
                quiz.save()
            return HttpResponseRedirect(reverse('quizzes:index'))

    
    context={'form': form, 'quizzes': quizzes, 'nodes': nodes, 'target_quiz':target_quiz}
    return render(request, 'quizzes/add_question.html', context)

@login_required
def add_quiz(request):
    """Add a new quiz and proceed to add head question"""
    if request.method != 'POST':
        form = AddQuiz()

    else:
        form = AddQuiz(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            return HttpResponseRedirect(reverse('quizzes:add_question', args=[quiz.id]))

    
    context={'form': form}
    return render(request, 'quizzes/add_quiz.html', context)

@login_required
def edit_quiz(request):
    """Add a new quiz and proceed to add head question"""
    quizzes = Quiz.objects.all()

    if request.method == "POST":
        quiz_name = request.POST.get("edit_quiz")
        quiz = Quiz.objects.get(name=quiz_name)
        return HttpResponseRedirect(reverse('quizzes:add_question', args=[quiz.id]))

    
    context={'quizzes': quizzes}
    return render(request, 'quizzes/edit_quiz.html', context)

@login_required
def delete_score(request, score_id):
    score = Score.objects.get(id=score_id)
    if score.user == request.user:
        score.delete()
    return HttpResponseRedirect(reverse('quizzes:index'))

@login_required
def delete_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz.delete()
    return HttpResponseRedirect(reverse('quizzes:index'))