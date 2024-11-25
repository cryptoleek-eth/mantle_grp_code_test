from src.log_analyzer import LogAnalyzer

def main():
    log_file = "programming-task-example-data.log"
    analyzer = LogAnalyzer(log_file)
    result = analyzer.analyze()
    
    print("\nLog Analysis Results")
    print("===================")
    print(f"\nNumber of unique IP addresses: {result.unique_ip_count}")
    
    print("\nTop 3 most visited URLs:")
    for url, count in result.top_urls:
        print(f"- {url}: {count} visits")
    
    print("\nTop 3 most active IP addresses:")
    for ip, count in result.top_ips:
        print(f"- {ip}: {count} requests")

if __name__ == "__main__":
    main() 