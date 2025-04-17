# VacancyMail Web Scraper
======================

A Python script that scrapes job listings from VacancyMail.co.zw and saves them to a CSV file. The script includes robust error handling, logging, and scheduled execution capabilities.

## Features
--------

* Daily scheduled scraping at 10:30 AM
* Comprehensive error handling for web requests and parsing
* Detailed logging system
* CSV output with job details
* Emoji-based status indicators
* Custom exception handling

## Setup Instructions
-------------------

### Prerequisites

* Python 3.7+
* Required packages:
  * `requests`
  * `beautifulsoup4`
  * `schedule`
  * `python-dateutil`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/vacancymail-scraper.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
-----

### Manual Run

To run the scraper manually:
```bash
python scraper.py
```

### Scheduled Run

The script is configured to run automatically at 10:30 AM daily. To start the scheduler:
```bash
python scraper.py
```

Press `Ctrl+C` to stop the scheduler.

## Configuration
-------------

### Logging

The script logs all events to `scraping.log` with the following format:
```text
'%(asctime)s - %(levelname)s - %(message)s'
```

### Error Handling

The script handles several types of errors:
* Web request timeouts (15-second timeout)
* Connection errors
* Parsing errors
* CSV writing errors
* Scheduler errors

Each error is logged with appropriate details and emoji indicators.

## Output
--------

The script generates a CSV file named `scraped_jobs.csv` containing:
* Job Title
* Company
* Location
* Expiry Date
* Job Description

The CSV file is updated daily with the latest job listings.

## Contributing
------------

Contributions are welcome! Please submit pull requests with:
1. Clear commit messages
2. Updated documentation
3. Additional test cases (if applicable)

## License
------

Copyright (c) 2025 Tinashe Wutete

