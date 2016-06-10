\begin{minted}[linenos]{python}
@smache.relations(
    (Participant, lambda participant: participant.courses)
)
@smache.computed(Course)
def course_score(course)
    participants = Database.find_all_participants_in_course(course)
    total_score = 0
    for participant in participants:
        total_score += time_consuming_participant_score(participant)
    return total_score / len(participants)

@smache.relations(
    (Grade, lambda grade: grade.graded_participant)
)
@smache.computed(Participant)
def time_consuming_participant_score(participant):
    grades = Database.find_all_grades_for_participant(participant)
    return numpy.advanced_statistical_method(participant)
\end{minted}
