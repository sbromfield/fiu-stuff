import sys
import json
import feedparser
import re
import datetime
import smtplib


def check(title, timecheck):
  regex = re.compile("(\d+)")
  r= regex.findall(title)
  t = datetime.date.today()
  if int(timecheck) == 0:
     t = t -datetime.timedelta(0)
  else:
     t = t -datetime.timedelta(1)
     
  classday = int(t.strftime("%d"))

  if r:
    day = int(r[0])
    if day == classday:
      return True
    else:
      return False

  else:
    return False

if __name__ == "__main__":
  fromaddr = "coursecapture@fiu.edu"
  sname = "smtpout.fiu.edu"
  date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
  whichday = 0
  r = []

  if len(sys.argv) == 2:
    print "Opening " + sys.argv[1]
  elif len(sys.argv) == 3:
    whichday = 1
    print "Opening " + sys.argv[1]
  else:
    print "error with parameters"
    sys.exit(0) 

  print sys.argv
  f = open(sys.argv[1])
  data = json.load(f)
  result = ""

  for k in data:
    d = feedparser.parse(k[1].replace(" ", "%20"))
    index = len(d.entries) - 1 
    test = check(d.entries[index].title, whichday)

    if test == False :
      r.append( "Problem with class " + k[0])
      print "problem with class " + k[0]
    else:
      print k[0] + " recorded just fine."
      r.append( k[0] + " recorded just fine." )

  for txt in r:
    result = result + "\n " + txt
 
  msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromaddr, "coursecapture@fiu.edu", "Report of class recordings ", date, result )
  server = smtplib.SMTP(sname)
  server.sendmail(fromaddr, "coursecapture@fiu.edu", msg)
  #server.sendmail(fromaddr, "sbromfi@fiu.edu", msg)
