<img width="1901" height="794" alt="Screenshot 2026-01-02 180800" src="https://github.com/user-attachments/assets/43e46134-6e0d-438b-a712-0f2650ca0c8e" />
# Google Review Scraper (Python + Camoufox)

A professional-grade Google Review data extraction system built in Python for market research and business consulting use cases.

This project was developed as part of a client market research engagement for a business consultant, where large volumes of structured customer review data were required for analysis, benchmarking, and strategic decision-making.

## Project Use Case

*   **Market research and customer sentiment analysis**
*   **Competitor benchmarking across multiple businesses**
*   **Business intelligence and consulting reports**
*   **Automated collection of public review data**

## Key Features

### 📊 Business-Ready Data Output
*   Structured CSV files per target business
*   Incremental saving to prevent data loss
*   Ready for Excel, Google Sheets, Power BI, or Python analysis

### 🛡️ Stealth & Reliability
*   Uses **Camoufox** (stealth browser automation) to mimic real user behavior
*   Reduces CAPTCHA challenges and automated detection
*   Designed for long-running and large-scale scraping sessions

### 🔄 Dynamic Review Loading
*   Automatically handles dynamically loaded review content
*   Ensures full review coverage for businesses with high review volume

### 🍪 Session & Cookie Management
*   Supports loading session cookies to:
    *   Bypass consent and verification prompts
    *   Maintain authenticated sessions
    *   Improve scraping stability

### 🧾 Structured Data Extraction
Extracted fields include:
*   Business name and location
*   Reviewer name
*   Rating
*   Review date
*   Review text

### 📜 Logging & Monitoring
*   Integrated logging for progress tracking and debugging

## Technology Stack

*   **Python 3.8+**
*   **Camoufox** (Playwright-based stealth automation)
*   Playwright-compatible browser engines
*   CSV-based data pipelines

## Installation

1.  **Install dependencies**
    ```bash
    pip install camoufox
    ```

2.  **Install browser binaries**
    ```bash
    python -m camoufox fetch
    ```

## Configuration

### Input URLs (`input.txt`)
Add Google review listing URLs (one per line):
```text
https://www.google.com/...
https://www.google.com/...
```

### Cookies (`cookies.json`) – Recommended
Using session cookies improves stability and reduces interruptions.
1.  Log in to Google in a regular browser
2.  Export cookies for `.google.com`
3.  Save as `cookies.json` in the project directory

## Usage

Run the scraper:
```bash
python google_review_scraper.py
```

The browser launches (non-headless by default), loads reviews dynamically, and exports structured data automatically.

## Output

CSV files: `review_list_1.csv`, `review_list_2.csv`, ...
Each file corresponds to a URL from `input.txt`.
<img width="1896" height="950" alt="Screenshot 2026-01-02 181324" src="https://github.com/user-attachments/assets/151441f0-5b70-46c2-8ca1-83ff304b8fe8" />


## Professional Context

*   Built as part of a real client market research project
*   Client identity and proprietary data are intentionally excluded
*   Demonstrates real-world experience with:
    *   Stealth scraping
    *   Market research automation
    *   Reliable data extraction pipelines

## Disclaimer

This project is shared as previous professional experience.
Users are responsible for ensuring compliance with website Terms of Service and applicable regulations when using this code.
