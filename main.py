import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from cdnCheck import cdn_check
import argparse

def ThreadPool(func,urls,max_thread=10):
    l=[]
    p = ThreadPoolExecutor(max_thread)
    for url in urls:
        obj = p.submit(func, url)
        l.append(obj)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        to_do = []
        for url in urls:
            obj = p.submit(cdn_check, url)
            to_do.append(obj)
    for future in concurrent.futures.as_completed(to_do):
        result, domain = future.result()
        if result is False:
            savefile('result/nocdnResult.txt',domain)
        elif result is True:
            savefile('result/cdnResult.txt',domain)
        else:
            savefile('result/errorResult.txt',domain)

        
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
    args = parser.parse_args()
    domain = args.file
    urls = readfile(domain)
    ThreadPool(cdn_check,urls,max_thread=20)