# Log File Analyzer

A Python application that analyzes HTTP request logs to extract useful statistics.

## Features

- Count unique IP addresses
- Identify top 3 most visited URLs
- Identify top 3 most active IP addresses

## Requirements

- Python 3.7+
- No external dependencies required

## Installation

1. Clone the repository: 
```
git clone https://github.com/yourusername/log-analyzer.git
cd log-analyzer
```

2. Run the application:
```
python main.py
```

3. Run the tests:
```
python -m unittest discover tests
```

## Assumptions

- Log file format follows the standard Apache/Nginx log format
- Log entries are well-formed and match the expected pattern
- The log file is small enough to fit in memory
- UTF-8 encoding for log files

## Future Improvements

- Add support for different log formats
- Implement streaming processing for large files
- Add more statistical analysis options
- Add CLI arguments for customization