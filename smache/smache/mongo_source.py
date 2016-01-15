from mongoengine import signals
from source_node import SourceNode

class MongoSourceNode(SourceNode):
    def __init__(self, document_class, **kwargs):
        SourceNode.__init__(self, document_class.__name__)
        self.document_class = document_class
        self.graph          = None
        self.kwargs         = kwargs

    def set_graph(self, graph):
        self.graph = graph
        self._hook_into_mongoengine()

    def _hook_into_mongoengine(self):
        signals.post_save.connect(self._after_save, sender=self.document_class)

    def _after_save(self, sender, document, **kwargs):
        self.set_value(document)
