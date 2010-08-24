from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.doc import documentation_view
from piston.authentication import HttpBasicAuthentication

from handlers import QuestionHandler, AnswerHandler

auth = HttpBasicAuthentication(realm='Quanda API')
questions = Resource(handler=QuestionHandler, authentication=auth)
answers = Resource(handler=AnswerHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^questions/$', questions, name='api_questions'),
    url(r'^question/(?P<id>\d+)/$', questions, name='api_question'),
    url(r'^question/(?P<question>\d+)/answers/$', answers, name='api_question_answers'),
    url(r'^answer/(?P<id>\d+)/$', answers, name='api_question_answer'),

    # automated documentation
    url(r'^$', documentation_view),
)