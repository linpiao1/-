import requests
import time
import xlwt
from lxml import etree

def main():
    Baseurl = 'https://weibo.cn/comment/Io28CCb0y?&page='
    data_list = getdata(Baseurl)
    savepath = '某某新闻评论.xls'
    Savedata(data_list,savepath)




def askurl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",

        "cookie": "_T_WM=3e40e78e41c9df6f8f7e348ecb2b43d0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhlIYCIji5f50-jfkch7n4y5JpX5KzhUgL.FoM7SK-41h-pS0z2dJLoIE5LxKMLB--L1KMLxKBLB.2L1hqLxK-L1K5LBKMNeoBc1Btt; SCF=AmvmEtdgbVNBLmY81b6nBUc87xPm36q8vSZjcyCgj68xqpzgSuQ4FbDSk7z5GrQF5i2SE4WSkzxvThn6_ftoHAI.; SUB=_2A25yhdDPDeRhGeFO7lcY-CvNzD6IHXVRifCHrDV6PUNbktAKLXLGkW1NQXWt35eq1acxAZMK7yH94HK9PDFVwq1x; SUHB=0u5Bp7gwLbKopm; SSOLoginState=1602330783; ALF=1604922783"
    }
    response = requests.get(url,headers = head)
    html = response
    return html

def getdata(Baseurl):
    data_list = []
    for i in range(1,3):
        print('正在爬取第'+str(i)+'页')
        url = Baseurl +str(i)
        time.sleep(2)
        html = askurl(url)

        html_ele = etree.HTML(html.text.encode('utf-8'))
        item = html_ele.xpath('/html/body/div[@class="c"][contains(@id,"C_")]')


        for i in item:
            data = []
            if i.xpath('./@id') != 'M_':
                comment = i.xpath('.//span[@class="ctt"]/text()')
                #print(comment)
                if len(comment) != 0:
                    data.append(comment)
                else:
                    data.append('')

            data_list.append(data)
    X = len(data_list)
    data_list.append(X)
    print(data_list)

    return data_list

def Savedata(data_list,savepath):
    print('save...')
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)  # 创建工作表

    col = ('评论')
    for i in range(0,1):
        sheet.write(0,i,col[i])
    for i in range(0, data_list[-1]):
        print('第%d条' % (i + 1))
        data = data_list[i]  # 要保存的数据
        #print(data)
        for j in range(0, 1):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)

if __name__ == '__main__':
    main()
    print('爬取完毕')







