import requests
import threading
import random
import argparse
from fake_useragent import UserAgent

ua = UserAgent()

def scrape_proxies(file_path: str):
    apis = [
        'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt'
    ]
    
    with open(file_path, 'w') as file:
        for host in apis:
            try:
                req = requests.get(host)
                content = req.text
                file.write(f'{content.strip()}\n')
            except requests.RequestException as e:
                print(f"Failed to fetch proxies from {host}: {e}")

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
    parser.add_argument('host', type=str, nargs='?', help='The URL of the host to check.')
    parser.add_argument('proxies_file', type=str, nargs='?', help='Path to the file containing the list of proxies.')
    parser.add_argument('--update', action='store_true', help='Update the list of proxies from the external sources.')

    args = parser.parse_args()

    if args.update:
        if args.host or args.proxies_file:
            print("Cannot use --update with host or proxies_file arguments.")
        else:
            scrape_proxies('./http.txt')
            print(f"Proxies updated and saved to ./http.txt")
    else:
        if not args.host or not args.proxies_file:
            parser.print_help()
            print("Error: --host and --proxies_file are required if not updating proxies.")
        else:
            load_proxies_and_get(args.host, args.proxies_file)
