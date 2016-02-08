from scheduler import Scheduler

class ComputedNode:
    def __init__(self, node_id, action, *dependencies):
        self.node_id      = node_id
        self._action      = action
        self.dependencies = dependencies
        self.value        = None
        self.is_dirty     = True
        self.parents     = []
        self._add_dependencies(dependencies)

    def update_value(self):
        values = [node.value for node in self.dependencies]
        self.value = self.evaluate(*values)
        self.is_dirty = False
        return self.value

    def mark_as_dirty(self):
        self.is_dirty = True
        self._mark_parents_as_dirty()

    def evaluate(self, *input):
        return self._action(*input)

    def add_parent(self, parent):
        self.parents.append(parent)

    def _add_dependencies(self, dependencies):
        for dependency in dependencies:
            dependency.add_parent(self)

    def _mark_parents_as_dirty(self):
        for parent in self.parents:
            parent.mark_as_dirty()


class SourceNode:
    def __init__(self, node_id):
        self.node_id  = node_id
        self.value    = None
        self.parents = []

    def set_value(self, new_value):
        self.value = new_value
        self._mark_parents_as_dirty()

    def add_parent(self, parent):
        self.parents.append(parent)

    def _mark_parents_as_dirty(self):
        for parent in self.parents:
            parent.mark_as_dirty()
