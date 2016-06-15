\begin{minted}[linenos]{python}
import time
import random
import json

retries = 25

def store(key, value, computation_timestamp):
    # Use a pipeline to execute more than one command
    pipeline = RedisConnection.pipeline()
    store_retry(key, value, computation_timestamp, pipe, retries)

def store_with_retry(key, value, computation_timestamp, pipe, retries):
    try:
        if retries > 0:
            # Execute WATCH command
            pipe.watch(key)

            # Fetch the current cache object
            current_cache_object = CacheStore.fetch(key)

            # Update the value and last_update_timestamp if it has
            # a newer timestamp than the current_cache_object
            if has_newer_timestamp(cache_object, current_cache_object):
                pipe.multi()
                pipe.hset(key, 'value', json.dumps(value))
                pipe.hset(key, 'last_update_timestamp', computation_timestamp)
                pipe.execute()

    except WatchError:
        # This is executed if the key was modified by another process
        # during the transaction. We wait for a random number of seconds
        # and retry
        time.sleep(random.random())
        store_entry(key, value, computation_timestamp, retries - 1)

def has_newer_timestamp(cache_object, computation_timestamp):
    """
    Checks if the timestamp from the computation is newer than the
    one for the current stored cache object
    """
    return cache_object.num_of_updates is None or \
        computation_timestamp > cache_object.num_of_updates
\end{minted}
