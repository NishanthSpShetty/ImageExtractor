#!/usr/bin/python

import urllib2
import os
import sys
from BeautifulSoup import BeautifulSoup

IMG_BASE_DIR = './pictures/';

def imageLoader(URL):
    print "Loading web page...please wait"
    #fetch response
    try :
        response = urllib2.urlopen(URL)
    except Exception as e:
        print "Error [ %s ]"%e
        return

    soup = BeautifulSoup(response.read())
    print "Page loaded, searching for images in the response"
    imgs = soup.findAll("img",{"alt":True,"src":True}) #get src and title too
    count = 0
    print "Total images found "+len(imgs)
    img_desc_file = open('image_descriptions.idf',"w")
    for img in imgs:
        print img
        #print img["alt"]
        img_url = img["src"];
        try :
            img_file = urllib2.urlopen(img_url)

        except Exception as e:
            #ignore the error
            continue
        img_file_name = IMG_BASE_DIR+img["alt"]+'.'+ img_url.split('.')[-1]

        #print img_file_name
        count+=1
        with open(img_file_name,"w") as f:
            f.write(img_file.read())

    print count+" Images loaded into "+IMG_BASE_DIR
    img_desc_file.close();



def main():
    if not os.path.exists(IMG_BASE_DIR):
        print "Base directory does not exist, creating.."
        os.makedirs(IMG_BASE_DIR)
    if len(sys.argv) == 2 :
        URL = sys.argv[1]
    else :
        URL = raw_input("Please enter the url ")

    imageLoader(URL)

if __name__ == '__main__':
    main()
