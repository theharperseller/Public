"""
Web Crawler Script

Author: Avery Harper
Date: January 26, 2025
Description: A web crawler that recursively crawls a website, extracts text and titles, 
             and saves the results to a JSON file. It uses the FileSaver class for saving progress.

Requirements:
- Python 3.7 or higher
- `requests` library
- `beautifulsoup4` library
- `file_saver.py` module in the same directory

Usage:
Run this script directly using the command line:
    python web_crawler.py <base_url> [--max_depth <int>] [--output <path>] [--timeout <int>] [--verbose]

Example:
    python web_crawler.py "https://example.com" --max_depth 3 --output "results.json"

Features:
- Logs progress and errors
- Periodically saves progress every 10 results
- Supports configurable crawl depth, timeouts, and logging verbosity
"""


import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import logging
from typing import Optional
import os
from file_saver import FileSaver  # Import FileSaver

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebCrawler:
    def __init__(self, base_url: str, output_file: str):
        self.base_url = base_url
        self.visited_urls = set()
        self.results = []
        self.output_file = output_file

    def crawl(self, url: str, max_depth: int = 2, current_depth: int = 0) -> None:
        if current_depth > max_depth or url in self.visited_urls:
            return

        logging.info(f"Crawling URL: {url} (Depth: {current_depth}/{max_depth})")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return

        if "text/html" not in response.headers.get("Content-Type", ""):
            logging.warning(f"Skipping non-HTML content at {url}")
            return

        self.visited_urls.add(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "No Title"
        text = soup.get_text(separator='\n').strip()
        self.results.append({
            "Title": title,
            "URL": url,
            "ExtractedText": text
        })

        # Save progress periodically
        if len(self.results) % 10 == 0:  # Save every 10 entries
            self._save_progress()

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            if not self._is_valid_url(full_url):
                logging.warning(f"Skipping URL not matching base domain or already visited: {full_url}")
                continue
            self.crawl(full_url, max_depth, current_depth + 1)

    def _is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.netloc == urlparse(self.base_url).netloc and url not in self.visited_urls

    def get_results_as_json(self) -> str:
        return json.dumps(self.results, ensure_ascii=False, indent=4)

    def _save_progress(self):
        """Save the current progress to the output file using FileSaver."""
        try:
            FileSaver.save(self.get_results_as_json(), filename=self.output_file)
            logging.info(f"Progress saved to {self.output_file}")
        except Exception as e:
            logging.error(f"Failed to save progress: {e}")

if __name__ == "__main__":
    import argparse
    import sys

    print(f"Simulated sys.argv: {sys.argv}")

    # Simulate command-line arguments for testing or interactive environments
    if len(sys.argv) <= 1 or "ipykernel_launcher.py" in sys.argv[0]:
        logging.warning("No arguments provided. Using simulated arguments for testing.")
        sys.argv = ["web_crawler.py", "https://example.com", "--max_depth", "3", "--output", "results.json"]

    parser = argparse.ArgumentParser(description="A simple web crawler.")
    parser.add_argument("base_url", type=str, help="The base URL to start crawling from.")
    parser.add_argument("--max_depth", type=int, help="The maximum depth to crawl.", default=2)
    parser.add_argument("--output", type=str, help="The file to save the crawl results.", default="crawl_results.json")
    parser.add_argument("--timeout", type=int, help="Timeout for HTTP requests (seconds).", default=10)
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logging.")

    args = parser.parse_args()

    # Adjust logging level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate max_depth
    if args.max_depth < 1:
        logging.error("Invalid max_depth. It must be a positive integer.")
        sys.exit(1)

    # Validate output directory
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Created directory for output: {output_dir}")

    crawler = WebCrawler(args.base_url, args.output)
    logging.info(f"Starting crawl at {args.base_url} with max depth {args.max_depth}...")

    try:
        crawler.crawl(args.base_url, max_depth=args.max_depth)
        json_content = crawler.get_results_as_json()

        # Save final results to file using FileSaver
        FileSaver.save(json_content, filename=args.output)

        logging.info(f"Crawl results saved to {args.output}")
    except Exception as e:
        logging.error(f"An error occurred during the crawl: {e}")
