# How do we record dependency between one computed instance that calls another?

This is not useful in our case. Maybe with another solution

## Example:
def h(a, b):
  return a + b

def k(a, b):
  return h(a, b) * 5

a --\
     h --> k
b --/

## The Smart one - Transaction Solution
- Solution:
  - We call k with a = 1 and b = 2
  - When calling k, start transaction 'tran(k)'
  - Record all computed funs running
    -> We run e.g. h(1, 2)
  - When k returns, stop transaction 'tran(k)'
  - We know that h was called with 1 and 2, and makes
    h(1, 2) a dependency of k(1, 2)

- Works assuming that k is pure
- If the purpose is to find dependencies between types of functions,
  we only need to find the function type and record that

## The simple one - Defining deps
@computed(a, b)
def h(a, b):
  return a + b

@computed(a, b)
def g(a):
  return a + b

@computed(a, b, computeds=(g, h))
def k(a, b):
  return h(a, b) * 5

- Then we know that k depends on:
  - h with input (a, b)
  - g with input (a)
