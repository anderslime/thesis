from smache import SourceNode, ComputedNode, Scheduler, topological_sort

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


def test_topological_order():
    nodes = [user_ass_grade, assignment, user_grade, grade, user]
    ordered_nodes = topological_sort(nodes)
    ordered_node_ids = [node.node_id for node in ordered_nodes]
    assert ordered_node_ids == [
        "User",
        "Assignment",
        "Grade",
        "user_grade",
        "user_ass_grade"
    ]
