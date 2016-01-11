# Caching

## From: A Survey of Web Caching Schemes for the Internet

### Elements of caching

* Caching System Architecture: how are proxies organized? hierarchically? distribued? hybrid?
* Proxy Placement: geographical placement?
* Caching Content: data? connections? computations?
* Proxy Cooperation
* Data Sharing: what data can be shared among proxies?
* Caching Resolution/Routing: how does a proxy decide where to fetch page requested by client?
* Prefetching: how can a proxy decide how/what to prefetch?
* Cache Placement/Replacemnt: storage
* Data Consistency
* Control Information Distribution
* Dynamic Data Caching

### Desireable Properties

* fast access (latency)
* robustness (availability, fault-tolerance on crashes, fault recovery)
* transparency
* scalability
* efficiency (overhead on network,
* adaptivity
* stability
* load balanced
* ability to deal with heterogeneity
* simplicity


## From: IBM Caching Slides

### Considerations

* What, when and where to cache
* Granularity: SQL query result, HTML-fragment, HTML-document, data processing results...
* Invalidation Policies: transparency, push vs pull, freshness maintenance,
* Exploitation: routing, failover, accounting, authentication, authorization
* Tools: performance monitoring, analysis

## From: Web Caching and Its Applications

### Cache Coherence

* Strong Cache Consistency: always check for freshness
  * Only to be able to save bandwidth - you save transfering the object
  * If-Modified-Since, ETag
* Weak Cache Consistency: you need not to check origin for freshness every time
  * Can server stale object, so consistency is not ensured
  * TTL (HTTP: Cache-Control)
  * Piggybag: fetches list of documents updates since date
