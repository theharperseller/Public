# Public
Scripts to help anyone who may be interested

# Project: Web Crawler and File Saver

## Overview
This project consists of two key Python scripts:

1. **FileSaver**: A utility for saving content to files with advanced features such as automatic filename incrementation and customizable encoding.
2. **WebCrawler**: A script for recursively crawling websites, extracting text and titles, and saving the results to a JSON file using the FileSaver utility.

---

## Features
### FileSaver
- Saves content to a specified file.
- Automatically increments filenames if a conflict exists.
- Supports customizable encoding.
- Validates and ensures the save directory exists.

### WebCrawler
- Recursively crawls a website up to a user-defined depth.
- Extracts webpage titles and text.
- Periodically saves progress to avoid data loss.
- Uses the FileSaver script for consistent and reliable file saving.

---

## Usage

### FileSaver
Run the script directly using the command line:
```bash
python file_saver.py "Your content here" --directory /path/to/save --filename output.txt --encoding utf-8
```

#### Arguments
- `content` (required): The content to save in the file.
- `--directory` (optional): Directory to save the file. Defaults to the current directory.
- `--filename` (optional): Filename to use. Defaults to `output.txt`.
- `--encoding` (optional): Encoding to use for saving the file. Defaults to `utf-8`.

### WebCrawler
Run the script directly using the command line:
```bash
python web_crawler.py https://example.com --max_depth 3 --output results.json --verbose
```

#### Arguments
- `base_url` (required): The starting URL for crawling.
- `--max_depth` (optional): Maximum depth for crawling. Defaults to `2`.
- `--output` (optional): File to save the crawl results. Defaults to `crawl_results.json`.
- `--timeout` (optional): Timeout for HTTP requests (in seconds). Defaults to `10`.
- `--verbose` (optional): Enables detailed logging for debugging.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Requirements
- Python 3.7 or higher
- Libraries: `requests`, `beautifulsoup4`

---

## Example
### FileSaver
```bash
python file_saver.py "Hello, World!" --directory ./output --filename greeting.txt
```
### WebCrawler
```bash
python web_crawler.py https://example.com --max_depth 3 --output ./output/results.json
```

---

## File Structure
```
project-folder/
│
├── file_saver.py         # FileSaver script
├── web_crawler.py        # WebCrawler script
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

---

## Contribution
Contributions are welcome! Feel free to fork the repository, make updates, and submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

