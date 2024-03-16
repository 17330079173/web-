import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from concurrent.futures import ThreadPoolExecutor
import argparse

visited_urls = set()

print("""

 .------..------..------.
|L.--. ||Y.--. ||G.--. |
| :/\: || (\/) || :/\: |
| (__) || :\/: || :\/: |
| '--'L|| '--'Y|| '--'G|
`------'`------'`------'
                                            
      [+] Fusion---VSion_2.0版本\n
      [+] phone:MTczMzAwNzkxNzM=    
      [+]python info.py -u <目标> || python info.py -r <文件>\n
      [-] 无限遍历获取所有信息，并且拥有高并发功能，让成果丝滑顺畅\n


""")


def collect_urls(url):
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        response = requests.get(url)
        print(f"******目标URL地址为: {url}, ******响应状态码为: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # 解析HTML源码中的URL
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if next_url.startswith('http') and next_url not in visited_urls:
                    collect_urls(next_url)

            # 解析JS文件中的地址
            js_links = re.findall(r'\\\\"https?://[^\\\\s\\\\"]+\\\\"', response.text)
            for js_link in js_links:
                js_link = js_link.strip('\\\\"')
                if js_link not in visited_urls:
                    collect_urls(js_link)

            # 解析数据包的URL
            for link in soup.find_all('a', href=True):
                file_url = urljoin(url, link['href'])
                if file_url.endswith('.zip') or file_url.endswith('.rar') or file_url.endswith('.exe'):
                    print(f"File URL: {file_url}")

            for link in soup.find_all('html',href=True):
                file_url = urljoin(url, link['html'])
                if file_url.endswith('.txt')or file_url.endswith('.html'):
                    print(f"File URL: {file_url}")
                else:
                    break

            for link in soup.find_all('img', href=True):
                file_url = urljoin(url, link['src'])
                if file_url.endswith('.jpg') or file_url.endswith('.icon') or file_url.endswith('.png'):
                    print(f"File URL: {file_url}")
                else:
                    break

    except Exception as e:
        print(f"Error accessing URL: {url}, {e}")


def main():
    parser = argparse.ArgumentParser(description='URL Collector with concurrency')
    parser.add_argument('-u', '--url', type=str, help='Target URL to start collecting from')
    parser.add_argument('-r', '--repeat', type=int, default=1, help='Number of times to repeat collection')
    args = parser.parse_args()

    if not args.url:
        parser.error('Please provide a target URL using -u or --url')

    start_url = args.url

    for _ in range(args.repeat):
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.submit(collect_urls, start_url)


if __name__ == '__main__':
    main()



