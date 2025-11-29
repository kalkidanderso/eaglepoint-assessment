# Task 2 – Async Data Fetcher with Retry (JavaScript)

Async/await function that calls a mock API and retries on failure.

## What it does

- Calls a function that simulates a network request.
- If it fails, waits 1 second and tries again.
- Gives up after `maxRetries` attempts and throws.
- Also includes a version with exponential backoff instead of a fixed delay.

## Run it

```bash
node async_fetcher.js
```

Logs attempts, successes, and failures to the console.

## Using `fetchWithRetry` from another file

```javascript
const { fetchWithRetry } = require('./async_fetcher');

(async () => {
  try {
    const data = await fetchWithRetry('https://api.example.com/data', 3);
    console.log(data);
  } catch (err) {
    console.error(err.message);
  }
})();
```

## More info

See `DOCUMENTATION.md` for how I built it, searches, etc.
