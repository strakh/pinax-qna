from django.core.exceptions import ObjectDoesNotExist
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended

from quanda.models import Question, Answer

class AnonymousQuestionHandler(AnonymousBaseHandler):
    model = Question
    fields = ('title', 'question_text', 'posted')

class QuestionHandler(BaseHandler):
    anonymous = AnonymousQuestionHandler
    model = Question
    fields = ('id', 'title', 'question_text', 'posted', 'last_modified', ('author', ('username',)))

class AnonymousAnswerHandler(AnonymousBaseHandler):
    model = Answer
    fields = ('answer_text', 'posted')

class AnswerHandler(BaseHandler):
    anonymous = AnonymousAnswerHandler
    model = Answer
    fields = ('id', 'answer_text', 'posted', 'last_modified', ('author', ('username',)))

    def create(self, request, *args, **kwargs):
        try:
            question = Question.objects.get(id=kwargs.get('question'))
        except ObjectDoesNotExist:
            return rc.BAD_REQUEST
        request.data.update({'question': question, 'author': request.user})
        super(AnswerHandler, self).create(request, *args, **kwargs)

