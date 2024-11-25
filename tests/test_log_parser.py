import unittest
import re
from pathlib import Path
from src.log_parser import LogParser, LogEntry
from src.log_analyzer import LogAnalyzer, LogAnalysisResult
from collections import Counter

class TestLogParser(unittest.TestCase):
    def setUp(self):
        self.log_file = "programming-task-example-data.log"
        self.parser = LogParser(self.log_file)
        self.parser.parse()

    def test_log_entry_creation(self):
        """Test if LogEntry objects are created correctly"""
        entry = self.parser.entries[0]
        self.assertIsInstance(entry, LogEntry)
        self.assertTrue(hasattr(entry, 'ip_address'))
        self.assertTrue(hasattr(entry, 'timestamp'))
        self.assertTrue(hasattr(entry, 'request_method'))
        self.assertTrue(hasattr(entry, 'url'))
        self.assertTrue(hasattr(entry, 'protocol'))
        self.assertTrue(hasattr(entry, 'status_code'))
        self.assertTrue(hasattr(entry, 'response_size'))

    def test_parse_valid_line(self):
        """Test parsing of a valid log line"""
        test_line = '177.71.128.21 - - [10/Jul/2018:22:21:28 +0200] "GET /intranet-analytics/ HTTP/1.1" 200 3574'
        pattern = re.compile(LogParser.LOG_PATTERN)
        match = pattern.match(test_line)
        self.assertIsNotNone(match)
        
        # Test specific fields
        self.assertEqual(match.group('ip'), '177.71.128.21')
        self.assertEqual(match.group('method'), 'GET')
        self.assertEqual(match.group('url'), '/intranet-analytics/')
        self.assertEqual(match.group('status'), '200')

    def test_unique_ips(self):
        """Test unique IP address extraction"""
        unique_ips = self.parser.get_unique_ips()
        self.assertIsInstance(unique_ips, set)
        self.assertTrue(len(unique_ips) > 0)
        
        # Verify that IPs are unique
        ip_list = [entry.ip_address for entry in self.parser.entries]
        self.assertEqual(len(unique_ips), len(set(ip_list)))

    def test_top_urls_count(self):
        """Test top URLs counting"""
        top_urls = self.parser.get_top_urls(3)
        self.assertEqual(len(top_urls), 3)
        
        # Verify ordering
        counts = [count for url, count in top_urls]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_top_urls_custom_limit(self):
        """Test top URLs with different limits"""
        for n in [1, 2, 5]:
            top_urls = self.parser.get_top_urls(n)
            self.assertEqual(len(top_urls), min(n, len(self.parser.entries)))

    def test_top_ips_count(self):
        """Test top IPs counting"""
        top_ips = self.parser.get_top_ips(3)
        self.assertEqual(len(top_ips), 3)
        
        # Verify ordering
        counts = [count for ip, count in top_ips]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_top_ips_accuracy(self):
        """Test accuracy of IP counting"""
        ip_counts = Counter(entry.ip_address for entry in self.parser.entries)
        top_ips = self.parser.get_top_ips(1)
        self.assertEqual(top_ips[0][1], max(ip_counts.values()))

    def test_http_methods(self):
        """Test HTTP methods in log entries"""
        methods = {entry.request_method for entry in self.parser.entries}
        self.assertTrue(all(method in ['GET', 'POST', 'PUT', 'DELETE'] for method in methods))

    def test_status_codes(self):
        """Test status codes in log entries"""
        status_codes = {entry.status_code for entry in self.parser.entries}
        self.assertTrue(all(isinstance(code, int) for code in status_codes))
        self.assertTrue(all(100 <= code <= 599 for code in status_codes))

class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.log_file = "programming-task-example-data.log"
        self.analyzer = LogAnalyzer(self.log_file)

    def test_analyze_result_structure(self):
        """Test the structure of analysis results"""
        result = self.analyzer.analyze()
        self.assertIsInstance(result, LogAnalysisResult)
        self.assertIsInstance(result.unique_ip_count, int)
        self.assertIsInstance(result.top_urls, list)
        self.assertIsInstance(result.top_ips, list)

    def test_analyze_content(self):
        """Test the content of analysis results"""
        result = self.analyzer.analyze()
        self.assertTrue(result.unique_ip_count > 0)
        self.assertEqual(len(result.top_urls), 3)
        self.assertEqual(len(result.top_ips), 3)

    def test_result_consistency(self):
        """Test consistency of multiple analyses"""
        result1 = self.analyzer.analyze()
        
        # Create a new analyzer instance to ensure fresh parsing
        analyzer2 = LogAnalyzer(self.log_file)
        result2 = analyzer2.analyze()
        
        self.assertEqual(result1.unique_ip_count, result2.unique_ip_count)
        # Compare only the URLs, not their counts
        self.assertEqual(
            [url for url, _ in result1.top_urls],
            [url for url, _ in result2.top_urls]
        )
        # Compare only the IPs, not their counts
        self.assertEqual(
            [ip for ip, _ in result1.top_ips],
            [ip for ip, _ in result2.top_ips]
        )

class TestEdgeCases(unittest.TestCase):
    def test_empty_file(self):
        """Test handling of empty log file"""
        # Create temporary empty file
        with open('empty.log', 'w') as f:
            pass
        
        parser = LogParser('empty.log')
        parser.parse()
        self.assertEqual(len(parser.entries), 0)
        self.assertEqual(len(parser.get_unique_ips()), 0)
        self.assertEqual(len(parser.get_top_urls()), 0)
        self.assertEqual(len(parser.get_top_ips()), 0)
        
        # Cleanup
        Path('empty.log').unlink()

    def test_malformed_lines(self):
        """Test handling of malformed log lines"""
        # Create temporary file with malformed lines
        test_data = """
        invalid line
        177.71.128.21 - - [10/Jul/2018:22:21:28 +0200] "GET /intranet-analytics/ HTTP/1.1" 200 3574
        another invalid line
        """
        with open('malformed.log', 'w') as f:
            f.write(test_data)
        
        parser = LogParser('malformed.log')
        parser.parse()
        self.assertEqual(len(parser.entries), 1)  # Only valid line should be parsed
        
        # Cleanup
        Path('malformed.log').unlink()

if __name__ == '__main__':
    unittest.main() 