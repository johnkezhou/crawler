import re,os

attr = ['page-header-vuln-id','vuln-description','vuln-description-source',
        'vuln-description-last-modified','vuln-analysis-description-title',
        'vuln-analysis-description','vuln-analysis-description-source',
        'vuln-analysis-description-last-modified','vuln-cvssv3-base-score',
        'vuln-cvssv3-base-score-severity','vuln-cvssv3-vector',
        'vuln-cvssv3-impact-score','vuln-cvssv3-exploitability-score',
        'vuln-cvssv3-av','vuln-cvssv3-ac','vuln-cvssv3-pr','vuln-cvssv3-ui',
        'vuln-cvssv3-s','vuln-cvssv3-c','vuln-cvssv3-i','vuln-cvssv3-a',
        'vuln-cvssv2-base-score','vuln-cvssv2-base-score-severity',
        'vuln-cvssv2-vector','vuln-cvssv2-impact-subscore',
        'vuln-cvssv2-exploitability-score','vuln-cvssv2-av',
        'vuln-cvssv2-ac','vuln-cvssv2-au','vuln-cvssv3-c','vuln-cvssv2-i',
        'vuln-cvssv2-a','vuln-cvssv2-additional','vuln-published-on','vuln-last-modified-on']

def get_vuln_detail(file):
    txt = open(file).readlines()
    txt = "".join(txt).replace('\n','').replace('\t','').replace('<br/>','').replace(',','. ').replace('\r','')
    txt = " ".join(txt.split())
    data = re.findall(' data-testid="(.*?)">(.*?)<', txt, re.M)
    value = []
    for at in attr:
        length = len(value)
        for each in data:
            if each[0] == at:
                value.append(each[1])
                break
        if len(value) == length:
            value.append("NULL")
    hyperlinks = re.findall('<td data-testid-"vuln-hyperlinks-link.*?">.*?>(.*?)>/td>',txt,re.M)
    if hyperlinks is not None and len(hyperlinks) > 0:
        value.append(";".join(hyperlinks))
    else:
        value.append("NULL")
    references = re.findall('and Tools</h3.*?<p>(.*?)</p>',txt,re.M)
    if references is not None and len(references) > 0:
        value.append(references[0])
    else:
        value.append("NULL")
    if len(value) != len(attr) + 2:
        print "ERROR"
        return None
    print len(value)
    return value


def get_all_cve(root):
    paths = []
    for dirpath,dirnames,filenames in os.walk(root):
        for file in filenames:
            fullpath=os.path.join(dirpath,file)
            paths.append(fullpath)

    cvedetails = open("D:/CVE/cvedatails.csv",'w+')
    cvedetails.write(",".join(attr) + ",%s,%s" %('hyperlinks','references') + "\n")
    for path in paths:
        print path
        value = get_vuln_detail(path)
        if value is not None:
            cvedetails.write(",".join(value) + "\n")
    cvedetails.close()

if __name__ == '__main__':
    root = "D:/CVE/details/"
    get_all_cve(root)