import re
import requests
import traceback
from bs4 import BeautifulSoup
print('21100510301 蔡建宏')
def gethttptext(url,code='utf-8'):
    #获得url对应的页面
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=code
        #print(r.status_code)
        return r.text
    except:
        return ""
def getstocklist(list,stockurl):#参数：股票信息保存在list列表，stockurl为获得列表的网站
    #获得股票的信息列表
    html=gethttptext(stockurl) #获得一个页面
    soup=BeautifulSoup(html,'html.parser') #解析页面
    tr =soup.find_all('tr') #找到全部tr标签 列表信息保存在tr标签中
    for i in tr: #遍历所有tr标签
        try:
            listid =i.attrs['id']#找到每个tr标签的id属性
            list.append(re.findall(r'[tr]\d{6}',listid)[0]) #找到tr链接域开头后面有6个数字
        except:
            continue #发生异常跳过此次循环进行下一次循环
 
def getstockinfo(list,stockurl,fpath):#参数fpath文件保存路径
    #获得每一支个股的股票信息并把它存到一个数据结构
    count=0
    for stock in list:
        url=stockurl+stock[1:]+".html"#固定链接格式加上每个个股的链接不同的地方
        html=gethttptext(url)
        try:
            if html=='':#判断是否为空页面
                continue
            infodict={} #定义一个字典储存当前页面返回的所有信息
            soup=BeautifulSoup(html,'html.parser') #解析
            stockinfo=soup.find('div',attrs={'class':'merchandiseDetail'}) #attrs检验注释并创建一个类
 
    
            name=stockinfo.find_all(attrs={'class':'fundDetail-tit'})[0]  #查找股票名称封装在fundDetail-tit对应的标签内
            infodict.update({'股票名称':name.text.split()[0]})   
 
            keylist=stockinfo.find_all('dt')
            valuelist=stockinfo.find_all('dd')
            for i in range(len(keylist)):
                key=keylist[i].text
                val=valuelist[i].text
                infodict[key]=val
            with open(fpath,'a',encoding='utf-8') as f:
                f.write(str(infodict)+'\n')
                count=count+1
                print('\r当前速度：{:.2f}%'.format(count*100/len(list)),end='')
 
        except:
            count = count + 1
            print('\r当前速度：{:.2f}%'.format(count * 100 / len(list)), end='')
            traceback.print_exc()
            continue

def main():
    stock_list_url="https://fund.eastmoney.com/fund.html"#获取列表
    stock_info_url="https://fund.eastmoney.com/"#获取信息
    output_fire="C:\\Users\\123\\Desktop\\gupiao1.txt"
    slist=[] #股票列表 
    print(slist)
    getstocklist(slist,stock_list_url) #获得股票列表
    getstockinfo(slist,stock_info_url,output_fire)#根据股票列表到相关网站上获取股票信息并存储到相关文件中
   
main()