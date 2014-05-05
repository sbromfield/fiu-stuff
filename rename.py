import xml.dom.minidom
import os
import subprocess

results = []

with open('mediarss.xml') as xmlfile:
  xmltext = xmlfile.read()
  dom = xml.dom.minidom.parseString(xmltext)
  classname = dom.getElementsByTagName("title")[0].childNodes[0].data
  
  classes = dom.getElementsByTagName('item')

  for myclass in classes:
    if myclass.childNodes[0].firstChild is not None:
       title = myclass.childNodes[0].firstChild.data
       url =  myclass.childNodes[4].firstChild.data
       k = myclass.childNodes[4].firstChild.data.rfind("/") + 1
       results.append((url[k:] ,title))

  for x,k in results:
    os.chdir(x)
    print os.getcwd()
    os.rename("MPEG-4-HD.mp4", k.replace(" ", "-") +".mp4")
    os.chdir("..")
    print os.getcwd()
