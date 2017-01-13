import sys
import csv
import urllib.request as urllib
import lxml.html
import signal
import sys
import os
import lxml.html
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
class WebScrap:
    def __init__(self):
        #Main URL include query to remove the archived and also select all
        self.main_url="https://support.f5.com/csp/#/article/KXXXXXXXX"
        #"https://support.f5.com/kb/en-us/search.res.html?productList=big-ip%2Cbc%2Cfp%2C3-dns%2Clc%2Cts%2Cwj%2Cwa_5_x%2Csam%2Clinerate-eol&versionList=all%2C&searchType=basic&isFromGSASearch=false&query=&site=support_external&client=support-f5-com&q=&prodName=ALL&prodVersText=&docTypeName=ALL&includeArchived=false&submit_form=&product=all&eolProducts=all&documentType=all"
        #Update URL for future use
        #self.logfile=open("logfile",'a')
        self.update_url="https://support.f5.com/kb/en-us/recentadditions.html?rs=30"
        desired_cap = {
        'phantomjs.page.settings.loadImages' : False,
        'phantomjs.page.settings.resourceTimeout' : 100000000,
        'phantomjs.page.settings.userAgent' : '...'
        }
        self.driver= webdriver.PhantomJS('/u/ankswarn/MindShift/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',desired_capabilities=desired_cap)
        #self.driver= webdriver.Chrome(chromedriver,service_args=service_args,service_log_path=service_log_path)        
        pass
    def download_files(self):
        i=16500
        logfile = open('new.log.file', 'a')
       
        while(True):
            print("\r\n Link ID:"+str(i))
            return_id=self.getFiles(str(i))
            logfile.write("\r\nLink ID: K"+str(i)+" Return: "+str(return_id))
            i+=1
            if i >= 999999999:
              break
        self.driver.close()
        #logfile.close()  
        '''
        #test
        self.getFiles(str(4852))
        self.driver.close()
        #logfile.close()
        '''
        
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
            self.logfile.write("\nException with url:"+str(url)+"\n")
        finally:
            print("")
           # driver.service.process.send_signal(signal.SIGTERM) # kill the specific phantomjs child proc
           # driver.quit()                                      # quit the node proc
           # driver.close()
        return tag,pro_ver

    def writeData(self,fname,url):
        loc="dataFiles/"+str(fname)
        file_open=open(loc,'a')
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

    def getFiles(self,linkid):
        #Number of test doc
        #outfile = open('prod.csv', 'w')
        #outfile.close()
        loc="dataFiles/K"+linkid
        #outfile = open('prod.csv', 'a')
        #writer = csv.writer(outfile)
        link=self.main_url.replace("XXXXXXXX",linkid)
        
        try:
            self.driver.get(link)
            title=self.driver.find_element_by_xpath("//div[@class=\"col-sm-12 col-lg-12\"]/h2")
            #attrs = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', title)
            #print(attrs)
             
            test3=self.driver.find_elements_by_xpath("//div[@class=\"row productInfo\"]/div[@class=\"col-sm-12 col-lg-12\"]/div[@class=\"ng-scope\"]/div[@class=\"article-content ng-binding\"]/p")
            if test3.__len__()==0 :
              return -1
            file_open=open(loc,'w')
            file_open.write(title.get_attribute('innerText'))
            file_open.write("\r\n")
            for t in test3:
                file_open.write(t.get_attribute('innerText'))
                file_open.write(" ")
            file_open.close()
            return 0
        except urllib.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e)
            return -1
            
        except urllib.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e)
            return -1
        except NoSuchElementException as e:
            print('Element not error')
            return -1
        except Exception as e:
            print("Some Error")
            return -1

       # exit(-1)
        #outfile.close()


if __name__ == '__main__':
    w=WebScrap()
    w.download_files()
