from topological_sort import topological_sort

class Scheduler:
    def __init__(self, sources):
        self._sources = sources
        self._sorted_nodes = self._topologically_sorted_nodes(sources)

    def update_dirty_nodes(self):
        for node in self._sorted_nodes:
            self._update_dirty_nodes(node.parents)

    def _topologically_sorted_nodes(self, sources):
        nodes = self._all_nodes(sources)
        return topological_sort(nodes)

    def _all_nodes(self, sources, nodes = set()):
        for node in sources:
            nodes.add(node)
            self._all_nodes(node.parents, nodes)
        return nodes

    def _add_nodes(self, node_set, node):
        node.add(node)
        for parent in node.parents:
            self._add_nodes(node_set, parent)

    def _update_dirty_nodes(self, nodes):
        for node in nodes:
            if node.is_dirty:
                node.update_value()
                self._update_dirty_nodes(node.parents)
