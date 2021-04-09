import requests
import re
from lxml import etree
import time

def main():
    Baseurl = 'https://www.fabiaoqing.com/biaoqing/lists/page/'
    # 1.爬取网页
    data_list = getdata(Baseurl)
    saveData(data_list)

def getdata(Baseurl):
    data_list = []
    for i in range(1,50):   #爬取的页数范围
        print('第'+str(i)+'页')
        url = Baseurl + str(i)
        print(url)
        time.sleep(2)
        try:

            html = askurl(url)

        except:
            time.sleep(2)
            html = askurl(url)
            #print(html)

        html_ele = etree.HTML(html.text.encode("utf-8"))
        #print(html_ele)
        item = html_ele.xpath('/html/body//div[@class="tagbqppdiv"][contains(@style,"vertical-align: middle;")]')
        print(item)
        for i in item :
            data = []
            picturelink = i.xpath('./ a /img/@data-original')
            if len(picturelink) != 0:
                picturelink = picturelink[0]
                data.append(picturelink)

            else:
                data.append('')

            data_list.append(data)
    return data_list


def askurl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",

        "cookie": "PHPSESSID=nv4e7tdc7n4j2knql1rljdodi5; UM_distinctid=178b01a5f4927e-0d5a7ec9d43f408-4c3f237d-144000-178b01a5f4a691; CNZZDATA1260546685=1773672731-1617860045-https%253A%252F%252Fwww.baidu.com%252F%7C1617860045; __gads=ID=3afb9fa626ad3547-221a3c290ec70009:T=1617862222:RT=1617862222:S=ALNI_MaoVkOqA6eA8v6g1OM40AZtUfBHeQ"
    }
    response = requests.get(url,headers = head)
    html = response
    return html


def saveData(data_list):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",

        "cookie": "PHPSESSID=nv4e7tdc7n4j2knql1rljdodi5; UM_distinctid=178b01a5f4927e-0d5a7ec9d43f408-4c3f237d-144000-178b01a5f4a691; CNZZDATA1260546685=1773672731-1617860045-https%253A%252F%252Fwww.baidu.com%252F%7C1617860045; __gads=ID=3afb9fa626ad3547-221a3c290ec70009:T=1617862222:RT=1617862222:S=ALNI_MaoVkOqA6eA8v6g1OM40AZtUfBHeQ"
    }
    print("save...")
    for ii in data_list:
        file_name = ii[0].split('/')[-1]
        print(file_name)
        res = requests.get(ii[0],headers = head)
        with open(r'D:/biaoqingbao/'+file_name,'wb') as f:
            f.write(res.content)



if __name__ == '__main__':  # 当程序执行时
    main()
    print("爬取完毕!")
