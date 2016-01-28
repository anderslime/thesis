# class TopologicalOrder:
#     def find(self, sources):
#         L = []
#         S = [node for node in nodes if node.__class__.__name__ == "SourceNode"]
#         removed_edges = set()
#         while len(S) > 0:
#             current_node = S.pop()
#             L.append(current_node)
#             for parent in current_node.parents:
#                 removed_edges.add(sorted(parent.node_id, current_node.node_id))
#                 if parent.kj
#
from collections import deque

GRAY, BLACK = 0, 1

class TopologicalSort:
    @classmethod
    def sort(cls, nodes):
        graph = cls.graph_from_nodes(nodes)
        order, state = deque(), {}
        enter = set(graph)

        def dfs(node_id):
            state[node_id] = GRAY
            (node, parents) = graph.get(node_id)
            for k in parents:
                sk = state.get(k.node_id, None)
                if sk == GRAY: raise ValueError("cycle")
                if sk == BLACK: continue
                enter.discard(k.node_id)
                dfs(k.node_id)
            order.appendleft(node)
            state[node_id] = BLACK

        while enter: dfs(enter.pop())
        return order

    @classmethod
    def graph_from_nodes(cls, nodes):
        graph = dict()
        for node in nodes:
            graph[node.node_id] = (node, node.parents)
        return graph



class Scheduler:
    def __init__(self, sources):
        self._sources = sources
        self._sorted_nodes = self._topologically_sorted_nodes(sources)

    def update_dirty_nodes(self):
        for node in self._sorted_nodes:
            self._update_dirty_nodes(node.parents)

    def _topologically_sorted_nodes(self, sources):
        nodes = self._all_nodes(sources)
        return TopologicalSort.sort(nodes)

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
