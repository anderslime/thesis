\begin{minted}[linenos]{python}
def course_score(course)
	participants = ParticipantDB.find_by_course(course)
	total_score = 0
	for participant in participants:
		total_score += participant_score(participant)
	return total_score / len(participants)

def participant_score(participant):
	return numpy.advanced_statistical_method(participant)
\end{minted}
