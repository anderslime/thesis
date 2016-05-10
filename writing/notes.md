# Outline

- Introduction
  - Problem & Requirements
  - Peergrade.io
  - formal stuff

- Some theory: maybe same chapter, but different sections. Depends on length.
- Caching Architecture
- Caching model
  - Evaluating caching technique
    - Freshness
    - Consistency
    - Ease of management (invalidation)
    - Have to wait for computation?
  - Granularity

- Existing caching approaches
  - Invalidation techniques
    - Expiration based invalidation
    - Key-based invalidation
    - Trigger-based invalidation
    - Automatic invalidation
  - Updating the cache
    - Pull vs. push-based cache update
      - Pull:
        - Update the cache when value is requested
        - Return the latest computed value and update cache in background
      - Push:
        - Update the cache when underlying data changes + return latest computed value
    - Data update propagation
  - Caching techniques in web development
    - DB Query caching
      - Materialized views
      - ORM-query caching
    - HTTP response caching
  - Discussion/Comparison
    - Compare current solutions to the requirements + problem
    - State the problem of using the solutions (move as much of this to the respective technique)

- Cachable functions
  - Analysis (requirements => our solution)
    - of the requirements
      - How do we get easy invalidations for the developer?
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
