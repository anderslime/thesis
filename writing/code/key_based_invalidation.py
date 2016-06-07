\begin{minted}[linenos]{python}
def time_consuming_participant_score(participant):
    return numpy.advanced_statistical_method(participant)

def cache_key_for_participant_score(participant):
    cache_key_components = [
        'cached_participant_score',
        participant.type,
        participant.id,
        participant.update_timestamp
    ]
    return '/'.join(cache_key_components)

def cached_participant_score(participant):

    cache_key = cached_participant_score(participant)
    if is_fresh_in_cache(cache_key):
        return fetch_from_cache(cache_key)
    else:
        result = time_consuming_participant_score(participant)
        set_cached_value(cache_key, result)
        return result

# Load the participant from the primary storage
participant = ParticipantDB.load_one_from_database

# Call the cached version of the time_consuming_participant_score
print cached_participant_score(participant)

# This second time it is called, the return value for
# the time_consuming_participant_score cached, which
# means it returns the value from the cache
print cached_participant_score(participant)
\end{minted}