import json
from urllib.parse import urlparse
from termcolor import colored

def extract_domains(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    results = {}
    
    for item in data:
        bucket_name = item.get('bucket', '')
        matches = item.get('matches', [])
        
        domains = set()
        for match in matches:
            url = match.split('[')[1].split(']')[0]
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.split(':')[0]
            domain = remove_subdomains(domain)
            domains.add(domain)
        
        results[bucket_name] = list(domains)
    
    return results

def remove_subdomains(domain):
    parts = domain.split('.')
    if len(parts) > 2:
        if len(parts[-1]) == 2:
            return '.'.join(parts[-3:])
        else:
            return '.'.join(parts[-2:])
    return domain

if __name__ == "__main__":
    json_file = "your_json_file.json"
    processed_data = extract_domains(json_file)
    
    for bucket, domains in processed_data.items():
        print(colored("Bucket:", 'blue'), colored(bucket, 'green'))
        for domain in domains:
            print(remove_subdomains(domain))
