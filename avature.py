import curl_cffi
import json
import os
import certifi
from urllib.parse import urlparse
from utils import *
from logger import setup_logger

logger = setup_logger("avature")

class CrawlerAvature:
    headers = {
        'Host': 'avature.net',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'pt-BR,pt;q=0.9'

    }

    def __init__(self, subdomain, proxies):
        self.PROXIES = proxies
        self.subdomain = subdomain

    def run(self):
        try:
            session = curl_cffi.Session()
            session.proxies = self.PROXIES

            self.headers['Host'] = self.subdomain
            jobs = []
            response_init = session.get(
                f'https://{self.subdomain}/careers/SearchJobs',
                #verify=certifi.where(),
                headers=self.headers,
                allow_redirects=True,
                timeout=10
            )

            jobs_per_page, total_items, pages_offset = detect_jobs_per_page_and_total_items(response_init.text)
        except Exception as e:
            logger.error(f"Error while fetching the main page: {e}") 
            return   

        
        logger.info(f'{total_items} of jobs finds - {self.subdomain}')
        for offset in pages_offset:
            logger.info(f'Fetching subdomain {self.subdomain} - {offset}')
            url_pagina = f'https://{self.subdomain}/careers/SearchJobs/?folderRecordsPerPage={jobs_per_page}&folderOffset={offset}&jobOffset={offset}'
            self.headers['Host'] = self.subdomain
            for _ in range(2):
                try:
                    response_page = session.get(
                        url_pagina,
                        verify=certifi.where(),
                        allow_redirects=False,
                        timeout=10
                    )

                    if response_page.headers.get('Location'):
                        response_page = session.get(
                            response_page.headers.get('Location'),
                            verify=certifi.where(),
                            allow_redirects=True,
                            timeout=10
                        )

                    links = get_links_jobs(response_page.text)
                    for link in links:
                        if self.headers['Host'] != urlparse(link).netloc:
                            self.subdomain = urlparse(link).netloc

                        self.headers['Host'] = urlparse(link).netloc
                        
                        response = session.get(link, headers=self.headers, verify=certifi.where(), timeout=10)
                        payload_job = parse_avature_job_detail(response.text)
                        payload_job['link'] = link
                        jobs.append(payload_job)             


                    break
                except Exception as e:
                    logger.error(f'Failed to fetch page <{url_pagina}>: {e}')

        
        return jobs