\begin{minted}[linenos]{python}
# Fictive course
course = Course(id='56123123jkasd')

# Assumed output
print course_score(course)
# => 5.52

# Serialization of cached object for course_score called with course
computed_key = smache.computed_key(course_score, course)

print computed_key
# => 'module_name.course_score~~~56123123jkasd'

# Deserialization
computed_fun, arguments = smache.deserialized_fun(computed_key)

print computed_fun(*arguments)
# => 5.52
\end{minted}
