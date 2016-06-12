# Outline

- Introduction
  - Problem & Requirements
  - Peergrade.io
  - formal stuff

- Caching Model
  - Intro:
    - Goals of caching (maybe make this a section of its own - look at length)
    - Present chapter
  - Caching basics
    - Terminology
      - Registration
      - Invalidation
      - Updating the cache
        - (Pull-based, pull-based) - maybe wait until next chapter
    - Architecture
      - Tell something about asynchronous/concurrent
      -
  - Evaluating caching technique
    - Goals of caching
    - Criteria
      - Freshness
      - Consistency
      - Ease of management (invalidation)
      - Cache hit rate / Have to wait for computation?
      - Granularity


- Existing caching approaches
  - Intro:
    - Solutions within invalidation + cache update + general approaches in web dev
      - We evaluate the overall approaches based on criteria from last chapter
      - + evaluate the concrete solutions based on requirements of the system
    - We discuss + evaluate based on criteria from last chapter.
  - Invalidation techniques
    - Expiration based invalidation
    - Key-based invalidation
    - Trigger-based invalidation
      - Just invalidate or write through
    - Automatic invalidation
  - Updating the cache
    - Solutions within pull and push-based
    - Data update propagation
  - Caching techniques in web development
    - DB Query caching
      - Materialized views
      - ORM-query caching
    - HTTP response caching
  - Discussion/Comparison
    - Compare current solutions to the requirements + problem
    - State the problem of using the solutions (move as much of this to the respective technique)
    - Problems to be solved:
      - Potential consistency problem when cache takes a long time to be computed

- Cachable functions
  - Analysis (requirements => our solution)
    - of the requirements
      - How do we get easy invalidations for the programmer?
        - Automatic cache invalidation
        - Easy declarions/integration
      - How do we ensure correctness?
        - Ensuring consistency when values are updated
        - Tool for detecting dynamic dependencies.. (vs. automatic detecting)
    - of the cachable function
      - Analysis of the structure of dependencies
        => Dependencies between cached values and underlying data
      - Limitations
  - Design
    - Architecture and model
      - Figure showing the parts of the solution
        - Web Application:
          - Cachable function
        - Update Worker
        - Cache Database
        - Storage + Wrapper
        - Something about the caching architecture
          => Application-layer library, application-worker that updates values
        - Updater process
    - How does the cachable function look like by design?
    - How do we identify a cached value?
      => Key identifier/name
      => De-/Serialization
  - Implementation:
    - Describe decorators and how it is implemented in Python
    - SMache
    - Architecture of the solution

- Automatic Cache Invalidation
  - Analysis of the problem
    - How is it done in existing solutions (maybe just write it under existing solutions)
    - What is needed to solve the problem?
  - Design
    - Data structure
    - Information
    - Algorithm
  - Implementation
    - How is it declared/implemented
    - Redis for dependencies

- Data Update Propagation
  - Analysis of the problem
    - How is it solve in existing litterature?
    - What are the challenges related?
      - Consistency
      - Race Conditions
  - Design
    - Data structure
    - Information
    - Algorithm
  - Implementation
    - How is it implemented
    - Redis for dependencies

- Result
  - Describe how it is used
    - Demonstrations in code
    - Demonstrations of how it is used in Peergrade.io

- Testing/evaluation
  - Performance tests
    => Test that it works fast (Quality of Service)
  - Scalability tests
    => Show that it works with multiple workers
  - Efficiency tests
    => Test that computed values are not executed unnecesarily

- Discussion
  - How does it solve the problem?
  - Limitations
  - Further research/extensions
  - What could have been done better?

- Conclusion
  - ?
