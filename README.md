# Page Pulse

Page Pulse is a lightweight full-stack website health auditing tool built with React and FastAPI.

A user enters a public webpage URL and Page Pulse fetches the page, analyzes its HTML, and displays basic technical, SEO, and accessibility information in a responsive dashboard.

## Features

Page Pulse reports:

- HTTP status code
- Response time
- Page title
- Meta description
- H1 count
- Images with missing or empty alt text
- Approximate visible word count

It also includes:

- URL validation
- Basic protection against private/local network URLs
- Request timeout handling
- Non-HTML response handling
- Loading and error states
- Responsive React interface
- Automated parser tests

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- HTTPX
- BeautifulSoup
- Pydantic

### Testing

- Pytest

## Project Structure

```text
page-pulse/
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── fetcher.py
│   │   │   └── parser.py
│   │   ├── utils/
│   │   │   └── validators.py
│   │   ├── main.py
│   │   └── models.py
│   ├── tests/
│   │   └── test_parser.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AuditForm.jsx
│   │   │   └── AuditResults.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── .env.example
│   └── package.json
│
├── .gitignore
└── README.md
```

## How It Works

The application follows this flow:

```text
User enters URL
       |
       v
React Frontend
       |
       | POST /api/audit
       v
FastAPI Backend
       |
       v
URL Validation
       |
       v
HTTPX Fetcher
       |
       v
External Website
       |
       | HTML response
       v
BeautifulSoup Parser
       |
       v
Audit Results
       |
       v
React Dashboard
```

The frontend sends the URL to the FastAPI backend.

The backend validates the URL, fetches the remote page using HTTPX, measures the response time, and passes the returned HTML to the parser.

BeautifulSoup extracts the required page information, and FastAPI returns the final report as JSON.

## API

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Audit a Page

```http
POST /api/audit
```

Request:

```json
{
  "url": "https://example.com"
}
```

Example response:

```json
{
  "url": "https://example.com",
  "http_status": 200,
  "response_time_ms": 500,
  "title": "Example Domain",
  "meta_description": null,
  "h1_count": 1,
  "images_missing_alt": 0,
  "word_count": 21
}
```

## Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd page-pulse
```

### 2. Backend Setup

Move into the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Create `.env` from `.env.example` and configure:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start Vite:

```bash
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

## Running Tests

From the backend directory:

```bash
python -m pytest -v
```

The parser tests cover:

- Standard metadata extraction
- Missing title and meta description
- Multiple H1 elements
- Missing and empty image alt attributes
- Word counting while excluding script and style content

## Error Handling

Page Pulse handles several failure cases.

- Invalid URLs are rejected through request validation.
- Private and local network destinations are blocked by basic URL safety validation.
- Request timeouts return a controlled error.
- Network failures return a controlled error.
- Non-HTML responses are rejected because the parser is intended for webpages.
- Unexpected backend failures return a generic server error instead of exposing internal details.

## Assumptions and Limitations

Page Pulse is intentionally a lightweight webpage auditing tool rather than a complete SEO crawler.

The analysis is based on the HTML returned to the backend HTTP client. It does not execute client-side JavaScript.

As a result, JavaScript-heavy websites may expose less content to Page Pulse than they display in a normal browser.

Websites using anti-bot or challenge systems may return responses such as HTTP 403. Page Pulse reports the response it actually receives rather than attempting to bypass those protections.

Word count is approximate and is based on parsed page text after removing script, style, and noscript elements.

The application includes basic protection against direct private/local network URLs. A production-grade public crawler would require additional SSRF protections, including validation of every redirect target.

## Production Improvements

With more time, I would add:

- Redirect-by-redirect SSRF validation
- Maximum response/download size limits
- More comprehensive API tests using mocked HTTP requests
- Rate limiting
- Structured logging
- Caching
- Expanded SEO checks
- Accessibility checks
- CI/CD
- Monitoring

## Task

Built for Digital Heroes Training Task.