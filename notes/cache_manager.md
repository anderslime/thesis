# Cache Manager

## Query Flow

1. A function is called with (pure) arguments (let's call them 'a' and 'b')
2. The cache cache manager is queried with fun and args:
  2a. Cached value exists and is not dirty: return cached value and exit
  2b. Cached value does not exist or is dirty: go to 3
3. Run update flow with function

### Queries performed

- Check if cached value exists
- Check if cached value is dirty

## Cache Update Flow on Fun Exec

1. Execute fun with args
2. Store result in cache with key hash(fun, args)
3. Mark fun with args as fresh (not dirty)

Note: since dependent funs are executes with the function, they are also
      automatically updated in the execution.

### Queries performed

- Store cached value


## Cache Update Flow on Data Source Update

1. Find all depending nodes instances of data source instance
2. Sort the nodes in topological order
3. Execute the cache update flow on each fun

### Queries performed

- Find all depending nodes of a data source (in topological order)
- or those in two seperate steps

## Optimization Idea:

- Instead of performing a cache query on each result, run some/all the functions
  and store them in a batch. This way the parent nodes can access it's dependent
  results in memory instead of querying what has just been computed.
  -> To prevent memory overload we could have schedules that executes a batch
     of funs and then saves them in the end of the schedule and then execute
     the next. If these need to run in parallel, we need to find depending
     schedules.

## Queries Need to be supported
