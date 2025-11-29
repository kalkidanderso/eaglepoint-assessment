# Task 2 - Async Data Fetcher with Retry (JavaScript) - Process Notes

Notes on how I approached this - searches, structure, etc.



## 1. What the task asked for (in my words)

- Function that fetches data from a URL
- Use async/await
- Retry on failure, up to maxRetries
- Wait 1 second between retries
- Throw if all attempts fail

PDF said we can mock the API so I simulated the network instead of hitting a real endpoint



## 2. Search log

Per the instructions, here are the searches I used (with terms and URLs where it made sense):

1. **Sleep with promises**  
   Search: `javascript sleep with promises setTimeout`  
   URL: https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
   - needed a clean way to wait between retries

2. **Async/await with fetch**  
   Search: `fetch async await example`  
   URL: https://stackoverflow.com/questions/67955033/async-await-with-fetch-js
   - quick refresher

3. **Retry patterns**  
Search: `javascript retry pattern async await loop vs recursion`  
   - ended up going with loop, easier to follow

4. **Exponential backoff**  
   Search: `exponential backoff javascript example`  
   - added this as an extra feature



## 3. Design decisions

- Simple for loop from 0 to maxRetries. `maxRetries + 1` total attempts
- Mock API with  around 60% success rate so retries actually get tested
- Input validation - fail fast if url is missing or maxRetries is negative
- Kept a `lastError` variable so the final error message is useful

Thought about doing it recursively but loops are easier to debug imo


## 4. Implementation

1. **sleep(ms)** - just wraps setTimeout in a promise

2. **mockApiCall(url)** - random delay 50-200ms, throws around 40% of the time

3. **fetchWithRetry(url, maxRetries)**
   - validate inputs
   - loop, try the call, if it fails wait 1s and retry
   - only sleep if theres another attempt coming (fixed a bug where i was sleeping after last failure too)
   - throw at the end with attempt count + last error

4. **fetchWithExponentialBackoff** - same thing but delay is 2 attempt seconds

5. **runTests()** - just runs a few scenarios and logs output. not real unit tests since the mock is random but shows the flow works



## 5. Issues I ran into

1. **Off by one thing** - had to decide if maxRetries=3 means 3 total or 3 extra. went with 1 initial + 3 retries = 4 total

2. **Unnecessary sleep** - was sleeping after final failure, moved it inside the `if (attempt < maxRetries)` check

3. **Success rate** - started with 50% but tests felt slow with all the retries. around to 60%


## 6. Why this works

- Easy to read - just a loop with try/catch
- Configurable retry count
- Good error messages
- Can swap mock for real fetch without changing retry logic

