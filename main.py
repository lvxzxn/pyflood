import requests
import threading
import random
import argparse
from fake_useragent import UserAgent

ua = UserAgent()

def scrape_proxies():
  apis = {
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt'
  }

def get_host(hostname: str, proxy: str):
    if 'http://' in proxy:
        proxies = {'http': proxy.strip()}
        headers = {'User-Agent': ua.random}
        host = proxy.replace('http://', '').strip()
        ip = host.split(':')[0].strip()
        port = host.split(':')[1].strip()
        try:
            r = requests.get(hostname, headers=headers, proxies=proxies)
            if r.text:
                print(f'[{ip}:{port}] | {hostname} - success!')
            else:
                return
        except requests.RequestException as e:
            print(f'[{ip}:{port}] | {hostname} - failed: {e}')
            return

def load_proxies_and_get(host: str, proxies_file_path: str):
    while True:
        try:
            with open(proxies_file_path, 'r') as proxies_file:
                lines = proxies_file.readlines()
            
            threads = []
            num_threads = len(lines)
            
            for _ in range(num_threads):
                random_proxy = random.choice(lines)
                thread = threading.Thread(target=get_host, args=(host, random_proxy))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check proxies with a given host.')
    parser.add_argument('host', type=str, help='The URL of the host to check.')
    parser.add_argument('proxies_file', type=str, help='Path to the file containing the list of proxies.')
    
    args = parser.parse_args()
    
    load_proxies_and_get(args.host, args.proxies_file)
