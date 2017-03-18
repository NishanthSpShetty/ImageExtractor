#!/usr/bin/python
import random
import urllib2
import os
import sys
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

grouping = True

IMG_BASE_DIR = './pictures/';
ignore_words = ['and','or','this','that','of','on','at','the','where','from','to'];
def imageLoader(URL,grouping_word_list,img_desc_file_name="img_desc_file.idf"):
    print "Loading web page : %s"%URL
    print "Please wait..."
    #fetch response

    url_parsed = urlparse(URL)

    domain = url_parsed.scheme+'://'+url_parsed.netloc

    print domain

    opener = urllib2.build_opener()
    #spoof User-Agent
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36')]

    try :
        response =  opener.open(URL)
        #response = urllib2.urlopen(URL)
    except Exception as e:
        print "Error [ %s ]"%e
        return
    #print "URL is",response.geturl()
    #print "Info ",response.info()
    soup = BeautifulSoup(response.read())
    print "Page loaded, searching for images in the response"
    imgs = soup.findAll("img",{"alt":True,"src":True}) #get src and title too
    count = 0
    table = []
    print "Total images found %d"%len(imgs)
    img_desc_file = open(img_desc_file_name,"a")
    for img in imgs:
        #print img
        #print img["alt"]
        img_url = img["src"].encode(sys.getfilesystemencoding());
        try :

            if img_url.startswith('/'):
                imgurl=domain+img_url
            else :
                imgurl=img_url
            print "loading ",img_url
            #img_file = urllib2.urlopen(img_url)
            img_file = opener.open(imgurl)
        except Exception as e:
            #ignore the error
            print "skipped...",e

            continue
        for grouping_word in grouping_word_list:
            img_file_name = img["alt"]+str(int(random.random()*10000))+'.'+ img_url.split('.')[-1]
            try:
                desc = img["alt"] #contains image description
    #        fname = img_file_name.encode(sys.getfilesystemencoding())
                if grouping:
                    if grouping_word in desc.lower():
                        if not os.path.isdir(IMG_BASE_DIR+grouping_word):
                            os.makedirs(IMG_BASE_DIR+grouping_word)
                        img_file_name = IMG_BASE_DIR +grouping_word+'/'+img_file_name
                else:
                    img_file_name = IMG_BASE_DIR +img_file_name
                
                #print img_file_name
                data = "%02s\nDesc  : %s\nFilename : %s\n%s\n"%(count,img["alt"],img_file_name.encode(sys.getfilesystemencoding()),"-"*130)
                #print data
                img_desc_file.write(data)
            
                with open(img_file_name.encode(sys.getfilesystemencoding()),"wb") as f:
                    f.write(img_file.read())
                count+=1
            except Exception as e:
                print "skipped...",e
                pass
    print count," images loaded into "+IMG_BASE_DIR
    img_desc_file.close();



def main():
    if not os.path.exists(IMG_BASE_DIR):
        print "Base directory does not exist, creating.."
        os.makedirs(IMG_BASE_DIR)
    if len(sys.argv) == 2 :
        URL = sys.argv[1]
    else :
        URL = raw_input("Please enter the url ")
    grouping_word = raw_input("Please enter word to group the images : ")
    if grouping_word:
        grouping = False
    imageLoader(URL,grouping_word.split(' '))
if __name__ == '__main__':
    main()
