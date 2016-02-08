from smache import SourceNode, ComputedNode, Scheduler


assignment = SourceNode("Assignment")
user       = SourceNode("User")
grade      = SourceNode("Grade")

user_grade = ComputedNode("user_grade",
                          lambda user, grade: {'user': user, 'grade': grade},
                          user, grade)

user_ass_grade = ComputedNode("user_ass_grade",
                              lambda ass, user_grade: {'ass': ass, 'user_grade': user_grade},
                              assignment, user_grade)

# assignment -----------------\
#                               user_ass_grade
# user       \                /
#              user_grade ---/
# grade      /

# We need some root!!!

def test_all_is_dirty_from_init():
    assert user_grade.is_dirty
    assert user_ass_grade.is_dirty


def test_computed_values_are_not_computed_lazily():
    assignment.set_value("ASS_VALUE")
    user.set_value("USER_VALUE")
    grade.set_value("GRADE_VALUE")

    assert user_grade.value == None
    assert user_ass_grade.value == None


def test_user_grade_values_are_calculated_when_values_are_set():
    assignment.set_value("ASS_VALUE")
    user.set_value("USER_VALUE")
    grade.set_value("GRADE_VALUE")

    expected_user_grade_value = {
        'user': "USER_VALUE",
        'grade': "GRADE_VALUE"
    }
    expected_user_ass_grade_value = {
        'ass': 'ASS_VALUE',
        'user_grade': expected_user_grade_value
    }

    scheduler = Scheduler([assignment, user, grade])
    scheduler.update_dirty_nodes()

    assert user_grade.value == expected_user_grade_value
    assert user_ass_grade.value == expected_user_ass_grade_value
