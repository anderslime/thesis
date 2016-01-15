from mongoengine import *
from smache import SourceNode

class Question(Document):
    objectTypeName = 'Question' # Shown in 404 errors
    text = StringField(required=True)
    question_type = StringField(required=True)
    positiveAnswerText = StringField(default='Yes')
    negativeAnswerText = StringField(default='No')
    numericalAnswers = DictField(default={'0': 'No answer', '1': 'Below expectations', '2': 'Meets expectations', '3': 'Above expectations'})
    weight = FloatField(default=1, required=True)

class ReportGrade(Document):
    feedback_grade = IntField()
    state = StringField(default='new')
    started_at = DateTimeField()
    submitted_at = DateTimeField()
    time_spent = IntField()

    def score(self):
        max_score = 0
        score = 0
        for a in Answer.objects(report_grade=self):
            if a.question.question_type == 'numerical':
                max_score += 5
                score += a.numerical_answer
            elif a.question.question_type == 'boolean':
                max_score += 5
                score += 5 if a.boolean_answer else 1
            else:
                # Text answer don't count towards the score
                pass

        return float(score) / float(max_score) * 5

class Answer(Document):
    numerical_answer = IntField(min_value=0)
    boolean_answer = BooleanField()
    text_answer = StringField()
    question = ReferenceField(Question, reverse_delete_rule=CASCADE, required=True)
    report_grade = ReferenceField(ReportGrade, reverse_delete_rule=CASCADE, required=True)
    flagged = BooleanField(default=False)
    flag_comment = StringField()
    teacher_approved_flag = BooleanField(default=None)
    teacher_grade = DictField()
