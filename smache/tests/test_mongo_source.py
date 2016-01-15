import sys
sys.path.append('../smache')

from smache import DependenceGraph, SourceNode, computed, MongoSourceNode

from mongoengine import connect
from fake_documents import Answer, Question, ReportGrade

db = connect('testdb', host='localhost', port=27017,)

class AnswerScoreGraph(DependenceGraph):
    answer = MongoSourceNode(Answer)
    question = MongoSourceNode(Question, from_model=Answer)
    report_grade = MongoSourceNode(ReportGrade, from_model=Answer)

    def __init__(self, source_id):
        DependenceGraph.__init__(self)
        answer = self.source('Answer').document_class.objects(id=source_id).first()
        question = answer.question
        report_grade = answer.report_grade
        self.set_value('Answer', answer)
        self.set_value('ReportGrade', report_grade)
        self.set_value('Question', question)

    @computed(report_grade)
    def score(self, report_grade):
        if report_grade is None:
            return None
        return report_grade.feedback_grade * 0.5

    @computed(score, question)
    def weighted_score(self, score, question):
        if score is None or question is None:
            return None
        return score * question.weight


def test_it_works():
    report_grade = ReportGrade(feedback_grade=5)
    report_grade.save()

    question = Question(text='hello', question_type='score', weight=4)
    question.save()

    answer = Answer(report_grade=report_grade, question=question)
    answer.save()

    graph = AnswerScoreGraph(answer.id)

    assert graph.get_value("score") == 2.5
    assert graph.get_value("weighted_score") == 10.0

def test_it_updates_values_when_source_changes():
    report_grade = ReportGrade(feedback_grade=5)
    report_grade.save()

    question = Question(text='hello', question_type='score', weight=4)
    question.save()

    answer = Answer(report_grade=report_grade, question=question)
    answer.save()

    graph = AnswerScoreGraph(answer.id)

    report_grade.feedback_grade = 10
    report_grade.save()

    question.weight = 5
    question.save()

    assert graph.get_value("score") == 5.0
    assert graph.get_value("weighted_score") == 25.0
