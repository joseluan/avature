# Avature Job Scraper (with TOR)

A crawler to collect job listings from **Avature ATS** based portals, using **TOR (SOCKS5)** for anonymization and IP rotation.

## Features
- Automatically detects total jobs and pagination
- Extracts title, description, metadata and application link
- Supports multiple subdomains
- Parallel execution
- TOR IP rotation

## Project Structure
.
├── main.py
├── avature.py
├── utils.py
├── tor_proxy.py
├── merge_jobs.py
├── subdomains_valids.json
├── subdomain_jobs/
└── requirements.txt

## Installation
pip install -r requirements.txt

## Dependencies
beautifulsoup4  
curl-cffi  
certifi  
requests  
stem  
PySocks  

## Run TOR
python tor_proxy.py

## Run the crawler
python main.py

## Output
The crawler generates one JSON file per subdomain inside the `subdomain_jobs/` directory:

subdomain_jobs/
  ├── amerilife.avature.net.json
  ├── oracle.avature.net.json
  └── ...

Each file contains a list of job objects extracted from that subdomain.

## Merging all jobs into a single file
The project includes a helper script called `merge_jobs.py` that merges all individual files into a single file named `jobs.json`.

Run:
python merge_jobs.py

This will generate:
jobs.json

containing all jobs from all subdomains in one unified dataset.

## Legal Notice
This project is intended for educational and research purposes only. You are responsible for complying with the terms of service of the scraped websites and local laws.
