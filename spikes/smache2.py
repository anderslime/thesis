DEBUG = False

def debug(message):
    if DEBUG == True:
        print message

class SourceNode:
    def __init__(self, id, value = None):
        self.id       = id
        self._parents = []
        self.value    = value

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        debug("Updating source value {}".format(new_value))
        self.value = new_value
        for parent in self._parents:
            debug("Cascaded updating parent {}".format(parent.id))
            parent.update()

    def set_parent(self, new_parent):
        self._parents.append(new_parent)

class ComputedNode:
    def __init__(self, id, *dependencies):
        self.id            = id
        self._value        = None
        self._dependencies = []
        self._parents      = []

        self._set_dependencies(dependencies)
        self.update()

    def update(self):
        debug("Updating myself %s" % self.id)
        values = [node.value for node in self._dependencies]
        self.value = self.evaluate(*values)
        for parent in self._parents:
            debug("Cascaded updating parent {}".format(parent.id))
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
        if grades is None:
            return None
        return float(sum(grades)) / len(grades)

class Graph:
    def __init__(self):
        student       = SourceNode("Student")
        grades        = SourceNode("Grades")
        student_grade = StudentGrade("StudentGrade", student, grades)
        self.sources = (student, grades)
        self.nodes = self.sources + tuple([student_grade])

    def set_value(self, node_id, new_value):
        node = next(node for node in self.sources if node.id == node_id)
        node.set_value(new_value)

    def get_value(self, node_id):
        node = next(node for node in self.nodes if node.id == node_id)
        return node.value

if __name__ == '__main__':
    graph = Graph()

    print graph.get_value("StudentGrade")

    graph.set_value("Student", "Henrik")
    graph.set_value("Grades",  [2, 4])

    print graph.get_value("StudentGrade")

    # smache        = Smache()
    #
    #
    # smache.cache_graph("StudentGrade", student, grades)
    # smache.create_graph_instance(
    #     "StudentGrade",
    #     ("Student", 1, 'Henrik'),
    #     ("Grade", 60, [2, 4])
    # )
    #
    # print student_grade.value
    #
    # grades.set_value([4, 6])
    # student.set_value({'name': 'Henrik'})
    #
    # print student_grade.value
