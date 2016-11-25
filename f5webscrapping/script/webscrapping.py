import sys
import csv
import urllib.request as urllib
import lxml.html
#Two ouput:
# 1 xls file with data file name, Product and version, Default Tag
#Collection of all the data file
import sys
import lxml.html
from selenium import webdriver
class WebScrap:
    def __init__(self):
        #Main URL include query to remove the archived and also select all
        self.main_url="https://support.f5.com/kb/en-us/search.res.html?q=+inmeta:archived%3DArchived%2520documents%2520excluded&dnavs=inmeta:archived%3DArchived%2520documents%2520excluded&filter=p&num="
        #"https://support.f5.com/kb/en-us/search.res.html?productList=big-ip%2Cbc%2Cfp%2C3-dns%2Clc%2Cts%2Cwj%2Cwa_5_x%2Csam%2Clinerate-eol&versionList=all%2C&searchType=basic&isFromGSASearch=false&query=&site=support_external&client=support-f5-com&q=&prodName=ALL&prodVersText=&docTypeName=ALL&includeArchived=false&submit_form=&product=all&eolProducts=all&documentType=all"
        #Update URL for future use
        self.update_url="https://support.f5.com/kb/en-us/recentadditions.html?rs=30"
        pass
    
    def downloadData(self,fname,url):
        loc="dataFiles/"+str(fname)
        file_open=open(loc,'a')
        try:
            connection = urllib.urlopen(url)
        except Exception as e:
            print(e.code)
            exit(-1)
        dom = lxml.html.fromstring(connection.read())
        query = "//div[@class='parsys pageContent']//text()"
        for text in dom.xpath(query):
            file_open.write(text)
        file_open.close()

    def getDetails(self,url):
        driver = webdriver.PhantomJS()
        list_Product = []
        tag = "None"
        try:
            driver.set_window_size(1120, 550)
            driver.get(url)

            #For Tag
            tag=driver.find_element_by_xpath("//meta[@name='kb_doc_type']").get_attribute("content")
            if tag=="":
                tag=="None"
            #For Product

            for ele in driver.find_elements_by_xpath("//meta[@name='product']"):
                list_Product.append(ele.get_attribute("content"))
            #print(list_Product)
            pro_ver = dict()
            for product in list_Product:
                query_od = "//meta[@name='" + str(product) + "']"
                driver.find_element_by_xpath(query_od).get_attribute("content")
                pro_ver[product] = list(str(driver.find_element_by_xpath(query_od).get_attribute("content")).rsplit(','))
        except Exception as e:
            print(e.code)
        finally:
            print("")
            driver.close()
        return tag,pro_ver

    def getFiles(self):
        #Number of test doc 15
        #outfile = open('prod.csv', 'w')
        #outfile.close()
        outfile = open('prod.csv', 'a')
        writer = csv.writer(outfile)
        for i in range(1,15):
            link_id=i*10
            link=self.main_url+str(link_id)+str("&start=")+str(link_id)
            try:
                connection = urllib.urlopen(link)
            except urllib.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                sys.exit(1)
            except urllib.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
                sys.exit(1)
            dom = lxml.html.fromstring(connection.read())
            query = "//div[@class=\"main-results\"]//a/@href"
            for lnk in dom.xpath(query):
                file_name=str(lnk).rsplit('/',1)[-1]
                tag,prod=self.getDetails(lnk)
                print(file_name)
                print(tag)
                print(prod)
                for key, value in prod.items():
                    writer.writerow([file_name,lnk,tag,key, value])
                #Add part to download the data content of lnk 
                self.downloadData(file_name,lnk)


if __name__ == '__main__':
    w=WebScrap()
    w.getFiles()
