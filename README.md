# EaglePoint AI Technical Assessment

This folder contains my work for the EaglePoint AI Full‑stack Developer technical assessment. I decided to complete all three of the suggested tasks (the email says minimum 2 are required).

## Project structure

```text
.
├── task1_text_analyzer/
│   ├── text_analyzer.py
│   ├── DOCUMENTATION.md
│   └── README.md
│
├── task2_async_fetcher/
│   ├── async_fetcher.js
│   ├── DOCUMENTATION.md
│   └── README.md
│
├── task3_rate_limiter/
│   ├── rate_limiter.py
│   ├── DOCUMENTATION.md
│   └── README.md
│
└── README.md  (this file)
```

Each task folder has:
- the main implementation file,
- a short `README.md` explaining how to run it,
- and `DOCUMENTATION.md` with my process notes (searches, decisions, and issues I ran into).

## Tasks

### Task 1 -  Smart Text Analyzer (Python)

- Simple text analysis helper that returns:
  - word count
  - average word length (2 decimals)
  - list of longest word(s)
  - case‑insensitive word frequencies
- Implemented in plain Python, no external libraries.
- To try it quickly:

```bash
cd task1_text_analyzer
python3 text_analyzer.py
```


### Task 2 - Async data fetcher with retry (JavaScript)

- Async/await‑based function that:
  - calls a mock API,
  - retries on failure up to a configurable number of times,
  - waits 1 second between retries.
- There is also a version with exponential backoff.
- To run the demo/tests:

```bash
cd task2_async_fetcher
node async_fetcher.js
```


### Task 3 - Rate limiter (Python)

- In‑memory rate limiter with a sliding window per user.
- Default: 5 requests per 60 seconds for each `user_id`.
- Includes a small demo and some basic tests.
- To run:

```bash
cd task3_rate_limiter
python3 rate_limiter.py
```


## Notes on documentation

The assessment email asks to document:
- searches and links,
- thought process and alternatives,
- step‑by‑step how the solution was built.

For each task I put that information in the corresponding `DOCUMENTATION.md` file, written more like working notes than a formal report.
