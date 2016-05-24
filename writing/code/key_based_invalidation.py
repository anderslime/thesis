\begin{minted}[linenos]{python}

def cached_value(entity):
    """
    A function where the time consuming part is cached.
    The time_consuming_function is only called if it
    is not already cached.
    """
    cache_key_components = [
        entity.type,
        entity.id,
        entity.update_timestamp
    ]
    cache_key = '/'.join(cache_key_components)
    with cache(cache_key):
        return time_consuming_function(entity)

# Load the entity from the primary storage
entity = Entity.load_from_database

# Call the cached version of the time_consuming_function
print cached_value(entity)

# This second time it is called, the return value for
# the time_consuming_function is cached, which means it
# returns the value from the cache
print cached_value(entity)

\end{minted}
