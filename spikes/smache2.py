class SourceNode:
    def __init__(self, id, value = None):
        self.id       = id
        self._parents = []
        self.value    = value

    def did_update(self):
        print "Updating myself %s" % self.id
        # Update dependencies

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        print "Updating source value {}".format(new_value)
        self.value = new_value
        for parent in self._parents:
            print "Cascaded updating parent {}".format(parent.id)
            parent.update()

    def set_parent(self, new_parent):
        self._parents.append(new_parent)

class ComputedNode:
    def __init__(self, id, dependencies = []):
        self.id            = id
        self._value        = None
        self._dependencies = []
        self._parents      = []

        self._set_dependencies(dependencies)
        self.update()

    def update(self):
        print "Updating myself %s" % self.id
        values = [node.value for node in self._dependencies]
        self.value = self.evaluate(*values)
        for parent in self._parents:
            print "Cascaded updating parent {}".format(parent.id)
            parent.update()

    def evalute(self, **input):
        raise NotImplementedError(
            "{} does not implement evaluate".format(self.__class__.__name__)
        )

    def _set_dependencies(self, dependencies):
        self._dependencies = dependencies
        for dependency in dependencies:
            dependency.set_parent(self)

    def set_parent(self, new_parent):
        self._parents.append(new_parent)


class StudentGrade(ComputedNode):
    def evaluate(self, student, grades):
        return {
            'student': student,
            'grade': self._average_grade(grades)
        }

    def _average_grade(self, grades):
        return float(sum(grades)) / len(grades)

if __name__ == '__main__':
    student = SourceNode("Student", { 'name': 'Henrik' })
    grades  = SourceNode("Grades", [2, 4])
    student_grade_inputs = (student, grades)
    student_grade = StudentGrade("StudentGrade", (student, grades))

    print student_grade.value

    grades.set_value([4, 6])

    print student_grade.value
