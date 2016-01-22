import sys
sys.path.append('../smache')

from smache import DependenceGraph, SourceNode, computed, MongoSourceNode

from mongoengine import connect
from fake_documents import Answer, Question, ReportGrade

db = connect('testdb', host='localhost', port=27017,)

class AnswerScoreGraph(DependenceGraph):
    answer       = MongoSourceNode(Answer)
    question     = MongoSourceNode(Question)
    report_grade = MongoSourceNode(ReportGrade)

    def __init__(self, source_id):
        DependenceGraph.__init__(self)
        answer = self.source('Answer').document_class.objects(id=source_id).first()
        question = answer.question
        report_grade = answer.report_grade
        self.set_value('Answer', answer)
        self.set_value('ReportGrade', report_grade)
        self.set_value('Question', question)

    @computed(answer, report_grade, question)
    def score(self, answer, r, q):
        if answer is None or r is None or q is None:
            return None
        q_score = 0.0
        if q.question_type == 'numerical':
            q_score = float(answer.numerical_answer - min(map(int, q.numericalAnswers.keys()))) / max(map(int, q.numericalAnswers.keys()))
        elif q.question_type == 'boolean':
            q_score = (1.0 if answer.boolean_answer else 0.0)
        return float("{0:.2f}".format(q_score))

    @computed(question)
    def max_score(self, q):
        if q is None:
            return None
        elif q.question_type == 'numerical':
            return 1.0
        elif q.question_type == 'boolean':
            return 1.0
        else:
            return 0.0

    @computed(score, question)
    def weighted_score(self, score, question):
        if score is None or question is None:
            return None
        return score * question.weight


def test_it_works():
    report_grade = ReportGrade()
    report_grade.save()

    question = Question(text='hello', question_type='numerical', weight=4)
    question.save()

    answer = Answer(numerical_answer='3', report_grade=report_grade, question=question)
    answer.save()

    graph = AnswerScoreGraph(answer.id)

    assert graph.get_value("score") == 1.0
    assert graph.get_value("weighted_score") == 4.0

def test_it_updates_values_when_source_changes():
    report_grade = ReportGrade()
    report_grade.save()

    question = Question(text='hello', question_type='numerical', weight=4)
    question.save()

    answer = Answer(numerical_answer=3, report_grade=report_grade, question=question)
    answer.save()

    graph = AnswerScoreGraph(answer.id)

    answer.numerical_answer = 1
    answer.save()

    question.weight = 3
    question.save()

    assert graph.score == 0.33
    assert graph.weighted_score == 0.99
