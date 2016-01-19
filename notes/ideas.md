# Reactive Push Caching

- En ekstern application/process/deamon, der modtager notificationer/events
  omkring ændringer i 'underlying data'/'data source'/'input'. Ændringen/eventet
  identifieres af vha. et node_id og et instance_id (strenge).
  -> Når der kommer en ændring, slår vi den givne node op i vores graf

- An external application/process/deamon receives notification/events about
  changes in the underlying data/data source/input. A change is identified
  by a unique node_id and an instance_key (strings)
  -> When a change i received, the node is looked up in the graph with thec


# On out-of-memory:

- Evict values of lowest priority
