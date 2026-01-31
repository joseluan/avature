import json
import os
from avature import CrawlerAvature
from concurrent.futures import ThreadPoolExecutor, as_completed

# TOR Proxy reset in 5 minutes
PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

SUBDOMAINS = json.load(open('subdomains_valids.json', 'r'))

def salvar_jobs(subdomain, jobs):
    with open(f'subdomain_jobs{os.sep}{subdomain}.json', 'w') as arq:
        arq.write(json.dumps(jobs, indent=4))


def run_subdomain(subdomain):
    try:
        crawler = CrawlerAvature(subdomain=subdomain, proxies=PROXIES)
        jobs = crawler.run()
        salvar_jobs(subdomain, jobs)
    except Exception as e:
        print(f'Erro in subdomain {subdomain}, {e}')
    
    return None




with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(run_subdomain, s) for s in SUBDOMAINS]

    for future in as_completed(futures):
        result = future.result()






