import dns.resolver
import argparse
import re 

def cdn_check(domain):
    """
    if   cdn    return True,domain
    else        return False,domain
    """
    ipcount = 0
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['1.1.1.1', '8.8.8.8']
        domain = domain.strip()
        a = resolver.resolve(domain, 'A')
        for index,value in enumerate(a.response.answer):
            for j in value.items:
                if re.search(r'\d+\.\d+\.\d+\.\d+', j.to_text()):
                    ipcount += 1
                    if ipcount >= 2:
                        return True,domain
                elif re.search(r'(\w+\.)+', j.to_text()):
                    cname = j.to_text()[:-1]
                    p1 = '.'.join(cname.split('.')[-2:])
                    p2 = '.'.join(domain.split('.')[-2:])
                    if p1 == p2:
                        return False,domain
                    else:
                        return True,domain
                else:
                    return False,domain
        if ipcount == 1:
            return False,domain
    except Exception as e:
        return None,domain
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='by Scrboy.')
    parser.add_argument('-u', '--url', type=str, default='huya.com')
    args = parser.parse_args()
    domain = args.url
    print(cdn_check(domain))