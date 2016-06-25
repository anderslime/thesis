\begin{minted}[linenos]{python}
def course_score(course)
    participants = Database.find_all_participants_in_course(course)
    total_score = 0
    for participant in participants:
        grades = Database.find_all_grades_for_participant(participant)
        total_score += numpy.advanced_statistical_method(participant)
    return total_score / len(participants)
\end{minted}
