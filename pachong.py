from bs4 import BeautifulSoup as bs
import urllib.request
from urllib.request import HTTPError
#这里是呼吸系统常用药物的url
# fr = open('drug_dict.txt', 'w')

# url_o = 'http://www.chealth.org.cn/mon/classifications_drug/article/MJ157000325_'
# txt = []
# i = 1
# while True:
#     url = url_o + str(i) + '.html'
#     try:
#         data = urllib.request.urlopen(url).read()
#         html = data.decode('utf8')
#         soup = bs(html, 'lxml')
#         for tag in soup.find_all('a'):
#             txt.append(tag.string)
#             fr.write(tag.string)
#             fr.write('\n')
#         i += 1
#     except HTTPError as e:
#         print ('ERROR: ' + e.reason)
#         break
# fr.close()

drug_url = 'http://www.chealth.org.cn/mon/classifications_drug/article/MJ157000325_1.html'
disease_url = 'http://www.chealth.org.cn/mon/departments_disease/article/MF149027411_1.html'


def get_content(starturl, filename):
    url_o = starturl[:-6]
    fr = open(filename, 'w')
    i = 1
    while True:
        url = url_o + str(i) + '.html'
        try:
            data = urllib.request.urlopen(url).read()
            html = data.decode('utf8')
            soup = bs(html, 'lxml')
            for tag in soup.find_all('a'):
                #txt.append(tag.string)
                fr.write(tag.string)
                fr.write('\n')
            i += 1
        except HTTPError as e:
            #print ('ERROR: ' + e.reason)
            break
    fr.close()
get_content(drug_url, 'drugdict.txt')
get_content(disease_url, 'diseasedict.txt')