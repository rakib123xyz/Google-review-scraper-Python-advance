# Google Review Scraper

A robust Python-based tool designed to scrape reviews from Google Maps listings. This project utilizes **Camoufox** (a stealthy wrapper for Playwright) to provide **Advanced Stealth Scraping** capabilities, evade bot detection, manage browser fingerprints, and handle dynamic content loading effectively.

## Features

*   **Advanced Stealth & CAPTCHA Bypass**: Uses `Camoufox` to automatically manage browser fingerprints, user agents, and headers to mimic real user behavior, significantly reducing the risk of blocks and CAPTCHAs.
*   **Infinite Scrolling**: Automatically handles scroll events to load all reviews for a listing.
*   **Cookie Management**: Supports loading `cookies.json` to maintain sessions or bypass initial consent popups.
*   **Data Extraction**: Extracts key details including:
    *   Dealer/Business Name
    *   Location
    *   Reviewer Name
    *   Rating
    *   Date
    *   Review Text
*   **CSV Export**: Saves data incrementally to CSV files to prevent data loss.
*   **Logging**: Integrated logging for tracking progress and debugging.

## Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package manager)

## Installation

1.  **Clone the repository** (if applicable) or download the source code.

2.  **Install dependencies**:
    This project relies on `camoufox`.

    ```bash
    pip install camoufox
    ```

3.  **Install Browser Binaries**:
    Camoufox requires specific browser binaries to function.

    ```bash
    python -m camoufox fetch
    ```

## Configuration

Before running the scraper, you need to set up the input files in the `Scraper` directory.

### 1. Input URLs (`input.txt`)
Create a file named `input.txt` in the same directory as the script. Add the Google Maps URLs you wish to scrape, one per line.

Example:
```text
https://www.google.com/maps/place/Some+Business+Name/...
https://www.google.com/maps/place/Another+Business/...
```

### 2. Cookies (`cookies.json`)
To avoid CAPTCHAs or login prompts, it is recommended to use valid session cookies.
1.  Log in to Google in your regular browser.
2.  Use a browser extension (like "EditThisCookie" or "Cookie-Editor") to export cookies for `.google.com`.
3.  Save the exported JSON content as `cookies.json` in the script directory.

## Usage

Navigate to the directory containing the script and run it:

```bash
cd Scraper
python google_review_scraper.py
```

The script will launch a browser (non-headless by default), navigate to the URLs, scroll through reviews, and save the data.

## Output

The script generates CSV files named `review_list_1.csv`, `review_list_2.csv`, etc., corresponding to the order of URLs in `input.txt`.

## Disclaimer

This tool is for educational purposes only. scraping data from websites should be done in accordance with the website's Terms of Service and `robots.txt` policy.