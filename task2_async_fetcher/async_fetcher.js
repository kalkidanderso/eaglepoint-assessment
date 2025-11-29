// simple sleep helper
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// mock api - randomly succeeds/fails
async function mockApiCall(url) {
    await sleep(Math.random() * 150 + 50); // fake network delay

    if (Math.random() > 0.4) {
        return {
            success: true,
            data: `Data from ${url}`,
            timestamp: new Date().toISOString(),
        };
    }
    throw new Error(`Network error: Failed to fetch ${url}`);
}

// fetch with retry - waits 1sec between attempts
async function fetchWithRetry(url, maxRetries = 3) {
    if (!url || typeof url !== 'string') {
        throw new Error('Invalid URL provided');
    }

    let lastError;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            console.log(`Attempt ${attempt + 1}/${maxRetries + 1}: Fetching ${url}...`);
            const data = await mockApiCall(url);
            console.log(`Success on attempt ${attempt + 1}`);
            return data;
        } catch (error) {
            lastError = error;
            console.log(`Attempt ${attempt + 1} failed: ${error.message}`);

            if (attempt < maxRetries) {
                console.log('Waiting 1 second...');
                await sleep(1000);
            }
        }
    }

    throw new Error(`Failed to fetch ${url} after ${maxRetries + 1} attempts. Last error: ${lastError.message}`);
}

// same thing but with exponential backoff (1s, 2s, 4s, etc)
async function fetchWithExponentialBackoff(url, maxRetries = 3) {
    if (!url || typeof url !== 'string') {
        throw new Error('Invalid URL provided');
    }

    let lastError;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            console.log(`[Backoff] Attempt ${attempt + 1}/${maxRetries + 1}: ${url}`);
            const data = await mockApiCall(url);
            console.log(`[Backoff] Success on attempt ${attempt + 1}`);
            return data;
        } catch (error) {
            lastError = error;
            console.log(`[Backoff] Attempt ${attempt + 1} failed`);

            if (attempt < maxRetries) {
                const waitTime = Math.pow(2, attempt) * 1000;
                console.log(`[Backoff] Waiting ${waitTime / 1000}s...`);
                await sleep(waitTime);
            }
        }
    }

    throw new Error(`Failed to fetch ${url} after ${maxRetries + 1} attempts. Last error: ${lastError.message}`);
}

// quick tests
async function runTests() {
    console.log('=== ASYNC FETCHER TESTS ===\n');

    console.log('Test 1: Basic retry (max 3)');
    try {
        const result = await fetchWithRetry('https://api.example.com/data', 3);
        console.log('Result:', result);
    } catch (error) {
        console.log('Error:', error.message);
    }

    console.log('\nTest 2: More retries (5)');
    try {
        const result = await fetchWithRetry('https://api.example.com/users', 5);
        console.log('Result:', result);
    } catch (error) {
        console.log('Error:', error.message);
    }

    console.log('\nTest 3: No retries');
    try {
        const result = await fetchWithRetry('https://api.example.com/quick', 0);
        console.log('Result:', result);
    } catch (error) {
        console.log('Error:', error.message);
    }

    console.log('\nTest 4: Exponential backoff');
    try {
        const result = await fetchWithExponentialBackoff('https://api.example.com/backoff', 3);
        console.log('Result:', result);
    } catch (error) {
        console.log('Error:', error.message);
    }

    console.log('\nTest 5: Invalid input');
    try {
        await fetchWithRetry('', 3);
    } catch (error) {
        console.log('Expected error:', error.message);
    }

    console.log('\nDone.');
}

if (require.main === module) {
    runTests().catch(console.error);
}

module.exports = { fetchWithRetry, fetchWithExponentialBackoff, mockApiCall, sleep };