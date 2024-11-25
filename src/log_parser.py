import re
from collections import Counter
from typing import List, Tuple, Set
from dataclasses import dataclass

@dataclass
class LogEntry:
    ip_address: str
    timestamp: str
    request_method: str
    url: str
    protocol: str
    status_code: int
    response_size: int

class LogParser:
    # Regular expression for parsing log lines
    LOG_PATTERN = r'(?P<ip>[\d\.]+) - (?P<user>.*?) \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<url>.*?) (?P<protocol>.*?)" (?P<status>\d+) (?P<size>\d+)'
    
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.entries: List[LogEntry] = []
        
    def parse(self) -> None:
        """Parse the log file and store entries."""
        with open(self.log_file_path, 'r') as file:
            for line in file:
                match = re.match(self.LOG_PATTERN, line.strip())
                if match:
                    self.entries.append(LogEntry(
                        ip_address=match.group('ip'),
                        timestamp=match.group('timestamp'),
                        request_method=match.group('method'),
                        url=match.group('url'),
                        protocol=match.group('protocol'),
                        status_code=int(match.group('status')),
                        response_size=int(match.group('size'))
                    ))

        self.print_entries()
        
    def print_entries(self) -> None:
        """Print all log entries in a readable format."""
        print(f"Log Entries: {len(self.entries)}")
        print("============")
        for entry in self.entries:
            print(f"IP: {entry.ip_address}")
            print(f"Timestamp: {entry.timestamp}")
            print(f"Method: {entry.request_method}")
            print(f"URL: {entry.url}")
            print(f"Protocol: {entry.protocol}")
            print(f"Status: {entry.status_code}")
            print(f"Size: {entry.response_size}")
            print("-" * 50)

    def get_unique_ips(self) -> Set[str]:
        """Return set of unique IP addresses."""
        return {entry.ip_address for entry in self.entries}
    
    def get_top_urls(self, n: int = 3) -> List[Tuple[str, int]]:
        """Return top N most visited URLs."""
        url_counter = Counter(entry.url for entry in self.entries)
        return url_counter.most_common(n)
    
    def get_top_ips(self, n: int = 3) -> List[Tuple[str, int]]:
        """Return top N most active IP addresses."""
        ip_counter = Counter(entry.ip_address for entry in self.entries)
        return ip_counter.most_common(n) 