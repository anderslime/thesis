ud(assignment) --> c(estimated_grade) --\
                                         c(grad_precision)
ud(grade) ------------------------------/



ud(assignment) ---\
  \                c(grad_precision)
   ud(grade) -----/

- On grade update:
  -> We receive grade_id
  -> Lookup the computations that depends on grade
    => grade_precision
  -> Run these computations in a topological order with some argument that
     describes the given instances. Could be hash of underlying data id's and function names.
    ->
- Query:
  - Map from node to other node based on function.

@computed(assignment)
def estimated_grade(assignment):
  return assignment.awesomeness * assignment.average

@computed(grade, assignment, deps=(estimated_grade))
def grade_precision(grade, assignment):
  return grade.value - estimated_grade(assignment)
