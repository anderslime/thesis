\begin{minted}[linenos]{python}
def update_cached_object(key):
    if not CacheDB.is_cached_object_fresh(key):
        # Deserialize and execute cached function
        cached_function, arguments = deserialized_fun(key)
        computed_value = cached_function(*arguments)

        # Store the new value unless it has been
        # updated by another update process
        computation_timestamp = CacheDB.last_update_timestamp(key)
        CacheDB.store(key, computed_value, timestamp)
\end{minted}
