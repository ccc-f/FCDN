import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from cdnCheck import cdn_check
import argparse
import os

def ThreadPool(func,urls,max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        to_do = []
        for url in urls:
            obj = executor.submit(func, url)
            to_do.append(obj)
    for future in concurrent.futures.as_completed(to_do):
        result, domain = future.result()
        if not os.path.exists('./result/'):
            os.mkdir('./result/')
        if result is False:
            savefile('./result/nocdnResult.txt',domain)
        elif result is True:
            savefile('./result/cdnResult.txt',domain)
        else:
            savefile('./result/errorResult.txt',domain)
        
def savefile(filename, data):
    with open(filename, 'a', encoding='utf-8')as f:
        f.write(data + '\n')

def readfile(filename):
    urls = []
    with open(filename,'r',encoding='utf-8')as f:
        data = f.read()
    urls = data.strip().split()
    return urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='by Scrboy.')
    parser.add_argument('-f', '--file', type=str, default='domain.txt')
    parser.add_argument('-t', '--thread',type=int, default=50)
    args = parser.parse_args()
    domain = args.file
    thread_count = args.thread
    urls = list(set(readfile(domain)))
    ThreadPool(cdn_check,urls,max_workers=thread_count)