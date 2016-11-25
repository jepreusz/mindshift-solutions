import sys
import csv
import urllib.request as urllib
import lxml.html
import signal
#Two ouput:
# 1 xls file with data file name, Product and version, Default Tag
#Collection of all the data file
import sys
import os
import lxml.html
from selenium import webdriver
class WebScrap:
    def __init__(self):
        #Main URL include query to remove the archived and also select all
        self.main_url="https://support.f5.com/kb/en-us/search.res.html?q=+inmeta:archived%3DArchived%2520documents%2520excluded&dnavs=inmeta:archived%3DArchived%2520documents%2520excluded&filter=p&num="
        #"https://support.f5.com/kb/en-us/search.res.html?productList=big-ip%2Cbc%2Cfp%2C3-dns%2Clc%2Cts%2Cwj%2Cwa_5_x%2Csam%2Clinerate-eol&versionList=all%2C&searchType=basic&isFromGSASearch=false&query=&site=support_external&client=support-f5-com&q=&prodName=ALL&prodVersText=&docTypeName=ALL&includeArchived=false&submit_form=&product=all&eolProducts=all&documentType=all"
        #Update URL for future use
        self.logfile=open("logfile",'a')
        self.update_url="https://support.f5.com/kb/en-us/recentadditions.html?rs=30"
        desired_cap = {
        'phantomjs.page.settings.loadImages' : True,
        'phantomjs.page.settings.resourceTimeout' : 10000,
        'phantomjs.page.settings.userAgent' : '...'
        }
        self.driver= webdriver.PhantomJS('/u/ankswarn/MindShift/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',desired_capabilities=desired_cap)
        #self.driver= webdriver.Chrome(chromedriver,service_args=service_args,service_log_path=service_log_path)        
        pass
    def dowload_file(self):
        pass

    def getDetails(self,url):
        #driver = webdriver.PhantomJS('/u/ankswarn/MindShift/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        list_Product = []
        tag = ""
        pro_ver = dict()
        try:
            #driver.set_window_size(1120, 550)
            self.driver.get(url)

            #For Tag
            try:
                tag=self.driver.find_element_by_xpath("//meta[@name='kb_doc_type']").get_attribute("content")
            
            except Exception as e:
                if tag=="":
                   tag=="None"
            #For Product
            try:
                for ele in self.driver.find_elements_by_xpath("//meta[@name='product']"):
                    list_Product.append(ele.get_attribute("content"))
                #print(list_Product)
                #pro_ver = dict()
            except Exception as e2:
                return tag,pro_ver
            for product in list_Product:
                query_od = "//meta[@name='" + str(product) + "']"
                self.driver.find_element_by_xpath(query_od).get_attribute("content")
                pro_ver[product] = list(str(self.driver.find_element_by_xpath(query_od).get_attribute("content")).rsplit(','))
        except Exception as e:
            print(e)
            print("Exception with url:"+str(url))
            self.logfile.write("Exception with url:"+str(url)+"\n")
        finally:
            print("")
           # driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
           # driver.quit()                                      # quit the node proc
           # driver.close()
        return tag,pro_ver

    def downloadData(self,fname,url):
        loc="dataFiles/"+str(fname)
        file_open=open(loc,'w')
        try:
            connection = urllib.urlopen(url)
        except Exception as e:
            print(e)
            #exit(-1)
            return
        dom = lxml.html.fromstring(connection.read())
        query = "//div[@class='parsys pageContent']//text()"
        for text in dom.xpath(query):
            file_open.write(text)
        file_open.close()



    def getFiles(self):
        #Number of test doc
        #outfile = open('prod.csv', 'w')
        # outfile.close()
        outfile = open('prod.csv', 'a')
        writer = csv.writer(outfile)
        for i in range(1,40):
            link_id=i*10
            link=self.main_url+str(link_id)+str("&start=")+str(link_id)
            try:
                connection = urllib.urlopen(link)
            except urllib.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e)
                continue
            except urllib.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e)
                continue
            dom = lxml.html.fromstring(connection.read())
            query = "//div[@class=\"main-results\"]//a/@href"
            for lnk in dom.xpath(query):
                file_name=str(lnk).rsplit('/',1)[-1].replace("html","txt")
                tag,prod=self.getDetails(lnk)
                print(file_name)
                print(tag)
                print(prod)
                for key, value in prod.items():
                    writer.writerow([file_name,lnk,tag,key, value])

                self.downloadData(file_name,lnk)
        self.driver.quit()


if __name__ == '__main__':
    w=WebScrap()
    w.getFiles()

