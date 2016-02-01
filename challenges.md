# Relationships Between Data:

## Dependent model has input as attribute.

### Data model

grade => user

### Function
def grade(user_id):
  grade = Grade.find_by_user_id(user_id)
  user  = User.find(user_id)
  return grade.value * user.awesomeness

ud(grade) --> ud(user) --> c(grade)

### Update:
- Updates on grade.value and user.awesomeness
- What to do when:
  - Grade is updated/inserted/removed:
    - Find user_id by grade.user_id
  - User is updated/inserted/removed
    - Just find id

### Query
user = User.find(user_id)
cached_value = grade(user_id)


## Dependent model does not have attributes related to key

### Data model

grade <= assignment

### Function
def ass_grade(assignment_id):
  assignment = Assignment.find(assignment_id)
  grade      = Grade.find(assignment.grade_id)
  return grade.value * assignment.weight

ud(grade) <-- ud(assignment) --> c(ass_grade)

### Update
- Updates on assignment.weight and grade.value
- What to do when:
  - Grade is updated/inserted/removed:
    - Find assignment for given grade (Assignment.find_by_grade_id(grade_id)
  - Assignment is updated/inserted/removed:
    - Just use id

### Query
user = User.find(user_id)
cached_value = grade(user_id)

## Multiple inputs (without data relationship)

### Data model

user, assignment (no relationship)

### Function
def estimated_grade(user_id, assignment_id)
  assignment = Assignment.find(assignment_id)
  user       = User.find(user_id)
  return user.awesomeness * assignment.weight

ud(user) --------\
                  c(estimated_grade)
ud(assignment) --/

### Update
- Updates on user.weight and assignment.value
- What to do when:
  - Assignment is updated/inserted/removed:
    - Find id and update all estimated grades
  - User is updated/inserted/removed:
    - Find id and update all estimated grades

## Multiple inputs (with data relationship)

### Data model

user <-- grade, course

### Function
def course_grade(user_id, course_id)
  user = User.find(user_id)
  grade = Grade.find_by_user_id(user_id)
  course = Course.find(course_id)
  return user.awesomeness * grade.value - course.relevance

ud(grade) --> ud(user) --------\
                                c(estimated_grade)
ud(assignment) ----------------/

### Update
- Updates on user.awesomeness, grade.value and course.relevance
- What to do when:
  - User is updated/inserted/removed:
    - Find id and update all estimated grades
  - Grade is updated/inserted/removed:
    - Find ud(user) by property and update estimated grades
  - Grade is updated/inserted/removed:
    - Find id and update all estimated grades

## Computations that depends on computations


ud(assignment) --> c(estimated_grade) --\
                                         c(grad_precision)
ud(grade) ------------------------------/

### Function


@computed(assignment)
def estimated_grade(assignment)
  return assignment.awesomeness * assignment.average

@computed(grade, assignment, estimated_grade)
def grade_precision(grade, assignment)
  return grade.value - assignment.count



can be written as:

def grade_precision(grade_id, assignment_id):
  grade = Grade.find(grade_id)
  retur my_grade_precision(grade, assignment_id)

def my_grade_precision(grade, assignment_id)
  return grade.value - estimated_grade(assignment_id)

### Update
- estimated_grade updates on assignment
- grade_precision updates on:
  - estimated grade that updates on assignment
  - grade by id

- What to do when:
  - Assignment updates:
    - update estimated grade and then grade precision
  - Grade updates
    - update grade_precision by id

