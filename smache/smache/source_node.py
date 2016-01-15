class SourceNode:
    def __init__(self, id, value = None):
        self.id       = id
        self.value    = value
        self._parents = []

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self.value = new_value
        self._update_parents()

    def add_parent(self, new_parent):
        self._parents.append(new_parent)

    def _update_parents(self):
        for parent in self._parents:
            parent.update()
