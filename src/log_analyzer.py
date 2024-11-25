from dataclasses import dataclass
from typing import List, Tuple, Set
from .log_parser import LogParser

@dataclass
class LogAnalysisResult:
    unique_ip_count: int
    top_urls: List[Tuple[str, int]]
    top_ips: List[Tuple[str, int]]

class LogAnalyzer:
    def __init__(self, log_file_path: str):
        self.parser = LogParser(log_file_path)
    
    def analyze(self) -> LogAnalysisResult:
        """Perform analysis on the log file."""
        self.parser.parse()
        
        return LogAnalysisResult(
            unique_ip_count=len(self.parser.get_unique_ips()),
            top_urls=self.parser.get_top_urls(),
            top_ips=self.parser.get_top_ips()
        ) 