

import requests
import re
import time
import os

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

sc = open('D:/CVE/status_code','a+')

def get_html(url):
    try:
        response = requests.get(url, verify=False)
        sc.write(url+"\t"+str(response.status_code)+"\n")
        print url, response.status_code
        if response.status_code != 200:
            print url, response.status_code
            time.sleep(300)
        time.sleep(1)
        return response.content
    except Exception as e:
        print url, str(e)
        sc.write(url+"\t"+str(e)+"\n")
        return 'None'

host = 'https://nvd.nist.gov'
def get_nvd_first_level():
    url = 'https://nvd.nist.gov/vuln/full-listing'
    txt = requests.get(url, verify=False).content
    time_urls = re.findall(r'<a href="(/vuln/full-listing/2.*?)">',txt,re.M)
    for i in range(0, len(time_urls)):
        time_urls[i] = host + time_urls[i]
    f = open('D:/CVE/time_urls','w')
    f.write("\n".join(time_urls))
    f.close()
    return time_urls

def get_cve_detail_url(time_url):
    txt = requests.get(time_url, verify=False).content
    detail_urls = re.findall(r'<a href="(/vuln/detail/CVE.*?)">',txt,re.M)
    for i in range(0, len(detail_urls)):
        detail_urls[i] = host + detail_urls[i]
    f = open('D:/CVE/detail_urls','a+')
    f.write("\n".join(detail_urls) + "\n")
    f.close()
    print detail_urls

def get_cve_detail_urls():
    time_urls = get_nvd_first_level()
    for url in time_urls:
        print url
        get_cve_detail_url(url)
        time.sleep(1)

def get_cve_detail_html(url):
    name = url.split('/')[-1]
    path = 'D:/CVE/details/' + name
    f = open(path, 'w')
    f.write(get_html(url))
    f.close()
    print "[%s] download successfully!" % name

if __name__ == '__main__':

    urls = open('D:/CVE/detail_urls','r').readlines()
    t = 20000
    for i in range(10000,t):
        print i
        get_cve_detail_html(urls[i].replace('\n',''))
    sc.close()